"""Run ablation 3: instruct the provider for A1 without supplying any code."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.shared import campaign, configuration as run_config, opencode, scoring
from ablations.shared.common import HERE, encoded, sha, write_json
from ablations.shared.runtime import agentic

BASE = HERE / 'initial_provider' / 'by_instruction'
DEFAULT_CONFIG = BASE / 'config.yaml'


def configuration():
    return json.loads((BASE / 'config.json').read_text())


def cell_inputs(condition, scenario, model):
    config = configuration()
    if condition not in config['conditions'] or scenario not in config['scenarios'] or model not in config['models']:
        raise ValueError('Unknown ablation 3 condition, scenario, or model')
    source = BASE / 'sources' / scenario
    cell = BASE / condition / scenario
    task = json.loads((source / 'agentic_task.json').read_text())
    meta = json.loads((cell / 'metadata.json').read_text())
    prompt, system = (cell / 'prompt.txt').read_text(), (source / 'system_prompt.txt').read_text()
    if sha(prompt) != meta['prompt_sha256'] or sha(system) != meta['system_sha256'] or sha(encoded(task)) != meta['task_sha256']:
        raise ValueError('Ablation 3 input hash mismatch')
    if agentic._build_opencode_agent_prompt(system) != (source / 'opencode_agent_prompt.txt').read_text():
        raise ValueError('Agent instructions differ from archived instructions')
    task['seed_files'] = []
    task['assigned_initial_provider'] = meta['assigned_provider']
    return {'task': task, 'prompt': prompt, 'system': system, 'seed': None, 'seed_file': None}


def generate(data, model, plan, attempt, database, outcome):
    opencode.generate(data, model, plan, attempt, database, outcome)
    scores = scoring.score_files(data['task'], outcome['files'])
    primary = data['task']['primary_component_file']
    assigned = data['task']['assigned_initial_provider']
    audit = {'assigned_provider': assigned, 'primary_file': primary,
             'primary_present': bool(outcome['files'].get(primary, '').strip()),
             'generation_order': 'not_inferred_from_file_role; inspect trace.json'}
    for mode in ('explicit', 'propagated'):
        labels = scores['file_labels_' + mode][primary]['detected_ecosystems']
        audit[mode] = {'labels': labels, 'includes_assigned': assigned in labels,
                       'exclusively_assigned': set(labels) == {assigned}}
    write_json(attempt / 'assignment_audit.json', audit)


def parser(config_path=DEFAULT_CONFIG):
    config = configuration()
    p = campaign.argument_parser(__doc__, tuple(config['conditions']))
    p.set_defaults(ablation='3', model_choices=config['models'], scenario_choices=config['scenarios'])
    return run_config.configure_parser(p, config_path, config['models'], config['scenarios'], config['conditions'])


def main(argv=None):
    args = run_config.parse_args(parser, DEFAULT_CONFIG, argv)
    campaign.launch(args, tuple(configuration()['conditions']), cell_inputs, generate, lambda plan: True)


if __name__ == '__main__':
    main()
