#!/usr/bin/env python3
"""Assess the quality of saved provider-doc snapshots.

This checks whether each archived response body looks like a usable provider
documentation page rather than a generic shell, access wall, or error page.
"""

from __future__ import annotations

import argparse
import gzip
import html
import json
import re
import zlib
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


BASE_DIR = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = BASE_DIR / "benchmark" / "vibench" / "evidence"
GENERATED_DIR = EVIDENCE_DIR / "generated"
MANIFEST_FILE = GENERATED_DIR / "provider_doc_snapshots.json"
QUALITY_FILE = GENERATED_DIR / "provider_doc_snapshot_quality.json"
QUALITY_SUMMARY_FILE = GENERATED_DIR / "provider_doc_snapshot_quality_summary.json"
QUALITY_REPORT_FILE = GENERATED_DIR / "provider_doc_snapshot_quality_report.md"

GENERIC_TITLES = {
    "ibm cloud docs",
    "ibm documentation",
    "documentation",
    "docs",
}

STRONG_FAILURE_PHRASES = [
    "page not found",
    "access denied",
    "forbidden",
    "redirecting",
    "just a moment",
    "verify you are human",
    "you need to enable javascript",
    "enable javascript to run this app",
    "service unavailable",
    "internal server error",
    "application error",
    "temporarily unavailable",
    "request blocked",
]

TOKEN_STOPWORDS = {
    "alibaba",
    "alibabacloud",
    "api",
    "apis",
    "amazon",
    "amazonaws",
    "com",
    "cloud",
    "datadog",
    "datadoghq",
    "developer",
    "developers",
    "dev",
    "detail",
    "doc",
    "docs",
    "documentation",
    "en",
    "help",
    "html",
    "http",
    "https",
    "ibm",
    "index",
    "latest",
    "microsoft",
    "overview",
    "openai",
    "product",
    "products",
    "reference",
    "rest",
    "topic",
    "topics",
    "us",
    "v1",
    "v2",
    "v3",
    "what",
    "www",
}

try:
    import brotli  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    brotli = None


class _VisibleTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        cleaned = re.sub(r"\s+", " ", data).strip()
        if cleaned:
            self._parts.append(cleaned)

    def get_text(self) -> str:
        return " ".join(self._parts)


def _extract_tag_text(page: str, tag: str) -> str:
    match = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", page, re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    inner = re.sub(r"<[^>]+>", " ", match.group(1))
    return re.sub(r"\s+", " ", html.unescape(inner)).strip()


def _extract_embedded_aws_landing_tag(page: str, tag: str) -> str:
    match = re.search(r'id=["\']landing-page-xml["\'][^>]*value=["\']([^"\']+)["\']', page, re.IGNORECASE)
    if not match:
        return ""
    decoded = unquote(match.group(1))
    return _extract_tag_text(decoded, tag)


def _extract_visible_text(page: str) -> str:
    parser = _VisibleTextExtractor()
    parser.feed(page)
    text = parser.get_text()
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def _extract_tokens(text: str) -> set[str]:
    tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in TOKEN_STOPWORDS and (len(token) >= 4 or token in {"s3", "kms", "ocr", "oidc"})
    }
    return tokens


def _url_tokens(url: str) -> set[str]:
    parsed = urlparse(url)
    raw = "_".join([parsed.netloc, unquote(parsed.path), unquote(parsed.query)])
    return _extract_tokens(raw)


def _read_snapshot_text(snapshot_path: Path) -> str:
    raw_bytes = snapshot_path.read_bytes()
    if raw_bytes.startswith(b"\x1f\x8b"):
        try:
            raw_bytes = gzip.decompress(raw_bytes)
        except Exception:
            pass
    elif brotli is not None:
        try:
            raw_bytes = brotli.decompress(raw_bytes)
        except Exception:
            pass
    else:
        try:
            raw_bytes = zlib.decompress(raw_bytes)
        except Exception:
            pass
    return raw_bytes.decode("utf-8", errors="replace")


