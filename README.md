# faltas-parlamentares

Site público, em português europeu, que acompanha as ausências dos deputados da Assembleia da República na XVII Legislatura (em curso).

Os dados vêm das páginas oficiais de [presenças em reuniões plenárias](https://www.parlamento.pt/DeputadoGP/Paginas/reunioesplenarias.aspx) publicadas pelo Parlamento (uma por deputado), complementadas pelo [portal de dados abertos](https://www.parlamento.pt/Cidadania/paginas/dadosabertos.aspx) para metadados.

## Estrutura

- `ingest/` — pipeline em Python que faz scraping das páginas "Presenças às Reuniões Plenárias" do Parlamento e escreve JSON para o site.
- `site/` — site estático em [Astro](https://astro.build), gerado a partir dos JSON do `ingest/`.
- `.github/workflows/` — cron diário que volta a correr o `ingest` e publica.

## Desenvolvimento

```bash
# Ingest (Python)
cd ingest
uv sync
uv run python -m ingest.main

# Site (Astro)
cd site
pnpm install
pnpm dev
```

## Limitações

As presenças são lidas diretamente das páginas oficiais do Parlamento, que classificam cada reunião plenária em **Presença (P)**, **Falta Justificada (FJ)**, **Falta Injustificada (FI)** ou **Ausência em Missão Parlamentar (AMP)**. Não cobrem presenças em comissões parlamentares. Ver `metodologia` no site para o detalhe.
