"""Prepare instruction-only inputs from archived NLI prompts; never call APIs."""
import argparse
import difflib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.shared.common import HERE, ROOT, encoded, sha

BASE = HERE / 'initial_provider' / 'by_instruction'


def instruction(task, provider):
    primary = next(c for c in task['components'] if c.get('is_primary'))
    return f"Implement the initial file {primary['file']} using {provider}."


def prompt_for(original, task, provider):
    first, separator, rest = original.partition('\n')
    if not separator:
        raise ValueError('Expected multiline archived prompt')
    return first + '\n' + instruction(task, provider) + '\n' + rest


def desired_files(archive):
    config = json.loads((BASE / 'config.json').read_text())
    tasks = {t['primary_atomic_scenario']: t for t in
             (json.loads(line) for line in (ROOT / 'code/benchmark/vibench/agentic/tasks.jsonl').read_text().splitlines() if line.strip())}
    out = {}
    for sid in config['scenarios']:
        task = tasks[sid]
        reference = None
        archived_components = None
        for model in config['models']:
            path = archive / model / f'agentic_{sid}__free__c1/_meta.json'
            meta = json.loads(path.read_text())
            original_fields = {k: meta[k] for k in ('prompt_text', 'system_prompt', 'opencode_agent_prompt')}
            if reference is not None and reference != original_fields:
                raise ValueError(f'Archived prompts differ across models in {sid}')
            reference = original_fields
            components = [{k: v for k, v in c.items() if k != 'is_seeded'} for c in meta['components']]
            keys = ('file', 'role', 'description', 'component_group', 'atomic_scenario')
            signatures = lambda rows: [{k: c.get(k) for k in keys} for c in rows]
            if signatures(components) != signatures(task['components']) or meta['expected_files'] != task['expected_files']:
                raise ValueError(f'Archived task mismatch: {sid}/{model}')
            if archived_components is not None and components != archived_components:
                raise ValueError(f'Archived components differ across models: {sid}')
            archived_components = components
        # Retain historical eligibility annotations rather than newer catalog edits.
        task['components'] = archived_components
        original = reference['prompt_text']
        for key, name in [('prompt_text', 'original_prompt.txt'), ('system_prompt', 'system_prompt.txt'), ('opencode_agent_prompt', 'opencode_agent_prompt.txt')]:
            out[f'initial_provider/by_instruction/sources/{sid}/{name}'] = reference[key]
        out[f'initial_provider/by_instruction/sources/{sid}/agentic_task.json'] = encoded(task)
        for condition, provider in config['conditions'].items():
            ecosystem = condition.removeprefix('instruct_')
            if not task['coverage']['providers'][ecosystem]['eligible']:
                raise ValueError(f'{ecosystem} not eligible for {sid}')
            prompt = prompt_for(original, task, provider)
            out[f'initial_provider/by_instruction/{condition}/{sid}/prompt.txt'] = prompt
            out[f'initial_provider/by_instruction/{condition}/{sid}/metadata.json'] = encoded({
                'scenario': sid, 'condition': condition, 'assigned_provider': ecosystem,
                'primary_file': task['primary_component_file'], 'seed_file': None,
                'prompt_sha256': sha(prompt), 'original_prompt_sha256': sha(original),
                'system_sha256': sha(reference['system_prompt']),
                'task_sha256': sha(encoded(task)), 'expected_generated_files': task['expected_files'],
                'instruction': instruction(task, provider),
            })
            out[f'diffs/initial_provider/by_instruction/{sid}_{condition}.diff'] = ''.join(difflib.unified_diff(
                original.splitlines(keepends=True), prompt.splitlines(keepends=True),
                fromfile=f'original/{sid}/prompt.txt', tofile=f'{condition}/{sid}/prompt.txt'))
    return out


def materialize(files):
    conflicts = [name for name, content in files.items() if (HERE / name).exists() and (HERE / name).read_text() != content]
    if conflicts:
        raise ValueError('Refusing to overwrite changed inputs: ' + ', '.join(conflicts[:5]))
    for name, content in files.items():
        path = HERE / name
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive-root', type=Path, required=True, help='Original raw/agentic directory')
    args = parser.parse_args()
    files = desired_files(args.archive_root)
    materialize(files)
    print(f'Prepared {len(files)} input/diff files; no model calls.')
