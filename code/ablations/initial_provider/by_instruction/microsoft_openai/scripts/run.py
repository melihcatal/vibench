"""Run only A3 Microsoft/OpenAI instructions using the existing agentic runner."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from ablations.shared import campaign, configuration, opencode, scoring
from ablations.shared.common import encoded, sha, write_json
from ablations.shared.runtime import agentic

BASE = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = BASE / 'config.yaml'
CONDITIONS = ('instruct_microsoft_openai',)
MODELS = ('gemini-2.5-flash', 'nova-pro', 'gpt-5.4-mini')
SCENARIOS = tuple(f'S{i:02d}' for i in range(1, 21))


def cell_inputs(condition, scenario, model):
    if condition not in CONDITIONS or scenario not in SCENARIOS or model not in MODELS:
        raise ValueError('Unknown Microsoft/OpenAI extension cell')
    base = BASE / 'inputs' / scenario
    meta = json.loads((base / 'metadata.json').read_text())
    task = json.loads((base / 'agentic_task.json').read_text())
    prompt, system = (base / 'prompt.txt').read_text(), (base / 'system_prompt.txt').read_text()
    if any(sha(content) != meta[key] for content, key in (
            (prompt, 'prompt_sha256'), (system, 'system_sha256'), (encoded(task), 'task_sha256'))):
        raise ValueError('Microsoft/OpenAI input hash mismatch')
    if agentic._build_opencode_agent_prompt(system) != (base / 'opencode_agent_prompt.txt').read_text():
        raise ValueError('Agent instructions differ from archived instructions')
    task['seed_files'] = []
    task['assigned_initial_provider'] = 'microsoft_openai'
    task['anchor_extension'] = meta
    return {'task': task, 'prompt': prompt, 'system': system, 'seed': None, 'seed_file': None}


def generate(data, model, plan, attempt, database, outcome):
    opencode.generate(data, model, plan, attempt, database, outcome)
    scores = scoring.score_files(data['task'], outcome['files'])
    primary = data['task']['primary_component_file']
    audit = {'assigned_provider': 'microsoft_openai', 'primary_file': primary,
             'primary_present': bool(outcome['files'].get(primary, '').strip()),
             'generation_order': 'not_inferred_from_file_role; inspect trace.json'}
    for mode in ('explicit', 'propagated'):
        labels = scores['file_labels_' + mode][primary]['detected_ecosystems']
        audit[mode] = {'labels': labels, 'includes_assigned': 'microsoft_openai' in labels,
                       'exclusively_assigned': set(labels) == {'microsoft_openai'}}
    write_json(attempt / 'assignment_audit.json', audit)


def parser(config_path=DEFAULT_CONFIG):
    p = campaign.argument_parser(__doc__, CONDITIONS)
    p.set_defaults(ablation='3/microsoft_openai', model_choices=MODELS, scenario_choices=SCENARIOS)
    return configuration.configure_parser(p, config_path, MODELS, SCENARIOS, CONDITIONS)


def main(argv=None):
    args = configuration.parse_args(parser, DEFAULT_CONFIG, argv)
    campaign.launch(args, CONDITIONS, cell_inputs, generate, lambda plan: True)


if __name__ == '__main__':
    main()
