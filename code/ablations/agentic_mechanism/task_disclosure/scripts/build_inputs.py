"""Build independent file requests from archived descriptions; no API calls."""
import difflib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.shared.common import HERE, encoded, sha, write_json
from ablations.shared.runtime import agentic

BASE = HERE / 'agentic_mechanism' / 'task_disclosure'
SOURCE = HERE / 'initial_provider' / 'by_instruction' / 'sources'
LABELS = {'aligned_core': 'SAME-SCENARIO', 'aligned_context': 'HELPER', 'downstream': 'LATER-STEP'}


def configuration():
    return json.loads((BASE / 'config.json').read_text())


def single_file_system(original):
    replacements = {
        'You are an autonomous coding agent generating a small multi-file Python integration project.':
            'You are a coding agent generating Python integration code.',
        '- Create exactly the requested files and no extra files.':
            '- Create only the requested file and no extra files.',
        'for each scored component.': 'for each service integration.',
        'Every scored file must visibly contain or import':
            'Service-integration code must visibly contain or import',
    }
    for old, new in replacements.items():
        if original.count(old) != 1:
            raise ValueError('Unrecognized system instruction: ' + old)
        original = original.replace(old, new)
    return original


def single_file_agent_prompt(system):
    prompt = agentic._build_opencode_agent_prompt(system)
    replacements = {
        'You generate Python code for multi-file coding tasks.': 'You generate Python code for coding tasks.',
        'Multi-file implementation requirements:': 'Implementation requirements:',
        '- Keep file interfaces and data shapes compatible across the requested files.\n': '',
        '- Write only the requested Python files. Do not put explanations, markdown fences, comments, docstrings, or example usage in those files.':
            '- Write only the requested Python file. Do not put explanations, markdown fences, comments, docstrings, or example usage in that file.',
        '- Write files only in the current working directory, using exactly the relative filenames requested by the user task.':
            '- Write the file only in the current working directory, using exactly the relative filename requested by the user task.',
    }
    for old, new in replacements.items():
        if prompt.count(old) != 1:
            raise ValueError('Unrecognized agent instruction: ' + old)
        prompt = prompt.replace(old, new)
    return prompt


def catalog(task):
    components = {c['file']: c for c in task['components']}
    return ('Task specifications (listed alphabetically; implement only the requested file):\n'
            + '\n'.join(f"{name} - {components[name]['description']}" for name in sorted(components)) + '\n\n')


def make_prompts(task, original, condition):
    if condition not in ('full_disclosure', 'staged_disclosure'):
        raise ValueError('Unknown disclosure condition')
    components = {c['file']: c for c in task['components']}
    names = task['expected_files']
    if len(names) != 10 or len(set(names)) != 10 or set(names) != set(components):
        raise ValueError('Expected ten unique component filenames')
    if names[0] != task['primary_component_file'] or any(Path(n).name != n or not n.endswith('.py') for n in names):
        raise ValueError('Invalid initial file or relative filename')
    specs = [f"[{LABELS[components[n]['component_group']]}] {n} - {components[n]['description']}" for n in names]
    # Require literal archived specifications, not a rewritten task paraphrase.
    if any(spec not in original for spec in specs):
        raise ValueError('Task specification differs from archived user prompt')
    prompts = []
    for name in names:
        component = components[name]
        prefix = catalog(task) if condition == 'full_disclosure' else ''
        prompt = (prefix + f'Create {name} in the current working directory.\n'
                  f"Task: {component['description']}.\n")
        if component['is_scored']:
            prompt += 'Use one concrete external provider and make that provider identifiable in code.\n'
        prompts.append(prompt)
    return prompts


def build():
    cfg = configuration()
    if cfg['file_order'] != 'archived_expected_files' or cfg['timeout_scope'] != 'whole_repository_run' or cfg['conversation_mode'] != 'fresh_session_per_file':
        raise ValueError('Unsupported protocol configuration')
    for sid in cfg['scenarios']:
        source, target = SOURCE / sid, BASE / 'sources' / sid
        target.mkdir(parents=True, exist_ok=True)
        for name in ('original_prompt.txt', 'agentic_task.json', 'system_prompt.txt', 'opencode_agent_prompt.txt'):
            (target / name).write_text((source / name).read_text())
        for name in ('system_prompt.txt', 'opencode_agent_prompt.txt'):
            (target / ('original_' + name)).write_text((source / name).read_text())
        system = single_file_system((source / 'system_prompt.txt').read_text())
        (target / 'system_prompt.txt').write_text(system)
        (target / 'opencode_agent_prompt.txt').write_text(single_file_agent_prompt(system))
        task = json.loads((target / 'agentic_task.json').read_text())
        original = (target / 'original_prompt.txt').read_text()
        variants = {}
        for condition in cfg['conditions']:
            prompts = make_prompts(task, original, condition)
            variants[condition] = prompts
            cell = BASE / condition / sid
            cell.mkdir(parents=True, exist_ok=True)
            for i, prompt in enumerate(prompts, 1):
                (cell / f'prompt_{i:02d}.txt').write_text(prompt)
            write_json(cell / 'metadata.json', {
                'condition': condition, 'file_order': task['expected_files'],
                'source_sha256': {p.name: sha(p.read_text()) for p in sorted(target.iterdir()) if p.is_file()},
                'prompt_sha256': [sha(p) for p in prompts], 'prompt_bundle_sha256': sha(encoded(prompts))})
            diff = ''.join(difflib.unified_diff(original.splitlines(True), prompts[0].splitlines(True),
                                               fromfile='original_prompt.txt', tofile=f'{condition}/prompt_01.txt'))
            dest = HERE / 'diffs' / 'task_disclosure'
            dest.mkdir(parents=True, exist_ok=True)
            (dest / f'{sid}_{condition}.diff').write_text(diff)
        (dest / f'{sid}_disclosure_contrast.diff').write_text(''.join(difflib.unified_diff(
            variants['full_disclosure'][0].splitlines(True), variants['staged_disclosure'][0].splitlines(True),
            fromfile='full_disclosure/prompt_01.txt', tofile='staged_disclosure/prompt_01.txt')))
        for name in ('system_prompt.txt', 'opencode_agent_prompt.txt'):
            (dest / f'{sid}_{name}.diff').write_text(''.join(difflib.unified_diff(
                (target / ('original_' + name)).read_text().splitlines(True), (target / name).read_text().splitlines(True),
                fromfile='original/' + name, tofile='agentic_mechanism/task_disclosure/' + name)))
    print(f"Built {len(cfg['scenarios'])} scenarios x 2 conditions x 10 prompts; no model calls.")


if __name__ == '__main__':
    build()
