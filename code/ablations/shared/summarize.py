"""Summarize a campaign using first attempts, never selecting successful retries."""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ablations.shared.attempts import cell_key


def summarize(campaign):
    plan = json.loads((campaign / 'plan.json').read_text())
    rows = defaultdict(lambda: {'planned': 0, 'attempted': 0, 'completed': 0, 'failed': 0,
                               'unfinished': 0, 'retries': 0, 'anchor_read_unverified': 0})
    for cell in plan['cells']:
        key = (cell['condition'], cell['model'])
        row = rows[key]
        row['planned'] += 1
        attempts = sorted((campaign / 'runs' / cell_key(cell)).glob('attempt_*'))
        if not attempts:
            continue
        row['attempted'] += 1
        row['retries'] += len(attempts) - 1
        status_path = attempts[0] / 'status.json'
        status = json.loads(status_path.read_text()) if status_path.exists() else {}
        state = status.get('state')
        row[state if state in ('completed', 'failed') else 'unfinished'] += 1
        row['anchor_read_unverified'] += bool(status.get('anchor_read_unverified'))
    lines = ['First-attempt inventory. Completed means execution/output checks passed, not technical correctness.',
             '', '| Condition | Model | Planned | Attempted | Completed | Failed | Unfinished | Extra attempts | Anchor read unverified |',
             '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for (condition, model), row in sorted(rows.items()):
        values = ' | '.join(str(v) for v in row.values())
        lines.append(f'| {condition} | {model} | {values} |')
    return '\n'.join(lines)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('campaign', type=Path)
    args = parser.parse_args()
    print(summarize(args.campaign))
