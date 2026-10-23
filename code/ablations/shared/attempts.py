"""Preserve all attempts, audit input hashes, and save per-run artifacts."""
import json
import time

from .common import encoded, redact, sha, timestamp, write_json
from .runtime import agentic
from .scoring import score_files
from .sampling_audit import audit_sampling

def cell_key(cell):
    return f"{cell['scenario']}/{cell['model']}/{cell['condition']}/r{cell['repetition']:03d}"


def next_attempt(cell_dir, resume=False, retry_failed=False):
    previous = sorted(cell_dir.glob('attempt_*')) if cell_dir.exists() else []
    if previous:
        if not resume:
            raise ValueError(f'Existing attempts at {cell_dir}; use --resume')
        status_path = previous[-1] / 'status.json'
        status = json.loads(status_path.read_text()) if status_path.exists() else {'state': 'interrupted'}
        if status['state'] == 'completed' or not retry_failed:
            return None
    path = cell_dir / f'attempt_{len(previous) + 1:03d}'
    path.mkdir(parents=True, exist_ok=False)
    return path


def execute_cell(plan, cell, attempt, database, data, generate):
    actual_hashes = {'prompt_sha256': sha(data['prompt']), 'system_sha256': sha(data['system']),
                     'task_sha256': sha(encoded(data['task'])),
                     'seed_sha256': sha(data['seed']) if data['seed'] is not None else None}
    if any(cell[key] != value for key, value in actual_hashes.items()):
        raise ValueError('Inputs changed after the campaign plan was created; refusing model call')
    model = agentic.load_models(cell['model'])[0]
    (attempt / 'prompt.txt').write_text(data['prompt'])
    (attempt / 'system_prompt.txt').write_text(data['system'])
    write_json(attempt / 'input.json', redact({'cell': cell, 'task': data['task'], 'model': model}))
    write_json(attempt / 'status.json', {'state': 'running', 'started': timestamp()})
    outcome = {'response': {}, 'files': {}, 'audit': {}, 'errors': []}
    started = time.monotonic()
    try:
        generate(data, model, plan, attempt, database, outcome)
    except Exception as exc:
        outcome['errors'].append(f'{type(exc).__name__}: {exc}')
    finally:
        repository = attempt / 'repository'
        repository.mkdir(exist_ok=True)
        for name, content in outcome['files'].items():
            (repository / name).write_text(redact(content))
        write_json(attempt / 'response.json', redact(outcome['response']))
    result, contents = outcome['response'], outcome['files']
    errors, audit = outcome['errors'], outcome['audit']
    if result.get('error'):
        errors.append(str(result['error']))
    expected_generated = set(data['task']['expected_files']) - {data['seed_file']}
    missing = sorted(name for name in expected_generated if not contents.get(name, '').strip())
    if missing:
        errors.append('Missing or empty generated files: ' + ', '.join(missing))
    if data['seed_file'] and contents.get(data['seed_file']) != data['seed']:
        errors.append('Supplied anchor changed or missing')
    if any(event['status'] == 'completed' for event in audit.get('anchor_write_attempts', [])):
        errors.append('Trace records a completed anchor write/edit, even if final contents were restored')
    write_json(attempt / 'metrics.json', score_files(data['task'], contents))
    sampling_audit = audit_sampling(model, plan['sampling'], result, attempt / 'trace.json')
    write_json(attempt / 'sampling_audit.json', sampling_audit)
    status = {'state': 'failed' if errors else 'completed', 'finished': timestamp(),
              'elapsed_seconds': round(time.monotonic() - started, 3), 'errors': redact(errors),
              'missing_generated_files': missing,
              'anchor_read_unverified': bool(data['seed_file'] and audit.get('read_before_generation_verified') is not True),
              'sampling_warnings': sampling_audit['warnings']}
    write_json(attempt / 'status.json', status)
    return status
