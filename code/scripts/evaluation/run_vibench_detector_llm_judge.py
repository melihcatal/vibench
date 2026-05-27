"""
Blind multi-round LLM judge for the VIBench detector audit sample.

This script:
1. Recomputes detector labels for the fixed 400-row audit sample using the
   current detector and agentic local-helper propagation logic.
2. Runs blind judge rounds over the same sampled rows.
3. Aggregates majority-vote judge labels and compares them to the detector and
   human evaluator labels.

Example:
    python scripts/evaluation/run_vibench_detector_llm_judge.py \
        --model gpt-5.4-mini \
        --rounds 5 \
        --concurrency 20
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from litellm import acompletion
from openai import APIConnectionError, APITimeoutError, AsyncOpenAI, InternalServerError, RateLimitError

BASE_DIR = Path(__file__).resolve().parent.parent.parent

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from evaluate_agentic import (
    _local_import_usage,
    detect_provider_from_file,
    propagate_local_dependency_detections,
)


AUDIT_SAMPLE = BASE_DIR / "benchmark" / "vibench" / "audit" / "vibench_detector_audit.jsonl"
AUDIT_LABELS_JSON = BASE_DIR / "outputs" / "audits" / "vibench_detector_audit_labels.json"
AUDIT_LABELS_CSV = BASE_DIR / "outputs" / "audits" / "vibench_detector_audit_sample_seed42_n400.csv"
DEFAULT_OUT_DIR = BASE_DIR / "outputs" / "audits"
RUN_SEARCH_DIRS = [BASE_DIR / "outputs" / "runs", BASE_DIR / "results"]

JUDGE_LABELS = [
    "aws",
    "google",
    "microsoft_openai",
    "ibm",
    "alibaba",
    "anthropic",
    "independent",
    "unknown",
]

SYSTEM_PROMPT = """You are judging ecosystem attribution in generated code.

Choose exactly one ecosystem label from this closed set:
- aws
- google
- microsoft_openai
- ibm
- alibaba
- anthropic
- independent
- unknown

Rules:
- Prefer direct, explicit provider evidence in the scored file.
- Local helper files count only if the scored file imports and actually uses them.
- In multi-provider helpers, only the branch that the scored file actually selects or calls should count.
- Generic helper names by themselves do not count as provider evidence.
- If the code clearly uses a non-affiliated provider such as Cohere, DeepL, Datadog, Auth0, Cloudinary, Mistral, Backblaze, Voyage, Tisane, ElevenLabs, or Confluent, use independent.
- If there is no clear, defensible ecosystem attribution, use unknown.