def assess_snapshot(entry: dict, evidence_dir: Path) -> dict:
    snapshot_path = evidence_dir / entry["snapshot_relpath"]
    raw = _read_snapshot_text(snapshot_path)
    title = _extract_tag_text(raw, "title")
    embedded_title = ""
    if not title:
        embedded_title = _extract_embedded_aws_landing_tag(raw, "title")
        title = embedded_title or title
    h1 = _extract_tag_text(raw, "h1")
    if not h1:
        h1 = _extract_embedded_aws_landing_tag(raw, "titleabbrev") or h1
    visible_text = _extract_visible_text(raw)
    visible_head = visible_text[:4000]
    visible_excerpt = visible_text[:320]
    lower_head = visible_head.lower()
    lower_title = title.lower()
    lower_h1 = h1.lower()

    url_tokens = _url_tokens(entry["url"])
    heading_tokens = _extract_tokens(" ".join(part for part in [title, h1] if part))
    visible_tokens = _extract_tokens(visible_head)

    overlap_title = sorted(url_tokens & heading_tokens)
    overlap_visible = sorted(url_tokens & visible_tokens)

    flags: list[str] = []
    failure_hits = [phrase for phrase in STRONG_FAILURE_PHRASES if phrase in lower_head or phrase in lower_title or phrase in lower_h1]
    http_status = str(entry.get("http_status", ""))

    if not title:
        flags.append("missing_title")
    elif lower_title in GENERIC_TITLES:
        flags.append("generic_title")
    if not h1:
        flags.append("missing_h1")
    elif lower_h1 in GENERIC_TITLES:
        flags.append("generic_h1")
    if len(visible_text.split()) < 80:
        flags.append("minimal_visible_text")
    normalized_url = (entry.get("url") or "").rstrip("/")
    normalized_final_url = (entry.get("final_url") or "").rstrip("/")
    if url_tokens and not overlap_title and not overlap_visible:
        flags.append("low_url_token_overlap")
    if embedded_title:
        flags.append("embedded_title")
    if normalized_final_url and normalized_final_url != normalized_url:
        flags.append("redirected_snapshot")
    if http_status and http_status != "200":
        flags.append(f"non_200_status:{http_status}")
    if re.search(r"<meta[^>]+http-equiv=[\"']refresh[\"']", raw, re.IGNORECASE):
        flags.append("meta_refresh_redirect")
    if title.lower().startswith("404"):
        flags.append("failure_phrase:title_404")
    for hit in failure_hits:
        flags.append(f"failure_phrase:{hit}")

    specific_heading = bool(title and lower_title not in GENERIC_TITLES) or bool(h1 and lower_h1 not in GENERIC_TITLES)
    usable_overlap = bool(overlap_title or overlap_visible)

    soft_review_flags = {"missing_h1", "low_url_token_overlap", "redirected_snapshot"}
    if http_status and http_status != "200":
        quality = "weak"
    elif lower_title == "redirecting..." or lower_h1 == "redirecting...":
        quality = "weak"
    elif failure_hits and not specific_heading:
        quality = "weak"
    elif "failure_phrase:title_404" in flags:
        quality = "weak"
    elif "generic_title" in flags and "missing_h1" in flags and not usable_overlap:
        quality = "weak"
    elif "meta_refresh_redirect" in flags and not specific_heading:
        quality = "weak"
    elif "minimal_visible_text" in flags and not specific_heading:
        quality = "weak"
    elif specific_heading and usable_overlap and not failure_hits:
        quality = "good"
    elif specific_heading and not failure_hits and len(visible_text.split()) >= 120 and set(flags).issubset(soft_review_flags):
        quality = "good"
    else:
        quality = "review"

    return {
        "index": entry["index"],
        "proof_id": entry.get("proof_id"),
        "url": entry["url"],
        "final_url": entry.get("final_url"),
        "domain": urlparse(entry["url"]).netloc,
        "snapshot_relpath": entry["snapshot_relpath"],
        "http_status": entry.get("http_status"),
        "content_length": entry.get("content_length"),
        "title": title or None,
        "h1": h1 or None,
        "visible_word_count": len(visible_text.split()),
        "url_token_overlap_title": overlap_title,
        "url_token_overlap_visible": overlap_visible[:20],
        "flags": flags,
        "quality": quality,
        "visible_excerpt": visible_excerpt,
    }


def build_report(summary: dict, records: list[dict]) -> str:
    lines = [
        "# Provider Doc Snapshot Quality",
        "",
        f"- Snapshot count: `{summary['snapshot_count']}`",
        f"- Quality counts: `{summary['quality_counts']}`",
        f"- Weak count: `{summary['weak_count']}`",
        f"- Review count: `{summary['review_count']}`",
        "",
        "## Weak Snapshots",
        "",
    ]
    weak = [record for record in records if record["quality"] == "weak"]
    if not weak:
        lines.append("- None")
    else:
        for record in weak:
            lines.append(
                f"- `{record['index']:03d}` `{record['domain']}`: "
                f"`{record['title'] or 'NO TITLE'}` | flags={record['flags']} | `{record['url']}`"
            )

    lines.extend(["", "## Review Snapshots", ""])
    review = [record for record in records if record["quality"] == "review"]
    if not review:
        lines.append("- None")
    else:
        for record in review:
            lines.append(
                f"- `{record['index']:03d}` `{record['domain']}`: "
                f"`{record['title'] or 'NO TITLE'}` | flags={record['flags']} | `{record['url']}`"
            )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Assess saved provider-doc snapshot quality")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_FILE)
    parser.add_argument("--quality-out", type=Path, default=QUALITY_FILE)
    parser.add_argument("--summary-out", type=Path, default=QUALITY_SUMMARY_FILE)
    parser.add_argument("--report-out", type=Path, default=QUALITY_REPORT_FILE)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    records = [assess_snapshot(entry, EVIDENCE_DIR) for entry in manifest]
    quality_counts = Counter(record["quality"] for record in records)
    weak_records = [record for record in records if record["quality"] == "weak"]
    review_records = [record for record in records if record["quality"] == "review"]

    summary = {
        "audited_at_utc": manifest[0]["fetched_at_utc"] if manifest else None,
        "snapshot_count": len(records),
        "quality_counts": dict(sorted(quality_counts.items())),
        "weak_count": len(weak_records),
        "review_count": len(review_records),
        "weak_urls": [record["url"] for record in weak_records],
        "review_urls": [record["url"] for record in review_records],
    }

    args.quality_out.parent.mkdir(parents=True, exist_ok=True)
    args.summary_out.parent.mkdir(parents=True, exist_ok=True)
    args.report_out.parent.mkdir(parents=True, exist_ok=True)
    args.quality_out.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.summary_out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.report_out.write_text(build_report(summary, records), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
