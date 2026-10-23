"""Trace and snapshot audits; file writes are not latent decision timestamps."""
import ast
from pathlib import Path

from ablations.shared.common import sha


def snapshot(workspace):
    contents, unsafe = {}, []
    for path in sorted(workspace.rglob('*')):
        if path.is_symlink():
            unsafe.append(str(path.relative_to(workspace)))
        elif path.is_file() and path.suffix == '.py':
            contents[str(path.relative_to(workspace))] = path.read_text(errors='replace')
    return contents, unsafe


def missing_local_imports(contents, expected):
    modules = {Path(n).stem: n for n in expected}
    missing = {}
    for name, content in contents.items():
        try:
            tree = ast.parse(content)
        except SyntaxError:
            continue
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(a.name.split('.')[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
                elif node.level:
                    imports.update(a.name for a in node.names)
        absent = sorted(modules[m] for m in imports if m in modules and modules[m] not in contents)
        if absent:
            missing[name] = absent
    return missing


def step_audit(before, after, target, future, unsafe, expected):
    created = sorted(set(after) - set(before))
    revised = sorted(n for n in set(before) & set(after) if before[n] != after[n])
    deleted = sorted(set(before) - set(after))
    return {'requested_file': target, 'requested_file_present': bool(after.get(target, '').strip()),
            'created': created, 'revised': revised, 'deleted': deleted,
            'off_target_changes': sorted((set(created) | set(revised) | set(deleted)) - {target}),
            'future_files_present': sorted(set(after) & set(future)),
            'unexpected_python_files': sorted(set(after) - set(expected)), 'symlinks': unsafe,
            'missing_local_imports': missing_local_imports(after, expected),
            'file_sha256': {n: sha(c) for n, c in after.items()}}


def event_order(trace, workspace, part_steps, expected):
    messages = {m['id']: m['data'] for m in trace.get('messages', [])}
    events, uncertain = [], []
    for row in trace.get('parts', []):
        d = row['data']
        if d.get('type') != 'tool':
            continue
        tool, state = d.get('tool'), d.get('state') or {}
        inp, timing = state.get('input') or {}, state.get('time') or {}
        if tool in ('bash', 'task'):
            uncertain.append({'part': row['id'], 'reason': tool + '_may_mutate_files'})
        if tool not in ('write', 'edit', 'apply_patch'):
            continue
        if state.get('status') != 'completed':
            uncertain.append({'part': row['id'], 'reason': 'incomplete_mutation'})
            continue
        names = [inp.get('filePath')]
        if tool == 'apply_patch':
            names = [f.get('filePath') for f in (state.get('metadata') or {}).get('files', [])]
        if not names:
            uncertain.append({'part': row['id'], 'reason': 'missing_mutation_paths'})
        for name in names:
            if not name:
                uncertain.append({'part': row['id'], 'reason': 'missing_mutation_path'})
                continue
            path = Path(name)
            path = (path if path.is_absolute() else workspace / path).resolve()
            try:
                file = str(path.relative_to(workspace))
            except ValueError:
                uncertain.append({'part': row['id'], 'reason': 'mutation_outside_workspace'})
                continue
            if file not in expected:
                continue
            turn = (messages.get(row['message_id'], {}).get('time') or {}).get('created')
            if turn is None or timing.get('start') is None or timing.get('end') is None:
                uncertain.append({'part': row['id'], 'reason': 'missing_timestamps'})
                continue
            events.append({'file': file, 'tool': tool, 'part': row['id'], 'message': row['message_id'],
                           'step': part_steps.get(row['id']), 'turn_start': turn,
                           'start': timing['start'], 'end': timing['end']})
    events.sort(key=lambda e: (e['start'], e['end'], e['part']))
    return {'events': events, 'uncertain_activity': uncertain,
            'interpretation': 'Observed tool mutations only; same-turn writes do not establish sequential model decisions.'}
