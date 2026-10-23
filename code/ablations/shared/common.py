"""Shared paths, study scope, and artifact serialization."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
STUDY = json.loads((HERE / 'shared' / 'study.json').read_text())
SCENARIOS = tuple(STUDY['scenarios'])
MODELS = {role: tuple(models) for role, models in STUDY['models'].items()}

def timestamp():
    return datetime.now(timezone.utc).isoformat()


def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + '\n'


def write_json(path, value):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(encoded(value))
    tmp.replace(path)


def redact(value):
    """Keep known environment credentials out of saved configs and tool traces."""
    secrets = [v for k, v in os.environ.items() if len(v) >= 8 and
               any(token in k.upper() for token in ('API_KEY', 'SECRET', 'TOKEN', 'PASSWORD', 'ACCESS_KEY'))]
    def walk(item):
        if isinstance(item, dict):
            return {k: '[REDACTED]' if k.lower().replace('_', '') in
                    ('apikey', 'authorization', 'password', 'secret', 'accesstoken') else walk(v)
                    for k, v in item.items()}
        if isinstance(item, list):
            return [walk(v) for v in item]
        if isinstance(item, str):
            for secret in secrets:
                item = item.replace(secret, '[REDACTED]')
        return item
    return walk(value)


def selections(value, choices):
    selected = list(choices) if value == 'all' else value.split(',')
    if not selected or len(set(selected)) != len(selected) or set(selected) - set(choices):
        raise ValueError(f'Expected unique choices from {list(choices)}, got {selected}')
    return selected


# Campaign directories are named for what they test, while the --ablation ids
# stay numeric because they appear in archived run manifests and in the
# analysis snapshots. Map between the two here.
ABLATION_DIRS = {
    '1': 'initial_provider/assigned_as_code',
    '2': 'agentic_mechanism/single_shot_multifile',
    '3': 'initial_provider/by_instruction',
    '4': 'agentic_mechanism/task_disclosure',
}


def ablation_dir(ablation):
    """Directory for an ablation id, including nested ids like '1/microsoft_openai'."""
    head, separator, rest = str(ablation).partition('/')
    name = ABLATION_DIRS[head]
    return f'{name}/{rest}' if separator else name
