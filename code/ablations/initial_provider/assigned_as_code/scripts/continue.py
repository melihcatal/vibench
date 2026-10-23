"""Continue A1 with five attempts per cell and an explicit settings migration."""
from collections import Counter
import fcntl
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.initial_provider.assigned_as_code.scripts import run
from ablations.shared import campaign, configuration, runtime
from ablations.shared.attempts import cell_key
from ablations.shared.common import HERE, ROOT, encoded, redact, sha, write_json
from ablations.shared.progress import pending_cells, run_jobs

DEFAULT_CONFIG = HERE / 'initial_provider/assigned_as_code/config_completion.yaml'
# No default predecessor: the shipped a1_completion_20s_3m_5c run already has the
# attempts it retained from its interrupted predecessor materialised in place
# (see retained_attempts_materialized in its plan.json), so that run was removed
# from the package. Pass --previous explicitly to resume your own campaign.
DEFAULT_PREVIOUS = None
MIGRATION = HERE / 'initial_provider/assigned_as_code/continuation_migration.json'


def effective_sampling(model, sampling):
    record = runtime.agentic.build_agentic_sampling_record(model, sampling)
    return {key: record[key] for key in (
        'temperature_sent_to_opencode', 'top_p_sent_to_opencode',
        'max_tokens', 'opencode_variant_sent_to_opencode')}


def continuation_plan(target, previous):
    old = json.loads((previous / 'plan.json').read_text())
    for key in ('ablation', 'timeout'):
        if old[key] != target[key]:
            raise ValueError(f'Previous campaign differs in {key}')
    migration = json.loads(MIGRATION.read_text())
    changes = {}
    for name, checksum in old['code_sha256'].items():
        current = sha((ROOT / name).read_text())
        if current != checksum:
            pair = {'previous': checksum, 'current': current}
            if migration.get(name) != pair:
                raise ValueError(f'Unreviewed source change: {name}')
            changes[name] = pair
    old_cells = {cell_key(c): c for c in old['cells']}
    if len(old_cells) != len(old['cells']):
        raise ValueError('Duplicate archived cells')
    retained, incompatible, scheduled = [], [], []
    settings = {}
    for cell in target['cells']:
        key = cell_key(cell)
        if old_cells.get(key) != cell:
            raise ValueError(f'Archived inputs differ: {key}')
        model = runtime.agentic.load_models(cell['model'])[0]
        before = effective_sampling(model, old['sampling'])
        after = effective_sampling(model, target['sampling'])
        settings[cell['model']] = {'previous': before, 'current': after}
        # Only the documented GPT default -> none migration can replace attempts.
        if before != after:
            if cell['model'] not in ('gpt-5.4', 'gpt-5.4-mini') or before != {**after, 'opencode_variant_sent_to_opencode': None} or after['opencode_variant_sent_to_opencode'] != 'none':
                raise ValueError(f'Unreviewed sampling change: {cell["model"]}')
        attempts = sorted((previous / 'runs' / key).glob('attempt_*'))
        if not attempts:
            scheduled.append(cell)
            continue
        if len(attempts) != 1:
            raise ValueError(f'Ambiguous archived attempts: {key}')
        attempt = attempts[0]
        data = json.loads((attempt / 'input.json').read_text())
        status = json.loads((attempt / 'status.json').read_text())
        if status['state'] not in ('completed', 'failed'):
            raise ValueError(f'Nonterminal archived attempt: {key}')
        if data['cell'] != cell or data['model'] != redact(model) or sha(encoded(data['task'])) != cell['task_sha256']:
            raise ValueError(f'Archived model/task mismatch: {key}')
        if sha((attempt / 'prompt.txt').read_text()) != cell['prompt_sha256'] or sha((attempt / 'system_prompt.txt').read_text()) != cell['system_sha256']:
            raise ValueError(f'Archived prompt mismatch: {key}')
        record = {'cell': key, 'model': cell['model'], 'state': status['state'],
                  'source_attempt': str(attempt.relative_to(previous)),
                  'artifacts_sha256': {str(p.relative_to(attempt)): sha(p.read_text())
                     for p in sorted(attempt.rglob('*')) if p.is_file()}}
        if before != after:
            incompatible.append(record)
            scheduled.append(cell)
        else:
            retained.append(record)
    return {**target, 'cells': scheduled, 'requested_cell_count': len(target['cells']),
            'previous_campaign': str(previous), 'previous_plan_sha256': sha(encoded(old)),
            'previous_runtime_sha256': sha((previous / 'runtime.json').read_text()),
            'migration_sha256': sha(MIGRATION.read_text()), 'source_migration': changes,
            'effective_sampling': settings, 'retained_attempts': retained,
            'incompatible_archived_attempts': incompatible,
            'policy': 'First five assigned repetitions; retain compatible failures; replace incompatible GPT settings, never overwrite archived runs.'}


