"""Materialize paired anchor inputs without invoking models or cloud services."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.shared.common import MODELS, SCENARIOS, STUDY

HERE = Path(__file__).resolve().parents[3]
ROOT = HERE.parents[1]
CONDITIONS = ('anchor_google', 'anchor_aws')
PACKAGES = {
    'aws': {s: 'boto3' for s in SCENARIOS},
    'google': {'S03': 'google-cloud-translate', 'S04': 'google-cloud-speech',
               'S10': 'google-genai', 'S11': 'google-genai',
               'S12': 'google-cloud-vision', 'S20': 'google-cloud-logging'},
}
CONTRACTS = {
    'S03': {'payload': ['text', 'source_language', 'target_language'],
            'output': ['text', 'source_language', 'target_language'],
            'aws_config': ['region (optional)'],
            'google_config': ['project_id', 'location (optional, global)']},
    'S04': {'payload': ['audio_uri', 'language_code'], 'output': ['job_id', 'status'],
            'aws_config': ['region (optional)', 'job_name (optional)'],
            'google_config': [],
            'preconditions': 'Use matched audio hosted in S3 / Cloud Storage respectively. Google input must have a supported self-describing header (e.g. FLAC/WAV). A1 submits only; the generated remaining workflow includes polling and transcript processing.'},
    'S10': {'payload': ['text'], 'output': ['text'],
            'aws_config': ['region (optional)'],
            'google_config': ['api_key or GOOGLE_API_KEY'],
            'model_ids': {'aws': 'amazon.nova-pro-v1:0', 'google': 'gemini-2.5-flash'},
            'preconditions': 'Verify access and availability of the fixed first-party model IDs before execution.'},
    'S11': {'payload': ['text'], 'output': ['text'],
            'aws_config': ['region (optional, us-east-1)'],
            'google_config': ['project_id', 'location'],
            'model_ids': {'aws': 'us.amazon.nova-pro-v1:0', 'google': 'gemini-2.5-flash'},
            'preconditions': 'Google uses google-genai in Vertex AI mode with ADC, an enabled project/location and access to gemini-2.5-flash. Historical evidence names vertexai; the SDK migration is explicitly recorded.'},
    'S12': {'payload': ['image_bytes'], 'output': ['labels: [{name, confidence in [0,1]}]'],
            'aws_config': ['region (optional)', 'max_labels (optional, 10)'],
            'google_config': ['max_labels (optional, 10)']},
    'S20': {'payload': ['event (JSON object)', 'timestamp_ms (optional)'],
            'output': ['submitted'], 'aws_config': ['log_group', 'log_stream', 'region (optional)'],
            'google_config': ['project_id', 'log_name'],
            'preconditions': 'Pre-provision the AWS log group/stream; configure permissions for both services. A1 writes one event; the generated remaining workflow includes log querying.'},
}
from ablations.initial_provider.assigned_as_code.scripts.expanded_specs import EXTRA_CONTRACTS, EXTRA_PACKAGES
CONTRACTS.update(EXTRA_CONTRACTS)
for provider, packages in EXTRA_PACKAGES.items():
    PACKAGES[provider].update(packages)
S11_MIGRATION = {
    'from_sdk': 'vertexai.generative_models (google-cloud-aiplatform)',
    'to_sdk': 'google-genai', 'mode': 'vertexai=True', 'model': 'gemini-2.5-flash',
    'reason': 'User-approved migration of deprecated generative SDK; same Vertex AI provider, task, function signature and output.',
    'documentation': 'https://googleapis.github.io/python-genai/',
    'validation': 'Offline request/response contract tests; not a live Vertex service execution.'}


def digest(content):
    return hashlib.sha256(content.encode()).hexdigest()


def encoded(value):
    return json.dumps(value, indent=2, ensure_ascii=True) + '\n'


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def prompt_for(task, condition, original=None):
    sid = task['primary_atomic_scenario']
    primary = next(c for c in task['components'] if c.get('is_primary'))
    if original is None:
        original = (HERE / 'paper_inputs' / sid / 'original_prompt.txt').read_text()
    if condition == 'no_anchor':
        return original
    first, separator, rest = original.partition('\n')
    assert separator, 'Expected a multiline archived prompt'
    notice = (f"The initial file {primary['file']} is already implemented. "
              'Read it before generating the remaining files, and leave it unchanged.')
    return first + '\n' + notice + '\n' + rest


def make_sources(archive_root=None):
    if archive_root is None:
        out = {p.relative_to(HERE).as_posix(): p.read_text()
               for p in (HERE / 'paper_inputs').rglob('*') if p.is_file()}
        direct = {r['scenario_id']: r for r in load_jsonl(ROOT / 'code/benchmark/vibench/vibench.jsonl') if r.get('stage') == 'direct'}
        for sid in SCENARIOS:
            for name in ('original_prompt.txt', 'system_prompt.txt', 'opencode_agent_prompt.txt', 'agentic_task.json'):
                key = f'paper_inputs/{sid}/{name}'
                if key not in out:
                    out[key] = (HERE / 'initial_provider/by_instruction/sources' / sid / name).read_text()
            key = f'paper_inputs/{sid}/scenario.json'
            if key not in out:
                out[key] = encoded(direct[sid])
        return out
    benchmark = ROOT / 'code/benchmark/vibench'
    direct = {r['scenario_id']: r for r in load_jsonl(benchmark / 'vibench.jsonl') if r.get('stage') == 'direct'}
    agentic = {r['primary_atomic_scenario']: r for r in load_jsonl(benchmark / 'agentic/tasks.jsonl')}
    models = {m['id'] for m in json.loads((benchmark / 'models.json').read_text())['models']}
    assert all(m in models for group in MODELS.values() for m in group)
    out = {}
    for s in SCENARIOS:
        for model in [m for group in MODELS.values() for m in group]:
            meta = json.loads((archive_root / model / f'agentic_{s}__free__c1/_meta.json').read_text())
            for source_key, filename in [('prompt_text', 'original_prompt.txt'),
                                         ('system_prompt', 'system_prompt.txt'),
                                         ('opencode_agent_prompt', 'opencode_agent_prompt.txt')]:
                key = f'paper_inputs/{s}/{filename}'
                value = meta[source_key]
                if key in out and out[key] != value:
                    raise ValueError(f'Original {filename} differs across selected models in {s}')
                out[key] = value
        out[f'paper_inputs/{s}/scenario.json'] = encoded(direct[s])
        out[f'paper_inputs/{s}/agentic_task.json'] = encoded(agentic[s])
        out[f'paper_inputs/{s}/anchor_contract.json'] = encoded(CONTRACTS[s])
    return out


def desired_files(archive_root=None):
    out = make_sources(archive_root)
    cells = []
    for s in SCENARIOS:
        task = json.loads(out[f'paper_inputs/{s}/agentic_task.json'])
        scenario = json.loads(out[f'paper_inputs/{s}/scenario.json'])
        primary = next(c for c in task['components'] if c.get('is_primary'))
        downstream = [c for c in task['components'] if c['component_group'] == 'downstream']
        out[f'paper_inputs/{s}/anchor_contract.json'] = encoded(CONTRACTS[s])
        for condition in CONDITIONS:
            provider = condition.removeprefix('anchor_') if condition != 'no_anchor' else None
            original = out[f'paper_inputs/{s}/original_prompt.txt']
            text = prompt_for(task, condition, original)
            if provider:
                out[f'diffs/initial_provider/assigned_as_code/{s}_{condition}.diff'] = ''.join(difflib.unified_diff(
                    original.splitlines(keepends=True), text.splitlines(keepends=True),
                    fromfile=f'original/{s}/prompt.txt', tofile=f'{condition}/{s}/prompt.txt'))
            anchor = (HERE / 'anchor_files' / condition / s / 'a1.py').read_text() if provider else None
            evidence = next(t for t in scenario['provider_tools'] if t['provider_key'] == provider) if provider else None
            if evidence:
                assert evidence['eligible']
            for role, models in MODELS.items():
                for model in models:
                    base = f'initial_provider/assigned_as_code/{condition}/{s}/models/{role}/{model}'
                    out[f'{base}/prompt.txt'] = text
                    out[f'{base}/system_prompt.txt'] = out[f'paper_inputs/{s}/system_prompt.txt']
                    if anchor:
                        out[f"{base}/workspace/{primary['file']}"] = anchor
                        out[f'{base}/requirements.txt'] = PACKAGES[provider][s] + '\n'
                    meta = {
                        'scenario': s, 'condition': condition, 'model_id': model, 'role': role,
                        'prompt_variant': 'original_NLI_plus_seed_notice' if anchor else 'original_NLI_free_generation',
                        'source_task_id': task['task_id'], 'original_anchor_file': primary['file'],
                        'workspace_dir': 'workspace',
                        'seed_file': primary['file'] if anchor else None,
                        'seed_provider': provider, 'seed_sha256': digest(anchor) if anchor else None,
                        'prompt_sha256': digest(text),
                        'system_prompt_sha256': digest(out[f'paper_inputs/{s}/system_prompt.txt']),
                        'original_prompt_sha256': digest(out[f'paper_inputs/{s}/original_prompt.txt']),
                        'expected_generated_files': [c['file'] for c in task['components']
                                                     if not anchor or not c.get('is_primary')],
                        'expected_repository_files': [c['file'] for c in task['components']],
                        'downstream_atomic_scenarios': {c['file']: c['atomic_scenario'] for c in downstream},
                        'scored_files': [c['file'] for c in downstream],
                        'input_contract': CONTRACTS[s], 'evidence': evidence,
                        'dependency_package': PACKAGES[provider][s] if provider else None,
                        'sdk_migration': S11_MIGRATION if provider == 'google' and s == 'S11' else None,
                        'status': 'prepared_not_live_validated',
                    }
                    out[f'{base}/metadata.json'] = encoded(meta)
                    cells.append({'path': base, 'scenario': s, 'condition': condition,
                                  'model_id': model, 'role': role})
    manifest = {'status': 'prepared_not_executed', 'scenarios': SCENARIOS, 'models': MODELS,
                'conditions': CONDITIONS, 'proposed_repetitions': STUDY['repetitions'],
                'input_cells': len(cells), 'proposed_runs': len(cells) * STUDY['repetitions'], 'cells': cells,
                'source_sha256': {k: digest(out[k]) for k in sorted(out) if k.startswith('sources/')},
                'template_sha256': {p.relative_to(HERE).as_posix(): digest(p.read_text())
                                    for p in sorted((HERE / 'anchor_files').rglob('a1.py'))}}
    out['initial_provider/assigned_as_code/manifest.json'] = encoded(manifest)
    return out


def materialize(files, refresh=False):
    conflicts = [name for name, content in files.items()
                 if (HERE / name).exists() and (HERE / name).read_text() != content]
    if conflicts and not refresh:
        raise RuntimeError('Refusing to overwrite changed files: ' + ', '.join(conflicts[:10]))
    obsolete_seeds = []
    if refresh:
        for name in files:
            if not name.startswith('initial_provider/assigned_as_code/') or not name.endswith('/metadata.json'):
                continue
            metadata_path = HERE / name
            if not metadata_path.exists():
                continue
            old = json.loads(metadata_path.read_text())
            seed_name = old.get('seed_file')
            if not seed_name:
                continue
            if Path(seed_name).name != seed_name:
                raise RuntimeError('Seed cleanup requires a simple relative filename')
            workspace = old.get('workspace_dir', '.')
            if workspace not in ('.', 'workspace'):
                raise RuntimeError('Seed cleanup requires a known workspace directory')
            old_path = metadata_path.parent / workspace / seed_name
            if old_path.relative_to(HERE).as_posix() not in files and old_path.exists():
                if digest(old_path.read_text()) != old['seed_sha256']:
                    raise RuntimeError(f'Refusing to remove edited seed: {old_path}')
                obsolete_seeds.append(old_path)
    for name, content in files.items():
        path = HERE / name
        if not path.exists() or (refresh and path.read_text() != content):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    for path in obsolete_seeds:
        path.unlink()
    # Empty no-anchor workspaces cannot be represented by a tracked placeholder.
    for name in files:
        if name.startswith('initial_provider/assigned_as_code/') and name.endswith('/metadata.json'):
            (HERE / name).parent.joinpath('workspace').mkdir(exist_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive-root', type=Path, help='Original raw/agentic directory; needed only for initial source snapshots')
    parser.add_argument('--refresh-generated', action='store_true', help='Explicitly overwrite generated inputs after reviewing template changes; never use on edited run outputs')
    args = parser.parse_args()
    outputs = desired_files(args.archive_root)
    materialize(outputs, refresh=args.refresh_generated)
    print(f"Checked/materialized {len(outputs)} files; {json.loads(outputs['initial_provider/assigned_as_code/manifest.json'])['input_cells']} cells; no generations executed.")
