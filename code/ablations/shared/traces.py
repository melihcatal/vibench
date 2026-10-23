"""Read-only OpenCode trace export and conservative anchor timing audit."""
import json
import os
from pathlib import Path
import sqlite3

from .common import sha

def trace_database():
    return Path(os.environ.get('XDG_DATA_HOME', str(Path.home() / '.local/share'))) / 'opencode/opencode.db'


def export_trace(database, workspace):
    """Export this workspace's sessions and descendants, never unrelated sessions."""
    with sqlite3.connect(Path(database).resolve().as_uri() + '?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        sessions = [dict(row) for row in db.execute('SELECT * FROM session WHERE directory=?', (str(workspace),))]
        seen = {row['id'] for row in sessions}
        pending = list(seen)
        while pending:
            parent = pending.pop()
            for row in db.execute('SELECT * FROM session WHERE parent_id=?', (parent,)):
                if row['id'] not in seen:
                    sessions.append(dict(row))
                    seen.add(row['id'])
                    pending.append(row['id'])
        result = {'sessions': sessions, 'messages': [], 'parts': []}
        for sid in sorted(seen):
            for table, key in [('message', 'messages'), ('part', 'parts')]:
                for row in db.execute(f'SELECT * FROM {table} WHERE session_id=?', (sid,)):
                    entry = dict(row)
                    entry['data'] = json.loads(entry['data'])
                    result[key].append(entry)
        return result


def audit_anchor(trace, workspace, seed_name, initial, final):
    if seed_name is None:
        return {'applicable': False}
    anchor = workspace / seed_name
    reads, write_turns, writes = [], [], []
    uncertain = False
    messages = {m['id']: m['data'] for m in trace.get('messages', [])}
    for row in trace.get('parts', []):
        data = row['data']
        if data.get('type') != 'tool':
            continue
        tool, state = data.get('tool'), data.get('state') or {}
        inp, timing = state.get('input') or {}, state.get('time') or {}
        name = inp.get('filePath')
        path = (workspace / name).resolve() if isinstance(name, str) else None
        if tool in ('bash', 'task', 'apply_patch'):
            uncertain = True
        if tool == 'read' and path == anchor.resolve() and state.get('status') == 'completed':
            if timing.get('end') is not None:
                reads.append(timing['end'])
        if tool in ('write', 'edit'):
            if path == anchor.resolve():
                writes.append({'tool': tool, 'status': state.get('status'), 'time': timing})
            elif path is not None and path.suffix == '.py':
                turn = (messages.get(row['message_id'], {}).get('time') or {}).get('created')
                if turn is None:
                    uncertain = True
                else:
                    write_turns.append(turn)
    # A read and write requested in the same assistant turn do not establish exposure.
    verified = None if uncertain or not write_turns else bool(reads and min(reads) < min(write_turns))
    return {'applicable': True, 'final_hash_matches': final is not None and sha(initial) == sha(final),
            'successful_read_events': len(reads), 'read_before_generation_verified': verified,
            'anchor_write_attempts': writes, 'unsupported_activity': uncertain,
            'protection': 'prompt instruction plus audit; not filesystem enforcement'}
