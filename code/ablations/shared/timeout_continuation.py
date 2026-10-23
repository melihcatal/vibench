"""Explicit 1200s -> 300s continuation; archived attempts remain separate."""
from collections import Counter
from contextlib import ExitStack
import fcntl
import json
from pathlib import Path

from . import campaign, configuration, runtime
from .attempts import cell_key
from .common import HERE, ROOT, encoded, redact, sha, write_json
from .progress import pending_cells, run_jobs

MIGRATIONS = HERE / 'shared/timeout_migrations.json'


def read_plan(root):
    return json.loads((root / 'plan.json').read_text())


def verify_sources(root, migrations):
    plan = read_plan(root)
    checksum = sha((root / 'plan.json').read_text())
    if checksum not in migrations:
        raise ValueError(f'Unreviewed source campaign: {root}')
    allowed = migrations[checksum]['changes']
    for name, before in plan['code_sha256'].items():
        current = sha((ROOT / name).read_text())
        if current != before and allowed.get(name) != {'previous': before, 'current': current}:
            raise ValueError(f'Unreviewed source change: {name}')
    return plan


def effective_sampling(model, settings):
    resolved = runtime.agentic.build_agentic_sampling_record(model, settings)
    return {k: resolved[k] for k in ('temperature_sent_to_opencode',
            'top_p_sent_to_opencode', 'max_tokens', 'opencode_variant_sent_to_opencode')}


def validate_attempt(root, attempt, cell, source_plan, target, expected_hashes=None):
    data = json.loads((attempt / 'input.json').read_text())
    status = json.loads((attempt / 'status.json').read_text())
    if status['state'] not in ('completed', 'failed'):
        raise ValueError(f'Archive contains nonterminal attempt: {attempt}')
    model = runtime.agentic.load_models(cell['model'])[0]
    if data['cell'] != cell or data['model'] != redact(model):
        raise ValueError(f'Archived cell/model changed: {attempt}')
    if sha(encoded(data['task'])) != cell['task_sha256']:
        raise ValueError(f'Archived task changed: {attempt}')
    for filename, key in [('prompt.txt', 'prompt_sha256'), ('system_prompt.txt', 'system_sha256')]:
        if sha((attempt / filename).read_text()) != cell[key]:
            raise ValueError(f'Archived prompt changed: {attempt}')
    if effective_sampling(model, source_plan['sampling']) != effective_sampling(model, target['sampling']):
        raise ValueError(f'Cannot retain incompatible reasoning settings: {attempt}')
    hashes = {str(p.relative_to(attempt)): sha(p.read_text())
              for p in sorted(attempt.rglob('*')) if p.is_file()}
    if expected_hashes is not None and hashes != expected_hashes:
        raise ValueError(f'Inherited attempt changed: {attempt}')
    return {'cell': cell_key(cell), 'model': cell['model'], 'state': status['state'],
            'source_campaign': str(root), 'source_attempt': str(attempt.relative_to(root)),
            'timeout_seconds': source_plan['timeout'], 'elapsed_seconds': status.get('elapsed_seconds'),
            'artifacts_sha256': hashes}


def continuation_plan(target, previous):
    migrations = json.loads(MIGRATIONS.read_text())
    old = verify_sources(previous, migrations)
    if old['ablation'] != target['ablation'] or old['timeout'] != 1200 or target['timeout'] != 300:
        raise ValueError('This migration requires the same ablation and timeout 1200 -> 300')
    if old['sampling'] != target['sampling']:
        raise ValueError('Sampling changed in addition to timeout')
    requested = {cell_key(c): c for c in target['cells']}
    if len(requested) != len(target['cells']):
        raise ValueError('Duplicate target cells')
    covered, records, sources = set(), [], [previous]
    inherited = old.get('retained_attempts', [])
    if inherited:
        parent = Path(old['previous_campaign'])
        parent_plan = verify_sources(parent, migrations)
        if sha(encoded(parent_plan)) != old['previous_plan_sha256']:
            raise ValueError('Parent plan changed')
        if sha((parent / 'runtime.json').read_text()) != old['previous_runtime_sha256']:
            raise ValueError('Parent runtime changed')
        sources.append(parent)
        parent_cells = {cell_key(c): c for c in parent_plan['cells']}
        for prior in inherited:
            key = prior['cell']
            cell = requested.get(key)
            if cell is None or cell != parent_cells.get(key) or key in covered:
                raise ValueError(f'Inherited input/coverage mismatch: {key}')
            records.append(validate_attempt(parent, parent / prior['source_attempt'], cell,
                           parent_plan, target, prior['artifacts_sha256']))
            covered.add(key)
    for cell in old['cells']:
        key = cell_key(cell)
        if requested.get(key) != cell or key in covered:
            raise ValueError(f'Previous input/coverage mismatch: {key}')
        covered.add(key)
        attempts = sorted((previous / 'runs' / key).glob('attempt_*'))
        if len(attempts) > 1:
            raise ValueError(f'Multiple attempts require explicit adjudication: {key}')
        if attempts:
            records.append(validate_attempt(previous, attempts[0], cell, old, target))
    if covered != set(requested):
        raise ValueError('Target scope differs from stopped campaign')
    retained_keys = {r['cell'] for r in records}
    return {**target, 'cells': [c for c in target['cells'] if cell_key(c) not in retained_keys],
            'requested_cell_count': len(target['cells']), 'retained_attempts': records,
            'source_campaigns': [{'path': str(p), 'plan_sha256': sha((p / 'plan.json').read_text()),
                                 'runtime_sha256': sha((p / 'runtime.json').read_text())} for p in sources],
            'migration_sha256': sha(MIGRATIONS.read_text()),
            'timeout_migration': {'archived': 1200, 'new': 300},
            'analysis_note': 'Mixed timeout protocols: retain per-run budgets, report separately/sensitivity; never relabel archived 1200s attempts as 300s. Failed attempts are not retried.'}


