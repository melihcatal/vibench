"""Run ablation 4: full versus staged disclosure, one file per interaction."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.shared import campaign, configuration as run_config
from ablations.shared.common import encoded, sha
from ablations.shared.runtime import agentic
from ablations.agentic_mechanism.task_disclosure.scripts.build_inputs import BASE, configuration, make_prompts, single_file_system, single_file_agent_prompt
from ablations.agentic_mechanism.task_disclosure.scripts.staged import generate

DEFAULT_CONFIG = BASE / 'config.yaml'


def cell_inputs(condition, scenario, model):
    cfg = configuration()
    if condition not in cfg['conditions'] or scenario not in cfg['scenarios'] or model not in cfg['models']:
        raise ValueError('Unknown ablation 4 condition, scenario, or model')
    source, cell = BASE / 'sources' / scenario, BASE / condition / scenario
    meta = json.loads((cell / 'metadata.json').read_text())
    for name, digest in meta['source_sha256'].items():
        if sha((source / name).read_text()) != digest:
            raise ValueError('Ablation 4 source hash mismatch')
    task = json.loads((source / 'agentic_task.json').read_text())
    system = (source / 'system_prompt.txt').read_text()
    prompts = [(cell / f'prompt_{i:02d}.txt').read_text() for i in range(1, 11)]
    expected = make_prompts(task, (source / 'original_prompt.txt').read_text(), condition)
    if prompts != expected or [sha(p) for p in prompts] != meta['prompt_sha256'] or sha(encoded(prompts)) != meta['prompt_bundle_sha256']:
        raise ValueError('Ablation 4 prompt hash or specification mismatch')
    if meta['file_order'] != task['expected_files'] or meta['condition'] != condition:
        raise ValueError('Ablation 4 condition/order mismatch')
    if single_file_system((source / 'original_system_prompt.txt').read_text()) != system:
        raise ValueError('System instructions differ from the declared single-file adaptation')
    if single_file_agent_prompt(system) != (source / 'opencode_agent_prompt.txt').read_text():
        raise ValueError('Agent instructions differ from the declared single-file adaptation')
    task['seed_files'] = []
    task['disclosure_condition'] = condition
    task['disclosure_protocol'] = cfg
    # The shared planner hashes the entire prompt bundle, not just the first turn.
    return {'task': task, 'prompt': encoded(prompts), 'prompts': prompts, 'system': system,
            'seed': None, 'seed_file': None}


def parser(config_path=DEFAULT_CONFIG):
    cfg = configuration()
    p = campaign.argument_parser(__doc__, tuple(cfg['conditions']))
    p.set_defaults(ablation='4', model_choices=cfg['models'], scenario_choices=cfg['scenarios'])
    return run_config.configure_parser(p, config_path, cfg['models'], cfg['scenarios'], cfg['conditions'])


def parse_args(argv=None):
    return run_config.parse_args(parser, DEFAULT_CONFIG, argv)


def main(argv=None):
    args = parse_args(argv)
    campaign.launch(args, tuple(configuration()['conditions']), cell_inputs, generate, lambda plan: True)


if __name__ == '__main__':
    main()
