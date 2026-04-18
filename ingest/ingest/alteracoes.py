from __future__ import annotations

import re
from dataclasses import dataclass

from .fetch import BASE_URL, fetch


@dataclass
class Alteracao:
    data: str
    substituido: str
    substituto: str
    circulo: str
    gp: str
    motivo: str


_TOKEN = re.compile(
    r'lblData"[^>]*>(\d{4}-\d{2}-\d{2})</span>'
    r"|"
    r'lblSubstituicao"[^>]*>Substitui[çc][ãa]o de ([^,]+), por ([^,]+), Deputado\(a\) por ([^,]+), Grupo Parlamentar do ([^,]+), pelo motivo de: ([^<]+)</span>'
)


def alteracoes_url() -> str:
    return f"{BASE_URL}/DeputadoGP/Paginas/AlteracoesComposicaoPlenario.aspx"


def parse_alteracoes(html: str) -> list[Alteracao]:
    events: list[Alteracao] = []
    current_date: str | None = None
    for m in _TOKEN.finditer(html):
        if m.group(1):
            current_date = m.group(1)
            continue
        if current_date is None:
            continue
        events.append(
            Alteracao(
                data=current_date,
                substituido=m.group(2).strip(),
                substituto=m.group(3).strip(),
                circulo=m.group(4).strip(),
                gp=m.group(5).strip(),
                motivo=m.group(6).strip(),
            )
        )
    return events


def fetch_alteracoes() -> list[Alteracao]:
    return parse_alteracoes(fetch(alteracoes_url()))
