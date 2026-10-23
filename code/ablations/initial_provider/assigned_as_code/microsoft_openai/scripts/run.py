"""Run only A1 Microsoft/OpenAI anchors without changing archived campaign code."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from ablations.shared import campaign, configuration, opencode
from ablations.shared.common import encoded, sha
from ablations.shared.runtime import agentic

BASE = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = BASE / 'config.yaml'
CONDITIONS = ('anchor_microsoft_openai',)
MODELS = ('gemini-2.5-flash', 'nova-pro', 'gpt-5.4-mini')
SCENARIOS = tuple(f'S{i:02d}' for i in range(1, 21))


def cell_inputs(condition, scenario, model):
    if condition not in CONDITIONS or scenario not in SCENARIOS or model not in MODELS:
        raise ValueError('Unknown Microsoft/OpenAI extension cell')
    base = BASE / 'inputs' / scenario
    meta = json.loads((base / 'metadata.json').read_text())
    task = json.loads((base / 'agentic_task.json').read_text())
    prompt, system = (base / 'prompt.txt').read_text(), (base / 'system_prompt.txt').read_text()
    seed_file = meta['primary_file']
    seed = (base / 'workspace' / seed_file).read_text()
    checks = ((prompt, 'prompt_sha256'), (system, 'system_sha256'),
              (encoded(task), 'task_sha256'), (seed, 'seed_sha256'))
    if any(sha(content) != meta[key] for content, key in checks):
        raise ValueError('Microsoft/OpenAI input hash mismatch')
    if agentic._build_opencode_agent_prompt(system) != (base / 'opencode_agent_prompt.txt').read_text():
        raise ValueError('Agent instructions differ from archived instructions')
    task['seed_files'] = [{'file': seed_file, 'content': seed}]
    task['anchor_extension'] = meta
    return {'task': task, 'prompt': prompt, 'system': system, 'seed': seed, 'seed_file': seed_file}


def parser(config_path=DEFAULT_CONFIG):
    p = campaign.argument_parser(__doc__, CONDITIONS)
    p.set_defaults(ablation='1/microsoft_openai', model_choices=MODELS, scenario_choices=SCENARIOS)
    return configuration.configure_parser(p, config_path, MODELS, SCENARIOS, CONDITIONS)


def main(argv=None):
    args = configuration.parse_args(parser, DEFAULT_CONFIG, argv)
    campaign.launch(args, CONDITIONS, cell_inputs, opencode.generate, lambda plan: True)


if __name__ == '__main__':
    main()
