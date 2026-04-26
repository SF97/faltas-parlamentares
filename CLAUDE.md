# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Static PT-PT site that ranks Assembleia da República MPs of the **XVII Legislatura** by plenary absences. Two halves:

- `ingest/` — Python 3.12 + uv + httpx. Scrapes parlamento.pt HTML and writes JSON files into `site/src/data/`.
- `site/` — Astro 6 static site that consumes those JSON files at build time. Deployed via GitHub Pages (`.github/workflows/update.yml`, daily cron at 06:00 UTC).

The ingest output is *committed* to the repo by the cron job; the site rebuilds from those committed JSONs.

## Common commands

```bash
# Ingest (run from ingest/)
uv sync
uv run python -m ingest.main         # uses local HTTP cache under ingest/.cache/http
FALTAS_NO_CACHE=1 uv run python -m ingest.main   # force re-fetch (what CI uses)

# Site (run from site/) — pnpm only, not npm
pnpm install
pnpm dev          # http://localhost:4321
pnpm build        # outputs to site/dist
pnpm preview
```

There is no test suite and no linter configured.

## Architecture notes

**Data flow.** `ingest/ingest/main.py` is the only entry point. It:
1. Fetches the substitutions page (`AlteracoesComposicaoPlenario.aspx`) → `site/src/data/substituicoes.json`.
2. Fetches one "session roster" page (`ROSTER_SESSION_BID = 376274` — chosen because it has all 230+ deputados present) to get the full list of MPs and their BIDs. There's a sanity check that aborts if fewer than 200 deputies parse — the parlamento.pt HTML has changed if this trips.
3. For each MP, fetches `PresencasReunioesPlenarias.aspx?BID={bid}` to get their attendance list.
4. For each unique session BID across all attendances, fetches the session roster again to learn the per-MP `motivo` (justification text) for that session.
5. Writes per-deputy detail (`site/src/data/deputado/{bid}.json`), summary (`deputados.json`), and `meta.json`.

**Parsing is regex over raw HTML** (`parse.py`, `alteracoes.py`). No DOM library — the regexes target specific ASP.NET span IDs (`lblPresenca`, `lblMotivo`, `lblData`, `lblSubstituicao`, etc.). When parlamento.pt changes markup, these are the things to fix.

**Status codes** (`parse.py:STATUS_CODES`) are the canonical short codes used everywhere downstream: `P`, `FJ`, `FI`, `AMP`, `FQV`, `PNO`. The Portuguese long-form labels are the keys.

**HTTP fetch** (`fetch.py`) caches all responses under `ingest/.cache/http/` keyed by sha256(url). Set `FALTAS_NO_CACHE=1` to bypass — CI always does this.

**Substitutions / suplentes.** The "substituições" mechanism matters: when an effective deputy is temporarily replaced by a suplente, the missing sessions show up on the *suplente's* page, not the effective's. So a low `total_reunioes` does **not** mean someone is "a substitute" — it usually means they were rarely called in. `events_for()` in `main.py` attaches entrada/saida events to each deputy's detail JSON.

**Site build.** Astro pages under `site/src/pages/` import the JSON directly. Dynamic routes:
- `pages/deputado/[bid].astro` — one page per MP, generated via `getStaticPaths` from `deputados.json`.
- `pages/motivo/[slug].astro` — aggregates by justification reason, slugified from the FJ `motivo` field.

`site/src/lib/base.ts` exports `base` (`import.meta.env.BASE_URL` trimmed) — always use it when constructing internal links so the site works under both root and a subpath.

## Conventions

- Project name in code/UI: **faltas-parlamentares** (or "Faltas parlamentares").
- All user-facing text is **Portuguese (PT-PT)**.
- Scope is **XVII Legislatura only**. Don't add multi-legislature logic unless asked.
- pnpm only on the site side; uv only on the ingest side.
- Don't commit `ingest/.cache/` (gitignored). The committed data lives in `site/src/data/`.
