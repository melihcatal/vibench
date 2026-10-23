"""Extend a finished single-shot campaign without modifying or repeating it."""
from collections import Counter
import fcntl
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.agentic_mechanism.single_shot_multifile.scripts import run
from ablations.shared import campaign, configuration, runtime
from ablations.shared.attempts import cell_key
from ablations.shared.common import HERE, ROOT, encoded, sha, write_json
from ablations.shared.progress import pending_cells, run_jobs

DEFAULT_CONFIG = HERE / 'agentic_mechanism/single_shot_multifile/config_20_scenarios.yaml'
DEFAULT_PREVIOUS = ROOT / 'outputs/ablations/agentic_mechanism/single_shot_multifile/a2_single_shot_8s_3m_5c'


def extension_plan(target, previous):
    old = json.loads((previous / 'plan.json').read_text())
    for key in ('ablation', 'sampling', 'timeout'):
        if old[key] != target[key]:
            raise ValueError(f'Previous campaign differs in {key}; cannot pool as one configuration')
    if any(c['condition'] != 'single_shot' for c in old['cells'] + target['cells']):
        raise ValueError('Extension only supports single-shot conditions')
    # Verify every source/config recorded before the first eight scenarios ran.
    for name, checksum in old['code_sha256'].items():
        path = ROOT / name
        if not path.exists() or sha(path.read_text()) != checksum:
            raise ValueError(f'Previous generation source/config changed: {name}')
    requested = {cell_key(c): c for c in target['cells']}
    retained = []
    for cell in old['cells']:
        key = cell_key(cell)
        if requested.get(key) != cell:
            raise ValueError(f'Previous cell missing or input hashes changed: {key}')
        attempts = sorted((previous / 'runs' / key).glob('attempt_*'))
        if not attempts or not (attempts[-1] / 'status.json').exists():
            raise ValueError(f'Previous cell has no terminal status: {key}')
        attempt = attempts[-1]
        status = json.loads((attempt / 'status.json').read_text())
        if status['state'] not in ('completed', 'failed'):
            raise ValueError(f'Previous cell is not finished: {key}')
        if json.loads((attempt / 'input.json').read_text())['cell'] != cell:
            raise ValueError(f'Previous attempt input mismatch: {key}')
        retained.append({'cell': key, 'state': status['state'],
                         'source_attempt': str(attempt.relative_to(previous)),
                         'status_sha256': sha((attempt / 'status.json').read_text()),
                         'response_sha256': sha((attempt / 'response.json').read_text())})
        del requested[key]
    return {**target, 'cells': [c for c in target['cells'] if cell_key(c) in requested],
            'requested_cell_count': len(target['cells']),
            'previous_campaign': str(previous), 'previous_plan_sha256': sha(encoded(old)),
            'retained_attempts': retained}


def parser(config_path=DEFAULT_CONFIG):
    p = run.parser(config_path)
    p.description = __doc__
    p.add_argument('--previous', type=Path, default=DEFAULT_PREVIOUS)
    return p


def main(argv=None):
    args = configuration.parse_args(parser, DEFAULT_CONFIG, argv)
    if args.retry_failed:
        raise ValueError('Extension preserves failed attempts; retries are not part of this protocol')
    if args.check and args.execute:
        raise ValueError('--check and --execute are mutually exclusive')
    if min(args.repetitions, args.timeout, args.max_consecutive_errors) < 1 or (args.limit is not None and args.limit < 1) or (args.workers is not None and args.workers < 1):
        raise ValueError('Counts, timeout, limit, and workers must be positive')
    previous = args.previous.resolve()
    plan = extension_plan(campaign.make_plan(args, run.CONDITIONS, run.cell_inputs), previous)
    runtime.validate_model_routes(plan)
    current_runtime = runtime.runtime_record(needs_opencode=False)
    if current_runtime != json.loads((previous / 'runtime.json').read_text()):
        raise ValueError('Runtime differs from the previous campaign; review before extending')
    output = args.output.resolve() if args.output else None
    if output is not None:
        if output == previous or output.is_relative_to(previous) or previous.is_relative_to(output):
            raise ValueError('Use a separate, non-overlapping output directory')
        if output.is_relative_to(ROOT) and not output.is_relative_to(ROOT / 'outputs' / 'ablations'):
            raise ValueError('Repository campaign outputs must be under ablations/outputs/')
        if output.exists():
            if not args.resume or not (output / 'plan.json').exists():
                raise ValueError('Extension output exists; use --resume with unchanged settings')
            if json.loads((output / 'plan.json').read_text()) != plan:
                raise ValueError('Extension plan or source changed; do not resume')
            if json.loads((output / 'runtime.json').read_text()) != current_runtime:
                raise ValueError('Extension runtime changed; do not resume')
    pending, local_skipped = pending_cells(plan, output, args.resume, False) if output and output.exists() else (plan['cells'], 0)
    selected = pending if args.limit is None else pending[:args.limit]
    retained = Counter(r['state'] for r in plan['retained_attempts'])
    print(f"Ablation 2 target: {plan['requested_cell_count']} runs across 20 scenarios" if args.scenarios == 'all' else f"Ablation 2 target: {plan['requested_cell_count']} runs")
    print(f"Previous attempts skipped: {len(plan['retained_attempts'])} ({retained['completed']} completed, {retained['failed']} failed; all retained, no retries)")
    print(f'Existing extension attempts skipped: {local_skipped}')
    print(f'New runs scheduled: {len(selected)}; pending before limit: {len(pending)}')
    print('New scenarios: ' + ', '.join(sorted({c['scenario'] for c in selected})))
    print('New runs per model: ' + json.dumps(dict(Counter(c['model'] for c in selected)), sort_keys=True))
    print(f'Timeout: {plan["timeout"]} seconds; workers: {args.workers}')
    print('Plan SHA256: ' + sha(encoded(plan)))
    if not args.execute:
        print('Dry run: no files written and no model calls made.')
        return
    if output is None:
        raise ValueError('--output is required with --execute')
    checked_runtime = runtime.preflight(plan, args, needs_opencode=False)
    if checked_runtime != current_runtime:
        raise ValueError('Runtime changed during preflight')
    output.mkdir(parents=True, exist_ok=True)
    with (output / '.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if not (output / 'plan.json').exists():
            write_json(output / 'plan.json', plan)
            write_json(output / 'runtime.json', checked_runtime)
        run_jobs(plan, args, output, run.cell_inputs, run.generate, campaign.execute_cell)


if __name__ == '__main__':
    main()
