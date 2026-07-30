#!/usr/bin/env python3
"""Snapshot VIBench provider documentation URLs into local evidence artifacts.

This script archives the current HTTP response body for every URL in
`benchmark/vibench/evidence/provider_urls.txt` and records a manifest with
status, content type, fetch time, and file checksums. The goal is to preserve a
local archival artifact even when vendor documentation later changes or becomes
unavailable.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import mimetypes
import re
import shutil
import subprocess
import zlib
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


BASE_DIR = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = BASE_DIR / "benchmark" / "vibench" / "evidence"
URLS_FILE = EVIDENCE_DIR / "provider_urls.txt"
PROOF_REGISTRY_FILE = EVIDENCE_DIR / "registry" / "proofs.jsonl"
SNAPSHOT_DIR = EVIDENCE_DIR / "snapshots"
GENERATED_DIR = EVIDENCE_DIR / "generated"
MANIFEST_FILE = GENERATED_DIR / "provider_doc_snapshots.json"
SUMMARY_FILE = GENERATED_DIR / "provider_doc_snapshots_summary.json"
CHROME_BIN = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
BROWSER_FALLBACK_DOMAINS = {"ai.google.dev", "platform.openai.com", "developers.openai.com"}

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
)

try:
    import brotli  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    brotli = None


def _slugify(url: str) -> str:
    parsed = urlparse(url)
    raw = f"{parsed.netloc}_{parsed.path}_{parsed.query}"
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", raw).strip("_").lower()
    cleaned = re.sub(r"_+", "_", cleaned)
    return cleaned[:96] or "root"


def _slugify_path(url: str) -> str:
    parsed = urlparse(url)
    raw = f"{parsed.path}_{parsed.query}"
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", raw).strip("_").lower()
    cleaned = re.sub(r"_+", "_", cleaned)
    return cleaned[:96] or "root"


def _safe_domain(url: str) -> str:
    netloc = urlparse(url).netloc.strip().lower()
    cleaned = re.sub(r"[^a-z0-9.-]+", "_", netloc).strip("_")
    return cleaned or "unknown-domain"


def _extension_for(content_type: str, url: str) -> str:
    content_type = (content_type or "").split(";", 1)[0].strip().lower()
    mapping = {
        "text/html": ".html",
        "application/xhtml+xml": ".html",
        "application/json": ".json",
        "text/plain": ".txt",
        "text/markdown": ".md",
        "application/pdf": ".pdf",
        "application/xml": ".xml",
        "text/xml": ".xml",
    }
    if content_type in mapping:
        return mapping[content_type]
    guessed, _ = mimetypes.guess_type(url)
    if guessed in mapping:
        return mapping[guessed]
    suffix = Path(urlparse(url).path).suffix
    if suffix:
        return suffix[:10]
    return ".bin"


def _extract_canonical_url(page: str, default: str) -> str:
    match = re.search(
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
        page,
        re.IGNORECASE,
    )
    if match:
        return match.group(1).strip()
    og_match = re.search(
        r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']',
        page,
        re.IGNORECASE,
    )
    if og_match:
        return og_match.group(1).strip()
    return default


def _decode_body(body: bytes, headers: dict[str, str]) -> bytes:
    encoding = (headers.get("content-encoding") or "").lower()
    if not encoding:
        return body
    try:
        if "gzip" in encoding:
            return gzip.decompress(body)
        if "deflate" in encoding:
            try:
                return zlib.decompress(body)
            except zlib.error:
                return zlib.decompress(body, -zlib.MAX_WBITS)
        if "br" in encoding and brotli is not None:
            return brotli.decompress(body)
    except Exception:
        return body
    return body


def _fetch_with_headless_chrome(url: str, timeout: float) -> tuple[int, dict[str, str], bytes, str] | None:
    if not CHROME_BIN.exists() or urlparse(url).netloc not in BROWSER_FALLBACK_DOMAINS:
        return None
    try:
        completed = subprocess.run(
            [str(CHROME_BIN), "--headless=new", "--disable-gpu", "--dump-dom", url],
            capture_output=True,
            timeout=timeout,
            check=True,
        )
    except Exception:
        return None
    body = completed.stdout or b""
    if not body.lstrip().startswith(b"<"):
        return None
    page = body.decode("utf-8", errors="replace")
    final_url = _extract_canonical_url(page, default=url)
    headers = {
        "content-type": "text/html; charset=utf-8",
        "x-snapshot-method": "headless_chrome_dump_dom",
    }
    return 200, headers, body, final_url


def _fetch(url: str, timeout: float) -> tuple[int | str, dict[str, str], bytes, str]:
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
            body = resp.read()
            headers = {key.lower(): value for key, value in resp.headers.items()}
            body = _decode_body(body, headers)
            status = resp.getcode()
            final_url = resp.geturl()
            if status != 200:
                fallback = _fetch_with_headless_chrome(url, timeout=timeout)
                if fallback is not None:
                    return fallback
            return status, headers, body, final_url
    except HTTPError as exc:
        body = exc.read() or b""
        headers = {key.lower(): value for key, value in exc.headers.items()} if exc.headers else {}
        body = _decode_body(body, headers)
        fallback = _fetch_with_headless_chrome(url, timeout=timeout)
        if fallback is not None:
            return fallback
        return exc.code, headers, body, exc.geturl() or url
    except URLError as exc:
        body = str(exc).encode("utf-8")
        fallback = _fetch_with_headless_chrome(url, timeout=timeout)
        if fallback is not None:
            return fallback
        return "URLERR", {}, body, url


def _load_proof_id_map() -> dict[str, str]:
    if not PROOF_REGISTRY_FILE.exists():
        return {}
    proof_ids = {}
    for line in PROOF_REGISTRY_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        url = str(row.get("url", "")).strip()
        proof_id = str(row.get("proof_id", "")).strip()
        if url and proof_id:
            proof_ids[url] = proof_id
    return proof_ids


def snapshot_urls(urls: list[str], snapshot_dir: Path, timeout: float, proof_ids: dict[str, str]) -> tuple[list[dict], dict]:
    if snapshot_dir.exists():
        shutil.rmtree(snapshot_dir)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    status_counts: Counter[str] = Counter()

    for index, url in enumerate(urls, start=1):
        fetched_at = datetime.now(timezone.utc).isoformat()
        status, headers, body, final_url = _fetch(url, timeout=timeout)
        content_type = headers.get("content-type", "")
        ext = _extension_for(content_type, final_url or url)
        domain_dir = snapshot_dir / _safe_domain(url)
        domain_dir.mkdir(parents=True, exist_ok=True)
        name = f"{index:03d}_{hashlib.sha1(url.encode('utf-8')).hexdigest()[:12]}_{_slugify_path(url)}{ext}"
        path = domain_dir / name
        path.write_bytes(body)
        sha256 = hashlib.sha256(body).hexdigest()
        status_key = str(status)
        status_counts[status_key] += 1
        manifest.append(
            {
                "index": index,
                "proof_id": proof_ids.get(url),
                "url": url,
                "final_url": final_url,
                "fetched_at_utc": fetched_at,
                "http_status": status,
                "content_type": content_type or None,
                "content_length": len(body),
                "sha256": sha256,
                "snapshot_relpath": str(path.relative_to(EVIDENCE_DIR)),
                "snapshot_filename": name,
                "user_agent": USER_AGENT,
                "capture_method": headers.get("x-snapshot-method", "http_fetch"),
            }
        )

    summary = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "snapshot_count": len(manifest),
        "status_counts": dict(sorted(status_counts.items())),
    }
    return manifest, summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Snapshot VIBench provider documentation pages")
    parser.add_argument("--urls-file", type=Path, default=URLS_FILE)
    parser.add_argument("--snapshot-dir", type=Path, default=SNAPSHOT_DIR)
    parser.add_argument("--manifest-out", type=Path, default=MANIFEST_FILE)
    parser.add_argument("--summary-out", type=Path, default=SUMMARY_FILE)
    parser.add_argument("--timeout", type=float, default=25.0)
    args = parser.parse_args()

    urls = [line.strip() for line in args.urls_file.read_text().splitlines() if line.strip()]
    proof_ids = _load_proof_id_map()
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    manifest, summary = snapshot_urls(
        urls,
        args.snapshot_dir,
        timeout=args.timeout,
        proof_ids=proof_ids,
    )

    args.manifest_out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    args.summary_out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
