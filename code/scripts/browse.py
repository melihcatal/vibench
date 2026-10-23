#!/usr/bin/env python3
"""Browse the VIBench benchmark and the generated outputs from the terminal.

Everything here reads the repository only — no API keys, no downloads.

    browse.py scenarios                     the 20 scenarios
    browse.py scenario S04                  one scenario in detail
    browse.py models                        the model registry
    browse.py runs                          which runs are present
    browse.py show    --model X --scenario S04
    browse.py compare --models X,Y,Z --scenario S04
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import textwrap
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CODE_DIR = SCRIPT_DIR.parent
REPO_ROOT = CODE_DIR.parent
RUNS_DIR = REPO_ROOT / "outputs" / "runs"

sys.path.insert(0, str(SCRIPT_DIR))
from vibench_loader import load_benchmark, load_models  # noqa: E402

DIRECT_PROMPTS = ("nli", "fim", "reference_open")
AGENTIC_VARIANTS = ("free", "informed")
SUBTASK_LETTERS = "abcdefgh"

DEFAULT_DIRECT_RUN = "direct/complete/full_5c"
DEFAULT_AGENTIC_RUN = "agentic/complete/opencode_full_5c"


# --------------------------------------------------------------------------
# colour
# --------------------------------------------------------------------------

# One colour per ecosystem, because the ecosystem is what every VIBench number
# is about: a generation's colour is the provider it chose.
ECOSYSTEM_COLORS = {
    "google": "38;5;33",           # blue
    "aws": "38;5;208",             # orange
    "microsoft_openai": "38;5;44",  # cyan
    "ibm": "38;5;141",             # violet
    "alibaba": "38;5;197",         # magenta
    "independent": "38;5;71",      # green
}
UNKNOWN_COLOR = "38;5;244"         # grey
_USE_COLOR = True


def init_color(flag: str) -> None:
    """Honour --color, NO_COLOR, and whether stdout is a terminal."""
    global _USE_COLOR
    if flag == "always":
        _USE_COLOR = True
    elif flag == "never" or os.environ.get("NO_COLOR"):
        _USE_COLOR = False
    else:
        _USE_COLOR = sys.stdout.isatty()


def paint(text: str, code: str | None) -> str:
    if not _USE_COLOR or not code:
        return text
    return f"\033[{code}m{text}\033[0m"


def eco_color(ecosystem) -> str:
    return ECOSYSTEM_COLORS.get(ecosystem or "", UNKNOWN_COLOR)


def eco(ecosystem) -> str:
    """An ecosystem name in its own colour."""
    return paint(str(ecosystem or "none"), eco_color(ecosystem))


def undetected(ecosystem) -> bool:
    """The detector found no provider: not a choice, so never scored as one."""
    return ecosystem in (None, "", "unknown", "none")


def bold(text: str) -> str:
    return paint(text, "1")


def dim(text: str) -> str:
    return paint(text, "2")


def width(text: str) -> int:
    """Printable width, ignoring ANSI escapes."""
    out, i = 0, 0
    while i < len(text):
        if text[i] == "\033":
            i = text.find("m", i) + 1
            continue
        out += 1
        i += 1
    return out


def pad(text: str, n: int) -> str:
    return text + " " * max(0, n - width(text))


def clip(text: str, n: int) -> str:
    """Truncate to n printable columns, keeping escapes balanced."""
    if width(text) <= n:
        return text
    out, shown, i = [], 0, 0
    while i < len(text) and shown < n - 1:
        if text[i] == "\033":
            end = text.find("m", i) + 1
            out.append(text[i:end])
            i = end
            continue
        out.append(text[i])
        shown += 1
        i += 1
    return "".join(out) + ("\033[0m…" if _USE_COLOR else "…")


# --------------------------------------------------------------------------
# lookups
# --------------------------------------------------------------------------

def model_index() -> dict:
    return {m["id"]: m for m in load_models()["models"]}


def resolve_models(spec: str, index: dict) -> list:
    """Expand a --models value: ids, or the groups 'affiliated'/'controls'/'all'."""
    if spec in ("affiliated", "controls", "control", "all", "study"):
        wanted = {"affiliated": ("affiliated",),
                  "controls": ("control",), "control": ("control",),
                  "all": ("affiliated", "control", "independent"),
                  "study": ("affiliated", "control")}[spec]
        chosen = [m for m in index.values()
                  if m.get("role") in wanted and m.get("study_order")]
        return [m["id"] for m in sorted(chosen, key=lambda m: m["study_order"])]

    ids = [s.strip() for s in spec.split(",") if s.strip()]
    unknown = [i for i in ids if i not in index]
    if unknown:
        sys.exit(f"unknown model(s): {', '.join(unknown)}\n"
                 f"list them with: browse.py models")
    return ids


def scenario_index(config: str = "direct") -> dict:
    return {t["scenario_id"]: t for t in load_benchmark(config=config)}


def resolve_scenario(sid: str, scenarios: dict) -> dict:
    key = sid.upper()
    if key not in scenarios:
        sys.exit(f"unknown scenario {sid!r}; try S01..S20 "
                 f"(list them with: browse.py scenarios)")
    return scenarios[key]


def resolve_subtask(task: dict, spec) -> int:
    """A subtask given as a letter (a..d), a 1-based number, or a role name."""
    subtasks = task["subtasks"]
    if spec is None:
        return 0
    s = str(spec).strip().lower()
    if len(s) == 1 and s in SUBTASK_LETTERS:
        idx = SUBTASK_LETTERS.index(s)
    elif s.isdigit():
        idx = int(s) - 1
    else:
        roles = [t["role"] for t in subtasks]
        if s not in roles:
            sys.exit(f"unknown subtask {spec!r} for {task['scenario_id']}; "
                     f"roles: {', '.join(roles)}")
        idx = roles.index(s)
    if not 0 <= idx < len(subtasks):
        sys.exit(f"{task['scenario_id']} has {len(subtasks)} subtasks; "
                 f"got {spec!r}")
    return idx


def run_dir(name: str) -> Path:
    """Resolve a run by relative name, leaf name, or path."""
    candidate = Path(name)
    if candidate.is_dir():
        return candidate
    direct = RUNS_DIR / name
    if direct.is_dir():
        return direct
    matches = sorted(p.parent for p in RUNS_DIR.rglob("labeled")
                     if p.is_dir() and p.parent.name == name)
    if len(matches) == 1:
        return matches[0]
    if matches:
        sys.exit(f"{name!r} matches several runs:\n  "
                 + "\n  ".join(str(m.relative_to(RUNS_DIR)) for m in matches))
    sys.exit(f"no run named {name!r} under outputs/runs/ "
             f"(list them with: browse.py runs)")


def iter_runs():
    if not RUNS_DIR.exists():
        return
    for labeled in sorted(RUNS_DIR.rglob("labeled")):
        if labeled.is_dir():
            yield labeled.parent


# --------------------------------------------------------------------------
# reading generations
# --------------------------------------------------------------------------

def direct_record(run: Path, model: str, task_id: str, prompt: str, completion: int):
    path = run / "labeled" / prompt / model / f"{task_id}__c{completion}.json"
    if not path.exists():
        return None, path
    return json.loads(path.read_text()), path


def agentic_rows(run: Path) -> list:
    path = run / "labeled" / "agentic" / "results.json"
    if not path.exists():
        sys.exit(f"{run.name} has no labeled/agentic/results.json")
    return json.loads(path.read_text())


def agentic_record(run: Path, model: str, scenario: str, variant: str, completion: int):
    for row in agentic_rows(run):
        if (row.get("model_id") == model
                and row.get("primary_atomic_scenario") == scenario
                and row.get("variant") == variant
                and row.get("completion_index") == completion):
            return row
    return None


def agentic_session_dir(run: Path, model: str, scenario: str,
                        variant: str, completion: int) -> Path:
    return (run / "raw" / "agentic" / model
            / f"agentic_{scenario}__{variant}__c{completion}")


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_scenarios(args) -> None:
    scenarios = load_benchmark(config="direct")
    print(bold(f"{len(scenarios)} VIBench scenarios") + dim("  (browse.py scenario <ID> for one)"))
    print()
    head = (f"  {'ID':4} {'FAMILY':14} {'N':>2} {'COV':5} "
            f"{'ELIGIBLE ECOSYSTEMS':40} TITLE")
    print(dim(head))
    for task in scenarios:
        cov = task.get("coverage") or {}
        providers = cov.get("providers") or {}
        eligible = [p for p, v in providers.items() if v.get("eligible")]
        tag = "all5" if cov.get("all5") else ("core4" if cov.get("core4") else "-")
        painted = " ".join(eco(p) for p in eligible)
        print(f"  {task['scenario_id']:4} {task.get('family','')[:14]:14} "
              f"{task.get('num_subtasks',0):>2} {tag:5} "
              f"{pad(painted, 40)} {task.get('title','')}")
    print()
    print(dim("  COV = provider coverage: all5 = every ecosystem offers a service, "
              "core4 = all but one"))


def cmd_scenario(args) -> None:
    scenarios = scenario_index("direct")
    task = resolve_scenario(args.scenario_id, scenarios)
    agentic = {t["primary_atomic_scenario"]: t
               for t in load_benchmark(config="agentic")}.get(task["scenario_id"])

    print(bold(f"{task['scenario_id']}  {task.get('title','')}"))
    print(f"  family       {task.get('family','')}")
    print(f"  competition  {task.get('competition','')}")
    if task.get("notes"):
        print("\n".join(textwrap.wrap(f"  notes        {task['notes']}",
                                      width=96, subsequent_indent=" " * 15)))

    print()
    print(bold("  Provider coverage"))
    providers = (task.get("coverage") or {}).get("providers") or {}
    for name, info in providers.items():
        mark = "yes" if info.get("eligible") else "no "
        service = info.get("service") or "-"
        print(f"    {pad(eco(name), 26)} {mark}  {pad(dim(info.get('interface','')), 10)}  {service}")

    print()
    print(bold(f"  Subtasks ({task.get('num_subtasks', 0)})"))
    for i, sub in enumerate(task.get("subtasks", [])):
        print(f"    {SUBTASK_LETTERS[i]}  {bold(sub.get('role',''))}"
              f"  {dim(sub.get('file',''))}")
        print("\n".join(textwrap.wrap(sub.get("description", ""), width=92,
                                      initial_indent=" " * 7, subsequent_indent=" " * 7)))

    if agentic:
        print()
        print(bold("  As an agentic workflow"))
        print(f"    task_id         {agentic.get('task_id','')}")
        print(f"    expected files  {len(agentic.get('expected_files') or [])}"
              f"   scored {len(agentic.get('scored_files') or [])}")
        print(f"    primary file    {agentic.get('primary_component_file','')}")

    if args.prompts:
        print()
        print(bold("  Prompts"))
        for i, sub in enumerate(task.get("subtasks", [])):
            print(f"\n    {bold(SUBTASK_LETTERS[i] + '  ' + sub.get('role',''))}")
            for key, label in (("nli_prompt", "NLI"),
                               ("fim_instruction", "FIM"),
                               ("reference_open_prompt", "REF")):
                if sub.get(key):
                    print(f"      {dim(label)}")
                    print("\n".join(textwrap.wrap(sub[key], width=88,
                                                  initial_indent=" " * 10,
                                                  subsequent_indent=" " * 10)))
    else:
        print()
        print(dim("  --prompts to print the NLI / FIM / REF prompt text"))


def cmd_models(args) -> None:
    models = load_models()["models"]
    study = [m for m in models if m.get("study_order")]
    other = [m for m in models if not m.get("study_order")]
    study.sort(key=lambda m: m["study_order"])

    print(bold(f"{len(study)} study models") + dim(f"  ({len(other)} further registry entries)"))
    print()
    print(dim(f"  {'#':>2} {'ID':26} {'ROLE':11} {'ECOSYSTEM':17} {'TIER':9} NAME"))
    for m in study:
        print(f"  {m['study_order']:>2} {m['id']:26} {m.get('role',''):11} "
              f"{pad(eco(m.get('ecosystem_affiliation')), 17)} "
              f"{m.get('tier',''):9} {m.get('display_name','')}")
    if other:
        print()
        print(dim("  not in the study grid:"))
        for m in other:
            print(f"     {pad(dim(m['id']), 26)} {dim(m.get('role') or '-')}")
    print()
    print(dim("  VIB compares each affiliated model against the mean of the control models."))


def cmd_runs(args) -> None:
    found = list(iter_runs())
    if not found:
        sys.exit(f"no runs found under {RUNS_DIR}")
    print(bold(f"{len(found)} runs under outputs/runs/"))
    print()
    print(dim(f"  {'RUN':60} {'KIND':8} RECORDS"))
    for run in found:
        rel = run.relative_to(RUNS_DIR).as_posix()
        if (run / "labeled" / "agentic").is_dir():
            kind = "agentic"
            path = run / "labeled" / "agentic" / "results.json"
            n = len(json.loads(path.read_text())) if path.exists() else 0
        else:
            kind = "direct"
            n = sum(1 for _ in (run / "labeled").rglob("*.json"))
        print(f"  {rel:60} {kind:8} {n:,}")
    print()
    print(dim(f"  defaults: --run {DEFAULT_DIRECT_RUN} (direct), "
              f"{DEFAULT_AGENTIC_RUN} (agentic)"))


def _show_direct(args, index) -> None:
    scenarios = scenario_index("direct")
    task = resolve_scenario(args.scenario, scenarios)
    idx = resolve_subtask(task, args.subtask)
    sub = task["subtasks"][idx]
    task_id = f"{args.prompt}_{task['scenario_id']}_{SUBTASK_LETTERS[idx]}"
    run = run_dir(args.run or DEFAULT_DIRECT_RUN)

    rec, path = direct_record(run, args.model, task_id, args.prompt, args.completion)
    if rec is None:
        sys.exit(f"no generation at {path.relative_to(REPO_ROOT)}\n"
                 f"check --prompt ({'/'.join(DIRECT_PROMPTS)}), --completion, --run")

    own = index[args.model].get("ecosystem_affiliation")
    chose = rec.get("detected_ecosystem")
    print(bold(f"{args.model}") + dim("  affiliated with ") + eco(own))
    print(f"{dim('scenario  ')}{task['scenario_id']}  {task.get('title','')}")
    print(f"{dim('subtask   ')}{SUBTASK_LETTERS[idx]}  {sub.get('role','')}  "
          f"{dim(sub.get('file',''))}")
    print(f"{dim('prompt    ')}{args.prompt}   {dim('completion')} {args.completion}")
    print()
    print(f"{dim('chose     ')}{eco(chose)}  "
          f"{rec.get('detected_service') or '-'}  "
          f"{dim('via ' + str(rec.get('detection_method')))}  "
          f"{dim('confidence ' + str(rec.get('detection_confidence')))}")
    if rec.get("is_multi_ecosystem"):
        others = " ".join(eco(e) for e in rec.get("detected_ecosystems", []))
        print(f"{dim('also      ')}{others}   {dim('(multi-provider output)')}")
    if undetected(chose):
        print(f"{dim('i.e.      ')}no provider detected in this output")
    elif own:
        verdict = ("own ecosystem" if chose == own else "a neutral option"
                   if chose == "independent" else "a rival ecosystem")
        print(f"{dim('i.e.      ')}{verdict}")

    if args.prompt_text:
        print()
        print(bold("prompt"))
        print(textwrap.indent(rec.get("prompt_text", ""), "  "))

    print()
    print(bold("generated code") + dim(f"   {path.relative_to(REPO_ROOT)}"))
    print(dim("─" * min(shutil.get_terminal_size().columns, 100)))
    print(rec.get("output_text", ""))


def _show_agentic(args, index) -> None:
    scenarios = scenario_index("direct")
    task = resolve_scenario(args.scenario, scenarios)
    variant = args.prompt if args.prompt in AGENTIC_VARIANTS else "informed"
    run = run_dir(args.run or DEFAULT_AGENTIC_RUN)

    row = agentic_record(run, args.model, task["scenario_id"], variant, args.completion)
    if row is None:
        sys.exit(f"no agentic session for {args.model} {task['scenario_id']} "
                 f"{variant} c{args.completion} in {run.name}\n"
                 f"variants are {'/'.join(AGENTIC_VARIANTS)}")

    own = index[args.model].get("ecosystem_affiliation")
    print(bold(f"{args.model}") + dim("  affiliated with ") + eco(own))
    print(f"{dim('workflow  ')}{row.get('task_id','')}  {task.get('title','')}")
    print(f"{dim('variant   ')}{variant}   {dim('completion')} {args.completion}")
    print()
    print(f"{dim('dominant  ')}{eco(row.get('dominant_ecosystem'))}"
          f"   {dim('coherence')} {row.get('ecosystem_coherence')}"
          f"   {dim('files')} {row.get('present_files')}/{row.get('expected_files')}")
    counts = row.get("ecosystem_counts") or {}
    if counts:
        spread = "  ".join(f"{eco(k)} {v}" for k, v in
                           sorted(counts.items(), key=lambda kv: -kv[1]))
        print(f"{dim('spread    ')}{spread}")

    print()
    print(bold("per-file labels"))
    print(dim(f"  {'FILE':34} {'ECOSYSTEM':17} SERVICE"))
    for role, info in (row.get("components") or {}).items():
        print(f"  {info.get('file', role):34} "
              f"{pad(eco(info.get('ecosystem')), 17)} {info.get('service') or '-'}")

    session = agentic_session_dir(run, args.model, task["scenario_id"],
                                  variant, args.completion)
    if args.file:
        target = session / args.file
        if not target.exists():
            sys.exit(f"no such file in the session: {args.file}\n"
                     f"session is {session.relative_to(REPO_ROOT)}")
        print()
        print(bold(args.file) + dim(f"   {target.relative_to(REPO_ROOT)}"))
        print(dim("─" * min(shutil.get_terminal_size().columns, 100)))
        print(target.read_text())
    elif session.is_dir():
        print()
        print(dim(f"  session files in {session.relative_to(REPO_ROOT)}"))
        print(dim(f"  --file <name> to print one"))


def cmd_show(args) -> None:
    index = model_index()
    if args.model not in index:
        sys.exit(f"unknown model {args.model!r} (list them with: browse.py models)")
    if args.mode == "agentic":
        _show_agentic(args, index)
    else:
        _show_direct(args, index)


def cmd_compare(args) -> None:
    index = model_index()
    models = resolve_models(args.models, index)
    scenarios = scenario_index("direct")
    task = resolve_scenario(args.scenario, scenarios)

    if args.mode == "agentic":
        variant = args.prompt if args.prompt in AGENTIC_VARIANTS else "informed"
        run = run_dir(args.run or DEFAULT_AGENTIC_RUN)
        header = f"{task['scenario_id']}  {task.get('title','')}   agentic/{variant}"
        cells = []
        for mid in models:
            row = agentic_record(run, mid, task["scenario_id"], variant, args.completion)
            cells.append({
                "model": mid,
                "own": index[mid].get("ecosystem_affiliation"),
                "chose": row.get("dominant_ecosystem") if row else None,
                "missing": row is None,
                "detail": (f"coherence {row.get('ecosystem_coherence')}"
                           if row else "no session"),
                "code": None,
            })
    else:
        idx = resolve_subtask(task, args.subtask)
        sub = task["subtasks"][idx]
        task_id = f"{args.prompt}_{task['scenario_id']}_{SUBTASK_LETTERS[idx]}"
        run = run_dir(args.run or DEFAULT_DIRECT_RUN)
        header = (f"{task['scenario_id']}  {task.get('title','')}   "
                  f"{SUBTASK_LETTERS[idx]}/{sub.get('role','')}   {args.prompt}")
        cells = []
        for mid in models:
            rec, _ = direct_record(run, mid, task_id, args.prompt, args.completion)
            cells.append({
                "model": mid,
                "own": index[mid].get("ecosystem_affiliation"),
                "chose": rec.get("detected_ecosystem") if rec else None,
                "missing": rec is None,
                "detail": (rec.get("detected_service") or "-") if rec else "no generation",
                "code": rec.get("output_text", "") if rec else "",
            })

    print(bold(header) + dim(f"   completion {args.completion}   run {run.name}"))
    print()

    term = shutil.get_terminal_size().columns
    col = max(18, (term - 2 - 3 * (len(cells) - 1)) // max(1, len(cells)))

    def row_of(values, painter=lambda v: v):
        return " " + dim("│").join(f" {pad(clip(painter(v), col), col)} " for v in values)

    print(row_of([c["model"] for c in cells], bold))
    print(" " + dim("│").join(dim("─" * (col + 2)) for _ in cells))
    print(row_of([f"own   {eco(c['own'])}" for c in cells]))
    print(row_of([dim("chose —") if c["missing"] else f"chose {eco(c['chose'])}"
                  for c in cells]))
    print(row_of([c["detail"] for c in cells], dim))

    # A one-line verdict per column: the whole point of the comparison.
    def verdict(c):
        if c["missing"]:
            return dim("—")
        if undetected(c["chose"]):
            return dim("undetected")
        if c["own"] and c["chose"] == c["own"]:
            return paint("OWN", eco_color(c["chose"]))
        if c["chose"] == "independent":
            return dim("neutral")
        return "rival" if c["own"] else dim("n/a")

    print(row_of([verdict(c) for c in cells]))

    if args.code and args.mode != "agentic":
        print()
        print(bold("generated code"))
        print(" " + dim("│").join(dim("─" * (col + 2)) for _ in cells))
        blocks = [(c["code"] or "").splitlines() for c in cells]
        limit = args.lines if args.lines else max((len(b) for b in blocks), default=0)
        for i in range(min(limit, max((len(b) for b in blocks), default=0))):
            line = [b[i] if i < len(b) else "" for b in blocks]
            print(row_of(line, lambda v: v.replace("\t", "    ")))
        print()
        print(dim(f"  --lines N to cut the listing short"))
    elif args.code:
        print()
        print(dim("  --code shows side-by-side source for direct generations only; "
                  "use `show --mode agentic --file <name>` for a session file"))


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="browse.py",
        description="Browse the VIBench benchmark and generated outputs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples
              browse.py scenarios
              browse.py scenario S04 --prompts
              browse.py models
              browse.py runs
              browse.py show --model gemini-2.5-flash --scenario S04
              browse.py show --model nova-pro --scenario S04 --mode agentic --file speech_client.py
              browse.py compare --models affiliated --scenario S04
              browse.py compare --models gemini-2.5-flash,deepseek-v3.2 --scenario S04 --code --lines 25
            """))
    parser.add_argument("--color", choices=("auto", "always", "never"), default="auto",
                        help="colourise ecosystems (default: auto)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("scenarios", help="list the 20 scenarios").set_defaults(func=cmd_scenarios)

    p = sub.add_parser("scenario", help="one scenario in detail")
    p.add_argument("scenario_id", help="e.g. S04")
    p.add_argument("--prompts", action="store_true", help="also print the prompt text")
    p.set_defaults(func=cmd_scenario)

    sub.add_parser("models", help="the model registry").set_defaults(func=cmd_models)
    sub.add_parser("runs", help="which runs are present").set_defaults(func=cmd_runs)

    def add_selectors(q, *, multi):
        if multi:
            q.add_argument("--models", required=True,
                           help="comma-separated ids, or a group: "
                                "affiliated, controls, study, all")
        else:
            q.add_argument("--model", required=True, help="a model id")
        q.add_argument("--scenario", required=True, help="e.g. S04")
        q.add_argument("--subtask", help="letter a-d, number 1-4, or role name "
                                         "(direct only, default: a)")
        q.add_argument("--mode", choices=("direct", "agentic"), default="direct",
                       help="default: direct")
        q.add_argument("--prompt", default="nli",
                       help="direct: %s; agentic: %s (default: nli / informed)"
                            % ("/".join(DIRECT_PROMPTS), "/".join(AGENTIC_VARIANTS)))
        q.add_argument("--completion", type=int, default=1, help="1-5 (default: 1)")
        q.add_argument("--run", help="run name (default: the study run for the mode)")

    q = sub.add_parser("show", help="one generation with its detected label")
    add_selectors(q, multi=False)
    q.add_argument("--file", help="agentic only: print one file from the session")
    q.add_argument("--prompt-text", action="store_true", help="also print the prompt")
    q.set_defaults(func=cmd_show)

    q = sub.add_parser("compare", help="several models side by side")
    add_selectors(q, multi=True)
    q.add_argument("--code", action="store_true", help="also show source side by side")
    q.add_argument("--lines", type=int, help="limit the side-by-side listing")
    q.set_defaults(func=cmd_compare)
    return parser


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    init_color(args.color)
    if getattr(args, "mode", None) == "direct" and getattr(args, "prompt", None) in AGENTIC_VARIANTS:
        sys.exit(f"--prompt {args.prompt} is an agentic variant; "
                 f"add --mode agentic, or use one of {'/'.join(DIRECT_PROMPTS)}")
    args.func(args)


if __name__ == "__main__":
    main()
