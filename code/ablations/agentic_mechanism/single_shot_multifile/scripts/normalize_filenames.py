"""Derive filename-normalized artifacts without modifying raw attempts or code."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.shared.common import timestamp, write_json

PREFIXES = ('[SAME-SCENARIO] ', '[HELPER] ', '[LATER-STEP] ',
            'SAME-SCENARIO/', 'HELPER/', 'LATER-STEP/')


def normalize_response(text, expected):
    if not isinstance(text, str):
        raise ValueError('Missing response text')
    expected = set(expected)
    if any(Path(name).name != name or name in ('.', '..') for name in expected):
        raise ValueError('Expected filenames must be plain basenames')
    lines = text.strip().splitlines()
    if len(lines) >= 3 and lines[0] in ('```json', '```') and lines[-1] == '```':
        text = '\n'.join(lines[1:-1])

    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate filename: {key}')
            result[key] = value
        return result

    parsed = json.loads(text, object_pairs_hook=unique_pairs)
    if not isinstance(parsed, dict):
        raise ValueError('Expected filename-to-source JSON object')
    files, mapping = {}, {}
    for original, source in parsed.items():
        name = original
        if name not in expected:
            for prefix in PREFIXES:
                if name.startswith(prefix):
                    name = name[len(prefix):]
                    break
        if name not in expected:
            raise ValueError(f'Unexpected filename: {original}')
        if name in files:
            raise ValueError(f'Filename collision after normalization: {name}')
        if not isinstance(source, str):
            raise ValueError(f'Source must be a string: {original}')
        files[name] = source
        if original != name:
            mapping[original] = name
    if set(files) != expected:
        raise ValueError(f'Missing filenames: {sorted(expected - set(files))}')
    return files, mapping


def derive(campaign):
    from ablations.shared.scoring import score_files

    campaign = campaign.resolve()
    plan = json.loads((campaign / 'plan.json').read_text())
    if str(plan['ablation']) != '2':
        raise ValueError('This normalization is only for ablation 2')
    statuses = sorted((campaign / 'runs').glob('*/*/single_shot/*/attempt_*/status.json'))
    if not statuses or any(json.loads(p.read_text())['state'] == 'running' for p in statuses):
        raise ValueError('Require saved, finished single-shot attempts')
    output = campaign / 'filename_normalized'
    output.mkdir(exist_ok=False)
    counts, records = defaultdict(Counter), []
    for status_path in statuses:
        attempt = status_path.parent
        relative = attempt.relative_to(campaign)
        status = json.loads(status_path.read_text())
        data = json.loads((attempt / 'input.json').read_text())
        model = data['cell']['model']
        record = {'source_attempt': str(relative), 'model': model,
                  'original_state': status['state']}
        target = output / relative
        target.mkdir(parents=True)
        try:
            response_path = attempt / 'response.json'
            record['response_sha256'] = hashlib.sha256(response_path.read_bytes()).hexdigest()
            response = json.loads(response_path.read_text())
            if response.get('error'):
                raise ValueError('API error in original response; no filename repair attempted')
            files, mapping = normalize_response(response.get('output_text'), data['task']['expected_files'])
        except (ValueError, OSError) as exc:
            record.update(state='unresolved', error=f'{type(exc).__name__}: {exc}')
        else:
            repository = target / 'repository'
            repository.mkdir()
            for name, source in files.items():
                (repository / name).write_bytes(source.encode('utf-8'))
            metrics = score_files(data['task'], files)
            write_json(target / 'metrics.json', metrics)
            record.update(state='normalized' if mapping else 'unchanged', filename_mapping=mapping,
                          source_content_unchanged=True,
                          missing_or_empty=[name for name, source in files.items() if not source.strip()],
                          source_sha256={name: hashlib.sha256(source.encode('utf-8')).hexdigest()
                                         for name, source in files.items()})
        counts[model][record['state']] += 1
        records.append(record)
        write_json(target / 'normalization.json', record)
    summary = {'created': timestamp(), 'source_campaign': str(campaign),
               'normalizer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'policy': 'Strip only the six listed role prefixes from JSON keys; exact expected filename set and no collisions required. Source strings are not edited or syntax-filtered.',
               'prefixes': PREFIXES, 'counts': dict(counts), 'attempts': records}
    write_json(output / 'summary.json', summary)
    print(json.dumps({'output': str(output), 'counts': dict(counts)}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--campaign', type=Path, required=True)
    derive(parser.parse_args().campaign)