def parser(config_path=DEFAULT_CONFIG):
    p = run.parser(config_path)
    p.add_argument('--previous', type=Path, default=DEFAULT_PREVIOUS,
                   required=DEFAULT_PREVIOUS is None,
                   help='Interrupted campaign directory to retain compatible attempts from')
    return p


def main(argv=None):
    args = configuration.parse_args(parser, DEFAULT_CONFIG, argv)
    if args.retry_failed:
        raise ValueError('Retain failed attempts; this continuation does not retry them')
    if args.check and args.execute:
        raise ValueError('--check cannot be combined with --execute')
    if min(args.repetitions, args.timeout, args.max_consecutive_errors, args.workers or 1, args.limit or 1) < 1:
        raise ValueError('Counts must be positive')
    if args.repetitions != 5:
        raise ValueError('This continuation is defined for repetitions 1 through 5')
    previous = args.previous.resolve()
    # Do not inventory an archive that another process is still writing.
    with (previous / '.lock').open('r') as prior_lock:
        fcntl.flock(prior_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        target = campaign.make_plan(args, run.CONDITIONS, run.cell_inputs)
        run.validate(target, args)
        plan = continuation_plan(target, previous)
        runtime.validate_model_routes(plan)
        current_runtime = runtime.runtime_record(needs_opencode=True)
        if current_runtime != json.loads((previous / 'runtime.json').read_text()):
            raise ValueError('Runtime changed; review before continuing')
        output = args.output.resolve() if args.output else None
        if output:
            if output == previous or output.is_relative_to(previous) or previous.is_relative_to(output):
                raise ValueError('Use a separate output directory')
            if output.is_relative_to(ROOT) and not output.is_relative_to(ROOT / 'outputs' / 'ablations'):
                raise ValueError('Outputs inside repo must be under ablations/outputs')
            if output.exists():
                if not args.resume or not (output / 'plan.json').exists():
                    raise ValueError('Existing output requires --resume')
                if json.loads((output / 'plan.json').read_text()) != plan:
                    raise ValueError('Continuation plan/source/archive changed; cannot resume')
                if json.loads((output / 'runtime.json').read_text()) != current_runtime:
                    raise ValueError('Continuation runtime changed')
        pending, skipped = pending_cells(plan, output, args.resume, False) if output and output.exists() else (plan['cells'], 0)
        selected = pending if args.limit is None else pending[:args.limit]
        retained = Counter(r['state'] for r in plan['retained_attempts'])
        print(f"Ablation 1 target: {plan['requested_cell_count']} runs (five repetitions)")
        print(f"Compatible archived attempts skipped: {len(plan['retained_attempts'])} ({retained['completed']} completed, {retained['failed']} failed; no retries)")
        print(f"Incompatible archived GPT attempts excluded: {len(plan['incompatible_archived_attempts'])}; selected GPT models use reasoning=none")
        print(f'Existing continuation attempts skipped: {skipped}')
        print(f'New runs scheduled: {len(selected)}; pending before limit: {len(pending)}')
        print('New runs per model: ' + json.dumps(dict(Counter(c['model'] for c in selected)), sort_keys=True))
        print(f'Timeout: {plan["timeout"]} seconds; workers: {1 if args.sequential else args.workers}')
        print('Plan SHA256: ' + sha(encoded(plan)))
        if not args.execute:
            print('Dry run: no files written and no model calls made.')
            return
        if output is None:
            raise ValueError('--output required with --execute')
        checked = runtime.preflight(plan, args, needs_opencode=True)
        if checked != current_runtime:
            raise ValueError('Runtime changed during preflight')
        output.mkdir(parents=True, exist_ok=True)
        with (output / '.lock').open('w') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            if (output / 'plan.json').exists():
                if json.loads((output / 'plan.json').read_text()) != plan:
                    raise ValueError('Continuation plan changed while acquiring lock')
            else:
                write_json(output / 'plan.json', plan)
                write_json(output / 'runtime.json', checked)
            run_jobs(plan, args, output, run.cell_inputs, run.opencode.generate, campaign.execute_cell)


if __name__ == '__main__':
    main()
