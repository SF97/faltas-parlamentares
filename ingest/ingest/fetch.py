from __future__ import annotations

import hashlib
import os
import time
from pathlib import Path

import httpx

CACHE_DIR = Path(__file__).resolve().parents[1] / ".cache" / "http"
NO_CACHE = os.environ.get("FALTAS_NO_CACHE") == "1"
BASE_URL = "https://www.parlamento.pt"
HEADERS = {
    "User-Agent": "faltas-parlamentares-ingest (+https://github.com/SF97/faltas-parlamentares)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Accept-Language": "pt-PT,pt;q=0.9,en;q=0.8",
}

_client: httpx.Client | None = None


def client() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(headers=HEADERS, timeout=60.0, follow_redirects=True)
    return _client


def fetch(url: str, *, cache: bool = True) -> str:
    use_cache = cache and not NO_CACHE
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(url.encode()).hexdigest()[:20]
    cached = CACHE_DIR / f"{key}.html"
    if use_cache and cached.exists():
        return cached.read_text(encoding="utf-8")

    attempts = 6
    for attempt in range(attempts):
        try:
            r = client().get(url)
            r.raise_for_status()
            text = r.text
            cached.write_text(text, encoding="utf-8")
            return text
        except httpx.HTTPError:
            if attempt == attempts - 1:
                raise
            time.sleep(min(30, 2**attempt))
    raise RuntimeError("unreachable")
