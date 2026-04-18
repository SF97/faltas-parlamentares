from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from dataclasses import asdict

from .alteracoes import Alteracao, fetch_alteracoes
from .fetch import BASE_URL, fetch
from .parse import STATUS_CODES, parse_attendance, parse_session_roster

SITE_DATA = Path(__file__).resolve().parents[2] / "site" / "src" / "data"
ROSTER_SESSION_BID = 376274


def detalhe_url(bid: int) -> str:
    return f"{BASE_URL}/DeputadoGP/Paginas/DetalheReuniaoPlenaria.aspx?BID={bid}"


def presencas_url(bid: int) -> str:
    return f"{BASE_URL}/DeputadoGP/Paginas/PresencasReunioesPlenarias.aspx?BID={bid}"


def code_for(label: str) -> str:
    return STATUS_CODES.get(label, "UNKNOWN")


def events_for(name: str, alteracoes: list[Alteracao]) -> list[dict]:
    """Return substitution events that concern `name`, tagged entrada/saida."""
    out: list[dict] = []
    for a in alteracoes:
        if a.substituto == name:
            out.append({"data": a.data, "tipo": "entrada", "motivo": a.motivo, "contraparte": a.substituido})
        elif a.substituido == name:
            out.append({"data": a.data, "tipo": "saida", "motivo": a.motivo, "contraparte": a.substituto})
    out.sort(key=lambda e: e["data"])
    return out


def main() -> int:
    SITE_DATA.mkdir(parents=True, exist_ok=True)
    (SITE_DATA / "deputado").mkdir(exist_ok=True)

    print("alteracoes: fetching…", file=sys.stderr)
    alteracoes = fetch_alteracoes()
    print(f"alteracoes: {len(alteracoes)} events", file=sys.stderr)
    (SITE_DATA / "substituicoes.json").write_text(
        json.dumps([asdict(a) for a in alteracoes], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"roster: fetching session {ROSTER_SESSION_BID}…", file=sys.stderr)
    roster_rows = parse_session_roster(fetch(detalhe_url(ROSTER_SESSION_BID)))
    print(f"roster: {len(roster_rows)} deputies", file=sys.stderr)
    if len(roster_rows) < 200:
        raise SystemExit(
            f"roster sanity check failed: got {len(roster_rows)} deputies "
            f"(expected ≥200). Parliament's HTML may have changed."
        )

    attendances: dict[int, list] = {}
    for i, r in enumerate(sorted(roster_rows, key=lambda x: x.name), 1):
        print(f"[{i}/{len(roster_rows)}] attendance {r.name} (BID={r.bid})", file=sys.stderr)
        attendances[r.bid] = parse_attendance(fetch(presencas_url(r.bid)))

    session_bids = sorted({e.session_bid for entries in attendances.values() for e in entries})
    print(f"motivos: fetching {len(session_bids)} session pages…", file=sys.stderr)
    motivos: dict[int, dict[int, str]] = {}
    for j, sbid in enumerate(session_bids, 1):
        print(f"[{j}/{len(session_bids)}] session {sbid}", file=sys.stderr)
        rows = parse_session_roster(fetch(detalhe_url(sbid)))
        motivos[sbid] = {row.bid: row.motivo for row in rows if row.motivo}

    summary: list[dict] = []
    for r in sorted(roster_rows, key=lambda x: x.name):
        entries = attendances[r.bid]
        codes = Counter(code_for(e.status) for e in entries)

        detail = {
            "bid": r.bid,
            "nome": r.name,
            "gp": r.party,
            "totais": dict(codes),
            "total_reunioes": len(entries),
            "eventos": events_for(r.name, alteracoes),
            "sessoes": [
                {
                    "data": e.date,
                    "reuniao_bid": e.session_bid,
                    "estado": code_for(e.status),
                    "estado_label": e.status,
                    "motivo": motivos.get(e.session_bid, {}).get(r.bid) or None,
                }
                for e in entries
            ],
        }
        (SITE_DATA / "deputado" / f"{r.bid}.json").write_text(
            json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        summary.append(
            {
                "bid": r.bid,
                "nome": r.name,
                "gp": r.party,
                "total_reunioes": len(entries),
                "presencas": codes.get("P", 0),
                "faltas_justificadas": codes.get("FJ", 0),
                "faltas_injustificadas": codes.get("FI", 0),
                "missao_parlamentar": codes.get("AMP", 0),
                "falta_quorum_votacao": codes.get("FQV", 0),
            }
        )

    summary.sort(key=lambda d: -(d["faltas_injustificadas"]))
    (SITE_DATA / "deputados.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    meta = {
        "legislatura": "XVII",
        "roster_session_bid": ROSTER_SESSION_BID,
        "deputados": len(summary),
        "substituicoes": len(alteracoes),
    }
    (SITE_DATA / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"wrote {len(summary)} deputados to {SITE_DATA}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