def launch(run, config, previous_default, argv=None):
    def parser(config_path=config):
        p = run.parser(config_path)
        p.add_argument('--previous', type=Path, default=previous_default)
        return p
    args = configuration.parse_args(parser, config, argv)
    if args.retry_failed or (args.check and args.execute):
        raise ValueError('No failed retries; --check and --execute cannot be combined')
    if min(args.repetitions, args.timeout, args.max_consecutive_errors) < 1 or (args.limit is not None and args.limit < 1) or (args.workers is not None and args.workers < 1):
        raise ValueError('Counts must be positive')
    previous = args.previous.resolve()
    old = read_plan(previous)
    archives = [previous] + ([Path(old['previous_campaign'])] if old.get('retained_attempts') else [])
    with ExitStack() as stack:
        for archive in sorted(set(archives)):
            handle = stack.enter_context((archive / '.lock').open('r'))
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        conditions = run.CONDITIONS if hasattr(run, 'CONDITIONS') else tuple(run.configuration()['conditions'])
        target = campaign.make_plan(args, conditions, run.cell_inputs)
        if hasattr(run, 'validate'):
            run.validate(target, args)
        plan = continuation_plan(target, previous)
        runtime.validate_model_routes(plan)
        current_runtime = runtime.runtime_record(needs_opencode=True)
        for archive in archives:
            if json.loads((archive / 'runtime.json').read_text()) != current_runtime:
                raise ValueError('Runtime changed; review before continuation')
        output = args.output.resolve() if args.output else None
        if output:
            if any(output == p or output.is_relative_to(p) or p.is_relative_to(output) for p in archives):
                raise ValueError('Use a new non-overlapping output directory')
            if output.is_relative_to(ROOT) and not output.is_relative_to(ROOT / 'outputs' / 'ablations'):
                raise ValueError('Repository outputs must be under ablations/outputs')
            if output.exists():
                if not args.resume or not (output / 'plan.json').exists():
                    raise ValueError('Existing continuation requires --resume')
                if read_plan(output) != plan or json.loads((output / 'runtime.json').read_text()) != current_runtime:
                    raise ValueError('Continuation plan, archive, sources, or runtime changed')
        pending, skipped = pending_cells(plan, output, args.resume, False) if output and output.exists() else (plan['cells'], 0)
        selected = pending if args.limit is None else pending[:args.limit]
        counts = Counter(r['state'] for r in plan['retained_attempts'])
        print(f"Ablation {args.ablation}: {plan['requested_cell_count']} target runs")
        print(f"Archived attempts skipped: {len(plan['retained_attempts'])} ({counts['completed']} completed, {counts['failed']} failed)")
        print(f'Existing 300s attempts skipped: {skipped}; new scheduled: {len(selected)}')
        print('New runs per model: ' + json.dumps(dict(Counter(c['model'] for c in selected)), sort_keys=True))
        print(f"New timeout: 300 seconds per repository; workers: {1 if args.sequential else args.workers}")
        print('Archived attempts keep their 1200-second budget; mixed-budget analysis must be explicit.')
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
                if read_plan(output) != plan or json.loads((output / 'runtime.json').read_text()) != checked:
                    raise ValueError('Continuation changed while acquiring lock')
            else:
                write_json(output / 'plan.json', plan)
                write_json(output / 'runtime.json', checked)
            generate = run.opencode.generate if args.ablation == '1' else run.generate
            run_jobs(plan, args, output, run.cell_inputs, generate, campaign.execute_cell)
