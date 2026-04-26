from __future__ import annotations

import re
from dataclasses import dataclass

STATUS_CODES = {
    "Presença (P)": "P",
    "Falta Justificada (FJ)": "FJ",
    "Falta Injustificada (FI)": "FI",
    "Ausência em Missão Parlamentar (AMP)": "AMP",
    "Falta ao Quórum de Votação": "FQV",
    "Presença Noutro Órgão (PNO)": "PNO",
    "Falta": "F",
}


@dataclass
class RosterEntry:
    bid: int
    name: str
    party: str
    status: str
    motivo: str


@dataclass
class AttendanceEntry:
    session_bid: int
    date: str
    status: str


ROSTER_ROW = re.compile(
    r'Biografia\.aspx\?BID=(\d+)"[^>]*>([^<]+)</a>'
    r'.*?lblGP"[^>]*>([^<]*)</span>'
    r'.*?lblPresenca"[^>]*>([^<]*)</span>'
    r'.*?lblMotivo"[^>]*>([^<]*)</span>',
    re.DOTALL,
)


ATTENDANCE_ROW = re.compile(
    r'DetalheReuniaoPlenaria\.aspx\?BID=(\d+)"[^>]*>(\d{4}-\d{2}-\d{2})</a>'
    r'.*?lblPresenca"[^>]*>([^<]*)</span>',
    re.DOTALL,
)


def parse_session_roster(html: str) -> list[RosterEntry]:
    rows = []
    for m in ROSTER_ROW.finditer(html):
        bid, name, party, status, motivo = m.groups()
        rows.append(
            RosterEntry(
                bid=int(bid),
                name=name.strip(),
                party=party.strip(),
                status=status.strip(),
                motivo=motivo.strip(),
            )
        )
    return rows


def parse_attendance(html: str) -> list[AttendanceEntry]:
    rows = []
    for m in ATTENDANCE_ROW.finditer(html):
        bid, date, status = m.groups()
        rows.append(
            AttendanceEntry(
                session_bid=int(bid),
                date=date,
                status=status.strip(),
            )
        )
    return rows
