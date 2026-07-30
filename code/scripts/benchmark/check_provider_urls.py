#!/usr/bin/env python3
"""Check current reachability of VIBench provider documentation URLs."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_DIR = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = BASE_DIR / "benchmark" / "vibench" / "evidence"
GENERATED_DIR = EVIDENCE_DIR / "generated"
URLS_FILE = EVIDENCE_DIR / "provider_urls.txt"
TSV_OUT = GENERATED_DIR / "provider_url_check.tsv"
SUMMARY_OUT = GENERATED_DIR / "provider_url_check_summary.json"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
)


def fetch_status(url: str, timeout: float) -> str:
    req = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "identity",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            return str(resp.getcode())
    except HTTPError as exc:
        return str(exc.code)
    except URLError:
        return "URLERR"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--urls-file", type=Path, default=URLS_FILE)
    parser.add_argument("--tsv-out", type=Path, default=TSV_OUT)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_OUT)
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args()

    urls = [line.strip() for line in args.urls_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    args.tsv_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)

    counts: Counter[str] = Counter()
    rows: list[tuple[str, str]] = []
    for url in urls:
        status = fetch_status(url, timeout=args.timeout)
        counts[status] += 1
        rows.append((status, url))

    args.tsv_out.write_text(
        "".join(f"{status}\t{url}\n" for status, url in rows),
        encoding="utf-8",
    )
    args.summary_out.write_text(
        json.dumps(dict(sorted(counts.items())), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(dict(sorted(counts.items())), indent=2))


if __name__ == "__main__":
    main()