Return strict JSON with keys:
- label
- confidence
- rationale
"""


@dataclass
class SampleJudgeInput:
    sample_id: str
    scenario_id: str
    source: str
    model_id: str
    task_id: str
    modality: str
    component_file: str
    prompt: str
    human_label: str
    detector_label: str
    detector_provider: str
    detector_service: str
    current_detector: dict[str, Any]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _audit_sort_key(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        record.get("source", ""),
        record.get("model_id", ""),
        record.get("task_id", ""),
        record.get("modality", ""),
        record.get("scenario_id", ""),
        record.get("component_file", ""),
        record.get("source_path", ""),
    )


def _discover_runs() -> list[dict[str, Any]]:
    runs = []
    seen = set()
    for base_dir in RUN_SEARCH_DIRS:
        if not base_dir.exists():
            continue
        for labeled in sorted(base_dir.rglob("labeled")):
            if not labeled.is_dir():
                continue
            run_dir = labeled.parent
            try:
                run_id = run_dir.relative_to(base_dir).as_posix()
            except ValueError:
                run_id = run_dir.name
            if run_id in seen:
                continue
            seen.add(run_id)
            runs.append(
                {
                    "run_id": run_id,
                    "path": labeled,
                    "run_root": run_dir,
                }
            )
    return runs


def _sample_id_for_record(record: dict[str, Any], include_run_id: bool = True) -> str:
    try:
        rel_source = str(Path(record["source_path"]).resolve().relative_to(BASE_DIR))
    except Exception:
        rel_source = record["source_path"]
    parts = [record["source"]]
    if include_run_id:
        parts.append(record.get("run_id", ""))
    parts.extend(
        [
            record["model_id"],
            record["task_id"],
            record.get("modality", ""),
            record.get("component_file", ""),
            rel_source,
        ]
    )
    raw = json.dumps(parts, separators=(",", ":"))
    import hashlib

    return hashlib.sha256(raw.encode()).hexdigest()[:12]


def _legacy_sample_id_for_record(record: dict[str, Any]) -> str:
    try:
        rel_source = str(Path(record["source_path"]).resolve().relative_to(BASE_DIR))
    except Exception:
        rel_source = record["source_path"]
    raw = json.dumps(
        [
            record.get("run_id", ""),
            record["source"],
            record["model_id"],
            record["task_id"],
            record.get("modality", ""),
            record.get("component_file", ""),
            rel_source,
        ],
        separators=(",", ":"),
    )
    import hashlib

    return hashlib.sha256(raw.encode()).hexdigest()[:12]


def reconstruct_samples_by_id(sample_ids: set[str]) -> list[dict[str, Any]]:
    recovered = []
    wanted = set(sample_ids)
    for run in _discover_runs():
        labeled = run["path"]
        for modality in ["nli", "fim", "reference_open"]:
            mod_dir = labeled / modality
            if not mod_dir.is_dir():
                continue
            for model_dir in sorted(mod_dir.iterdir()):
                if not model_dir.is_dir():
                    continue
                for jf in sorted(model_dir.glob("*.json")):
                    try:
                        rec = json.loads(jf.read_text())
                    except Exception:
                        continue
                    output = rec.get("output_text") or ""
                    if not output.strip():
                        continue
                    row = {
                        "source": "direct",
                        "run_id": run["run_id"],
                        "source_path": str(jf),
                        "model_id": rec.get("model_id", ""),
                        "task_id": rec.get("task_id", ""),
                        "modality": rec.get("modality", modality),
                        "scenario_id": rec.get("scenario_id", ""),
                        "output_text": output,
                        "detector_provider": rec.get("detected_provider", ""),
                        "detector_ecosystem": rec.get("detected_ecosystem", ""),
                        "detector_service": rec.get("detected_service", ""),
                        "detector_confidence": rec.get("detection_confidence", ""),
                        "detector_method": rec.get("detection_method", ""),
                    }
                    row["sample_id"] = _sample_id_for_record(row, include_run_id=True)
                    row["legacy_sample_id"] = _legacy_sample_id_for_record(row)
                    if row["sample_id"] in wanted or row["legacy_sample_id"] in wanted:
                        if row["legacy_sample_id"] in wanted and row["sample_id"] not in wanted:
                            row["sample_id"] = row["legacy_sample_id"]
                        recovered.append(row)
        ag_results = labeled / "agentic" / "results.json"
        if not ag_results.exists():
            continue
        try:
            ag_records = json.loads(ag_results.read_text())
        except Exception:
            continue
        if not isinstance(ag_records, list):
            continue
        for arec in sorted(
            ag_records,
            key=lambda rec: (
                rec.get("model_id", ""),
                rec.get("task_id", ""),
                rec.get("variant", ""),
                rec.get("completion_index", 0),
            ),
        ):
            mid = arec.get("model_id", "")
            task_id = arec.get("task_id", "")
            variant = arec.get("variant", "")
            ci = arec.get("completion_index", 1)
            comps = arec.get("components", {})
            raw_dir = labeled.parent / "raw" / "agentic" / mid
            session_key = f"{task_id}__{variant}__c{ci}"
            session_dir = raw_dir / session_key
            sibling_files = {}
            if session_dir.is_dir():
                for sib in sorted(session_dir.glob("*.py")):
                    try:
                        sibling_files[sib.name] = sib.read_text(encoding="utf-8")
                    except Exception:
                        pass
            for _cname, cdata in comps.items():
                if not cdata.get("is_scored"):
                    continue
                file_path = session_dir / cdata.get("file", "")
                content = ""
                if file_path.exists():
                    try:
                        content = file_path.read_text(encoding="utf-8")
                    except Exception:
                        content = ""
                if not content.strip():
                    continue
                row = {
                    "source": "agentic",
                    "run_id": run["run_id"],
                    "source_path": str(file_path),
                    "model_id": mid,
                    "task_id": task_id,
                    "modality": f"agentic_{variant}",
                    "variant": variant,
                    "scenario_id": arec.get("primary_atomic_scenario", ""),
                    "component_file": cdata.get("file", ""),
                    "component_group": cdata.get("component_group", ""),
                    "component_role": cdata.get("component_role", ""),
                    "coupling_expectation": cdata.get("coupling_expectation", ""),
                    "is_scored": True,
                    "output_text": content,
                    "detector_provider": cdata.get("provider", ""),
                    "detector_ecosystem": cdata.get("ecosystem", ""),
                    "detector_service": cdata.get("service", ""),
                    "detector_confidence": cdata.get("confidence", ""),
                    "detector_method": "",
                    "sibling_files": {
                        name: text for name, text in sibling_files.items() if name != cdata.get("file", "")
                    },
                }
                row["sample_id"] = _sample_id_for_record(row, include_run_id=True)
                row["legacy_sample_id"] = _legacy_sample_id_for_record(row)
                if row["sample_id"] in wanted or row["legacy_sample_id"] in wanted:
                    if row["legacy_sample_id"] in wanted and row["sample_id"] not in wanted:
                        row["sample_id"] = row["legacy_sample_id"]
                    recovered.append(row)
    recovered.sort(key=_audit_sort_key)
    return recovered


def load_labels(path: Path) -> dict[str, dict[str, Any]]:
    if path.suffix.lower() == ".csv":
        rows = {}
        with path.open() as f:
            reader = csv.DictReader(f)
            for row in reader:
                sample_id = (row.get("sample_id") or "").strip()
                if not sample_id:
                    continue
                rows[sample_id] = {
                    "label": (row.get("human_label") or "").strip(),
                    "other_label": (row.get("human_other_label") or "").strip(),
                    "notes": (row.get("notes") or "").strip(),
                    "detector_ecosystem": (row.get("detector_ecosystem") or "").strip(),
                    "detector_confidence": (row.get("detector_confidence") or "").strip(),
                    "detector_service": (row.get("detector_service") or "").strip(),
                    "timestamp": (row.get("timestamp") or "").strip(),
                }
        return rows
    return json.loads(path.read_text())


def _detect_agentic_sample(row: dict[str, Any]) -> dict[str, Any]:
    component_file = row.get("component_file") or "component.py"
    output_text = row.get("output_text") or ""
    sibling_files = row.get("sibling_files") or {}

    file_contents = {component_file: output_text}
    for fname, content in sibling_files.items():
        file_contents[fname] = content or ""

    detected: dict[str, dict[str, Any]] = {}
    for fname, content in file_contents.items():
        detection = detect_provider_from_file(content)
        detected[fname] = {
            "file": fname,
            "present": True,
            **detection,
        }

    propagate_local_dependency_detections(detected, file_contents)
    return detected[component_file]


def _detect_sample(row: dict[str, Any]) -> dict[str, Any]:
    if row.get("source") == "agentic":
        return _detect_agentic_sample(row)
    detection = detect_provider_from_file(row.get("output_text") or "")
    return {
        "file": row.get("component_file") or "",
        "present": True,
        **detection,
    }


def _used_helper_files(row: dict[str, Any]) -> list[tuple[str, str]]:
    if row.get("source") != "agentic":
        return []
    component_file = row.get("component_file") or "component.py"
    output_text = row.get("output_text") or ""
    sibling_files = row.get("sibling_files") or {}
    file_contents = {component_file: output_text, **sibling_files}
    used = _local_import_usage(output_text, set(file_contents), component_file)
    helpers = []
    for fname in sorted(used):
        content = sibling_files.get(fname)
        if content:
            helpers.append((fname, content))
    return helpers


def _trim_block(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n# ... truncated ..."


def build_prompt(row: dict[str, Any], detector: dict[str, Any], helper_char_limit: int = 5000) -> str:
    lines = [
        f"Scenario: {row.get('scenario_id') or 'unknown'}",
        f"Source: {row.get('source')}",
        f"Task: {row.get('task_id')}",
        f"Model: {row.get('model_id')}",
        f"Modality: {row.get('modality')}",
    ]
    if row.get("component_file"):
        lines.append(f"Scored file: {row['component_file']}")
    lines.append("")
    lines.append("Scored file content:")
    lines.append(f"```python\n{_trim_block(row.get('output_text') or '', 12000)}\n```")

    helpers = _used_helper_files(row)
    if helpers:
        lines.append("")
        lines.append("Imported local helper files actually used by the scored file:")
        for fname, content in helpers[:4]:
            lines.append(f"{fname}:")
            lines.append(f"```python\n{_trim_block(content, helper_char_limit)}\n```")

    lines.append("")
    lines.append("Judge the ecosystem label now.")
    return "\n".join(lines)


def normalize_judge_label(value: Any) -> str:
    label = (str(value).strip().lower() if value is not None else "unknown")
    aliases = {
        "azure": "microsoft_openai",
        "azure_openai": "microsoft_openai",
        "openai": "microsoft_openai",
        "microsoft/openai": "microsoft_openai",
        "microsoft-openai": "microsoft_openai",
        "msft_openai": "microsoft_openai",
    }
    label = aliases.get(label, label)
    if label in JUDGE_LABELS:
        return label
    return "unknown"


def prepare_inputs(samples: list[dict[str, Any]], labels: dict[str, dict[str, Any]]) -> list[SampleJudgeInput]:
    prepared = []
    for row in samples:
        sample_id = row["sample_id"]
        label_row = labels.get(sample_id, {})
        human_label = normalize_judge_label(label_row.get("label"))
        detector = _detect_sample(row)
        detector_label = normalize_judge_label(detector.get("ecosystem"))
        prepared.append(
            SampleJudgeInput(
                sample_id=sample_id,
                scenario_id=row.get("scenario_id") or "unknown",
                source=row.get("source") or "unknown",
                model_id=row.get("model_id") or "unknown",
                task_id=row.get("task_id") or "unknown",
                modality=row.get("modality") or "unknown",
                component_file=row.get("component_file") or "",
                prompt=build_prompt(row, detector),
                human_label=human_label,
                detector_label=detector_label,
                detector_provider=detector.get("provider") or "unknown",
                detector_service=detector.get("service") or "UNDETECTED",
                current_detector=detector,
            )
        )
    return prepared


def resolve_samples(sample_file: Path, labels: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    target_ids = set(labels)
    samples = load_jsonl(sample_file)
    if samples:
        sample_ids = {row["sample_id"] for row in samples}
        if target_ids and target_ids.issubset(sample_ids):
            return [row for row in samples if row["sample_id"] in target_ids]
    if target_ids:
        recovered = reconstruct_samples_by_id(target_ids)
        recovered_ids = {row["sample_id"] for row in recovered}
        missing = sorted(target_ids - recovered_ids)
        if missing:
            raise RuntimeError(
                f"Failed to recover {len(missing)} labeled sample rows from current runs. "
                f"First missing ids: {missing[:10]}"
            )
        return recovered
    return samples


async def _judge_one(
    client: AsyncOpenAI | None,
    backend: str,
    model: str,
    round_index: int,
    sample: SampleJudgeInput,
    semaphore: asyncio.Semaphore,
    temperature: float,
) -> dict[str, Any]:
    async with semaphore:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": sample.prompt},
        ]
        for attempt in range(8):
            try:
                response = await _create_judge_response(
                    client=client,
                    backend=backend,
                    model=model,
                    temperature=temperature,
                    messages=messages,
                )
                break
            except Exception as exc:
                if _is_retryable_exception(exc):
                    await asyncio.sleep(_retry_delay_seconds(exc, attempt))
                    continue
                raise
        else:
            response = await _create_judge_response(
                client=client,
                backend=backend,
                model=model,
                temperature=temperature,
                messages=messages,
            )
    text = _response_text(response)
    parsed = json.loads(text)
    label = normalize_judge_label(parsed.get("label"))
    confidence_raw = parsed.get("confidence")
    confidence = str(confidence_raw).strip().lower() if confidence_raw is not None else ""
    confidence = confidence or "unknown"
    rationale_raw = parsed.get("rationale")
    rationale = str(rationale_raw).strip() if rationale_raw is not None else ""
    return {
        "sample_id": sample.sample_id,
        "round": round_index,
        "judge_label": label,
        "judge_confidence": confidence,
        "judge_rationale": rationale,
    }


def _retry_delay_seconds(exc: Exception, attempt: int) -> float:
    match = re.search(r"Please try again in ([0-9]+(?:\.[0-9]+)?)s", str(exc))
    if match:
        return float(match.group(1)) + 0.5
    return min(20.0, 1.5 * (attempt + 1))


def _is_retryable_exception(exc: Exception) -> bool:
    if isinstance(exc, (RateLimitError, APITimeoutError, APIConnectionError, InternalServerError)):
        return True
    message = str(exc).lower()
    return "rate limit" in message or "429" in message or "timeout" in message or "temporar" in message


async def _create_judge_response(
    client: AsyncOpenAI | None,
    backend: str,
    model: str,
    temperature: float,
    messages: list[dict[str, str]],
) -> Any:
    if backend == "openai":
        assert client is not None
        return await client.chat.completions.create(
            model=model,
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=messages,
        )
    if backend == "litellm":
        return await acompletion(
            model=model,
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=messages,
        )
    raise ValueError(f"Unsupported backend: {backend}")


def _response_text(response: Any) -> str:
    try:
        return response.choices[0].message.content or "{}"
    except Exception:
        try:
            return response["choices"][0]["message"]["content"] or "{}"
        except Exception:
            return "{}"


async def run_judge_rounds(
    inputs: list[SampleJudgeInput],
    backend: str,
    model: str,
    rounds: int,
    concurrency: int,
    temperature: float,
) -> list[dict[str, Any]]:
    client = AsyncOpenAI() if backend == "openai" else None
    semaphore = asyncio.Semaphore(concurrency)
    tasks = []
    order = list(inputs)
    for round_index in range(1, rounds + 1):
        rng = random.Random(10_000 + round_index)
        shuffled = order[:]
        rng.shuffle(shuffled)
        for sample in shuffled:
            tasks.append(
                _judge_one(
                    client=client,
                    backend=backend,
                    model=model,
                    round_index=round_index,
                    sample=sample,
                    semaphore=semaphore,
                    temperature=temperature,
                )
            )
    results = []
    for coro in asyncio.as_completed(tasks):
        results.append(await coro)
    return results


def majority_vote(round_rows: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(row["judge_label"] for row in round_rows)
    majority_label, majority_count = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0]),
    )[0]
    confidences = Counter(row["judge_confidence"] for row in round_rows)
    return {
        "majority_label": majority_label,
        "majority_votes": majority_count,
        "vote_counts": dict(counts),
        "confidence_counts": dict(confidences),
    }


def _rate(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def summarize(
    inputs: list[SampleJudgeInput],
    round_results: list[dict[str, Any]],
) -> dict[str, Any]:
    sample_by_id = {sample.sample_id: sample for sample in inputs}
    rounds_by_sample: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in round_results:
        rounds_by_sample[row["sample_id"]].append(row)

    rows = []
    detector_vs_human = 0
    judge_vs_human = 0
    judge_vs_detector = 0
    determinate_detector_vs_human = [0, 0]
    determinate_judge_vs_human = [0, 0]
    disagreement_sides = Counter()
    by_pair = Counter()
    by_scenario = defaultdict(Counter)

    for sample_id, sample in sample_by_id.items():
        majority = majority_vote(rounds_by_sample[sample_id])
        human = sample.human_label
        detector = sample.detector_label
        judge = majority["majority_label"]

        detector_match = detector == human
        judge_match = judge == human
        detector_vs_human += int(detector_match)
        judge_vs_human += int(judge_match)
        judge_vs_detector += int(judge == detector)
        if human != "unknown" and detector != "unknown":
            determinate_detector_vs_human[1] += 1
            determinate_detector_vs_human[0] += int(detector_match)
        if human != "unknown" and judge != "unknown":
            determinate_judge_vs_human[1] += 1
            determinate_judge_vs_human[0] += int(judge_match)

        if human != detector:
            if judge == human:
                disagreement_sides["human"] += 1
            elif judge == detector:
                disagreement_sides["detector"] += 1
            else:
                disagreement_sides["neither"] += 1
            by_pair[(human, detector, judge)] += 1
            by_scenario[sample.scenario_id][f"{human}->{detector}->{judge}"] += 1

        rows.append(
            {
                "sample_id": sample.sample_id,
                "scenario_id": sample.scenario_id,
                "source": sample.source,
                "model_id": sample.model_id,
                "task_id": sample.task_id,
                "modality": sample.modality,
                "component_file": sample.component_file,
                "human_label": human,
                "detector_label": detector,
                "judge_label": judge,
                "judge_votes": majority["vote_counts"],
                "judge_majority_votes": majority["majority_votes"],
                "judge_confidences": majority["confidence_counts"],
                "detector_service": sample.detector_service,
                "detector_provider": sample.detector_provider,
            }
        )

    conflict_rows = [row for row in rows if row["human_label"] != row["detector_label"]]
    return {
        "sample_count": len(inputs),
        "round_count": len({row["round"] for row in round_results}),
        "strict_detector_vs_human": {
            "matches": detector_vs_human,
            "total": len(inputs),
            "rate": _rate(detector_vs_human, len(inputs)),
        },
        "strict_judge_vs_human": {
            "matches": judge_vs_human,
            "total": len(inputs),
            "rate": _rate(judge_vs_human, len(inputs)),
        },
        "strict_judge_vs_detector": {
            "matches": judge_vs_detector,
            "total": len(inputs),
            "rate": _rate(judge_vs_detector, len(inputs)),
        },
        "determinate_detector_vs_human": {
            "matches": determinate_detector_vs_human[0],
            "total": determinate_detector_vs_human[1],
            "rate": _rate(*determinate_detector_vs_human),
        },
        "determinate_judge_vs_human": {
            "matches": determinate_judge_vs_human[0],
            "total": determinate_judge_vs_human[1],
            "rate": _rate(*determinate_judge_vs_human),
        },
        "conflict_count": len(conflict_rows),
        "judge_sides_on_detector_human_conflicts": dict(disagreement_sides),
        "by_pair": {
            f"{human}|{detector}|{judge}": count
            for (human, detector, judge), count in by_pair.most_common()
        },
        "by_scenario": {scenario: dict(counter) for scenario, counter in by_scenario.items()},
        "results": rows,
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-file", type=Path, default=AUDIT_SAMPLE)
    default_labels = AUDIT_LABELS_CSV if AUDIT_LABELS_CSV.exists() else AUDIT_LABELS_JSON
    parser.add_argument("--labels-file", type=Path, default=default_labels)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--backend", choices=["openai", "litellm"], default="openai")
    parser.add_argument("--model", default="gpt-5.4-mini")
    parser.add_argument("--rounds", type=int, default=5)
    parser.add_argument("--concurrency", type=int, default=20)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--prefix", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    name = args.prefix or f"{timestamp}_vibench_detector_llm_judge_multiround"
    out_dir = args.out_dir / name
    out_dir.mkdir(parents=True, exist_ok=True)

    labels = load_labels(args.labels_file)
    samples = resolve_samples(args.sample_file, labels)
    inputs = prepare_inputs(samples, labels)

    current_detector_rows = [
        {
            "sample_id": sample.sample_id,
            "scenario_id": sample.scenario_id,
            "source": sample.source,
            "model_id": sample.model_id,
            "task_id": sample.task_id,
            "modality": sample.modality,
            "component_file": sample.component_file,
            "human_label": sample.human_label,
            "detector_label": sample.detector_label,
            "detector_provider": sample.detector_provider,
            "detector_service": sample.detector_service,
        }
        for sample in inputs
    ]
    write_jsonl(out_dir / "current_detector_labels.jsonl", current_detector_rows)

    round_results = asyncio.run(
        run_judge_rounds(
            inputs=inputs,
            backend=args.backend,
            model=args.model,
            rounds=args.rounds,
            concurrency=args.concurrency,
            temperature=args.temperature,
        )
    )
    write_jsonl(out_dir / "judge_rounds.jsonl", round_results)

    summary = summarize(inputs, round_results)
    summary.update(
        {
            "model": args.model,
            "temperature": args.temperature,
            "created_at_utc": timestamp,
        }
    )
    (out_dir / "judge_summary.json").write_text(json.dumps(summary, indent=2))

    print(f"Saved detector labels to: {out_dir / 'current_detector_labels.jsonl'}")
    print(f"Saved round outputs to: {out_dir / 'judge_rounds.jsonl'}")
    print(f"Saved summary to: {out_dir / 'judge_summary.json'}")
    print(
        "Judge vs human:",
        f"{summary['strict_judge_vs_human']['matches']}/{summary['strict_judge_vs_human']['total']}",
        f"({summary['strict_judge_vs_human']['rate']:.2%})",
    )
    print(
        "Detector vs human:",
        f"{summary['strict_detector_vs_human']['matches']}/{summary['strict_detector_vs_human']['total']}",
        f"({summary['strict_detector_vs_human']['rate']:.2%})",
    )
    print("Conflict sides:", summary["judge_sides_on_detector_human_conflicts"])


if __name__ == "__main__":
    main()
