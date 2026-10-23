"""Shared planning and resume helpers; each ablation owns its entry point."""
import argparse
import fcntl
import json
from pathlib import Path
import random

from .attempts import execute_cell
from .common import HERE, ROOT, MODELS, SCENARIOS, STUDY, ablation_dir, encoded, selections, sha, write_json
from .configuration import PAPER_AGENTIC_CONFIG, PAPER_DIRECT_CONFIG, paper_sampling, timeout_seconds
from .runtime import preflight, validate_model_routes
from .progress import run_jobs
from .traces import trace_database

def make_plan(args, conditions, load_inputs):
    scenarios = selections(args.scenarios, getattr(args, 'scenario_choices', SCENARIOS))
    models = selections(args.models, getattr(args, 'model_choices', [m for group in MODELS.values() for m in group]))
    conditions = selections(args.conditions, conditions)
    cells = []
    for scenario in scenarios:
        for model in models:
            for condition in conditions:
                data = load_inputs(condition, scenario, model)
                for repetition in range(1, args.repetitions + 1):
                    cells.append({'scenario': scenario, 'model': model, 'condition': condition,
                                  'repetition': repetition, 'prompt_sha256': sha(data['prompt']),
                                  'system_sha256': sha(data['system']),
                                  'seed_sha256': sha(data['seed']) if data['seed'] is not None else None,
                                  'task_sha256': sha(encoded(data['task']))})
    random.Random(args.schedule_seed).shuffle(cells)
    source_paths = [*sorted((HERE / 'shared').glob('*.py')),
                    HERE / 'shared/study.json',
                    *sorted((HERE / ablation_dir(args.ablation) / 'scripts').glob('*.py')),
                    ROOT / 'code/scripts/generation/run_agentic.py',
                    ROOT / 'code/scripts/generation/run_direct.py',
                    ROOT / 'code/scripts/evaluation/core/evaluate_agentic.py',
                    ROOT / 'code/benchmark/vibench/models.json',
                    PAPER_AGENTIC_CONFIG, PAPER_DIRECT_CONFIG, ROOT / 'code/configs/default.yaml']
    run_config = getattr(args, 'run_config', None)
    if run_config is not None:
        source_paths.append(run_config)
    return {'schema_version': 1, 'ablation': args.ablation, 'sampling': getattr(args, 'sampling', None) or paper_sampling(),
            'timeout': args.timeout, 'schedule_seed': args.schedule_seed,
            's11_legacy_ack': getattr(args, 's11_legacy_ack', None), 'cells': cells,
            'code_sha256': {str(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p): sha(p.read_text()) for p in source_paths}}


def argument_parser(description, conditions):
    p = argparse.ArgumentParser(description=description)
    p.add_argument('--scenarios', default='all', help='Comma-separated scenario IDs')
    p.add_argument('--models', default='all', help='Comma-separated model IDs')
    p.add_argument('--conditions', default='all', help='Comma-separated choices: ' + ','.join(conditions))
    p.add_argument('--repetitions', type=int, default=STUDY['repetitions'])
    p.add_argument('--timeout', type=timeout_seconds, default=300,
                   help='Generation budget per repository attempt, at most 300 seconds')
    p.add_argument('--schedule-seed', type=int, default=20260918)
    p.add_argument('--output', type=Path, help='New campaign directory, required with --execute')
    p.add_argument('--execute', action='store_true', help='Explicitly authorize paid model calls; default only validates and prints plan')
    p.add_argument('--resume', action='store_true')
    p.add_argument('--retry-failed', action='store_true', help='With --resume, create new attempts for failed/interrupted cells')
    p.add_argument('--limit', type=int, help='Maximum new attempts this invocation; plan stays unchanged for resume')
    p.add_argument('--max-consecutive-errors', type=int, default=3)
    p.add_argument('--workers', type=int, help='Maximum parallel models; default one worker per model')
    p.add_argument('--sequential', action='store_true', help='Run models sequentially within this ablation')
    p.add_argument('--check', action='store_true', help='Strict offline plan validation; no model calls')
    p.add_argument('--trace-db', type=Path, default=trace_database())
    return p


def launch(args, conditions, load_inputs, generate, needs_opencode, validate=None):
    if min(args.repetitions, args.timeout, args.max_consecutive_errors) < 1 or (args.limit is not None and args.limit < 1):
        raise ValueError('Counts and timeout must be positive')
    if args.retry_failed and not args.resume:
        raise ValueError('--retry-failed requires --resume')
    if args.workers is not None and args.workers < 1:
        raise ValueError('--workers must be positive')
    if args.check and args.execute:
        raise ValueError('--check cannot be combined with --execute')
    plan = make_plan(args, conditions, load_inputs)
    print(f"Ablation {args.ablation}: {len(plan['cells'])} planned runs; execution {'ENABLED' if args.execute else 'DISABLED (dry run)'}")
    print('Plan SHA256:', sha(encoded(plan)))
    for model_id in sorted({cell['model'] for cell in plan['cells']}):
        from run_direct import _reasoning_effort_sent_to_api
        from .runtime import agentic
        model = agentic.load_models(model_id)[0]
        oc = agentic.build_agentic_sampling_record(model, plan['sampling'])['opencode_variant_sent_to_opencode']
        direct = _reasoning_effort_sent_to_api(model, plan['sampling'])[0]
        print(f'{model_id}: OpenCode reasoning={oc if oc is not None else "provider default"}; direct reasoning={direct if direct is not None else "provider default"}')
    if not args.execute:
        print('No files written and no model calls made.')
        if args.check:
            validate_model_routes(plan)
            if validate is not None:
                validate(plan, args)
            return
        try:
            validate_model_routes(plan)
        except ValueError as exc:
            print(f'Launch blocker: {exc}')
        if validate is not None:
            try:
                validate(plan, args)
            except ValueError as exc:
                print(f'Launch blocker: {exc}')
        return
    if args.output is None:
        raise ValueError('--output is required with --execute')
    output = args.output.resolve()
    if output.is_relative_to(ROOT) and not output.is_relative_to(ROOT / 'outputs' / 'ablations'):
        raise ValueError('Inside this repository, campaigns must live under outputs/ablations/')
    if validate is not None:
        validate(plan, args)
    runtime = preflight(plan, args, needs_opencode(plan))
    if output.exists() and not (args.resume and (output / 'plan.json').exists()):
        raise ValueError('Output exists; use a fresh campaign directory or --resume')
    output.mkdir(parents=True, exist_ok=True)
    with (output / '.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if (output / 'plan.json').exists():
            if json.loads((output / 'plan.json').read_text()) != plan:
                raise ValueError('Plan or source code changed; start a new campaign')
            if json.loads((output / 'runtime.json').read_text()) != runtime:
                raise ValueError('Runtime versions changed; start a new campaign')
        else:
            write_json(output / 'plan.json', plan)
            write_json(output / 'runtime.json', runtime)
        run_jobs(plan, args, output, load_inputs, generate, execute_cell)
