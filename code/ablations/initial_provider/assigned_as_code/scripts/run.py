"""Run ablation 1: assigned Google versus AWS initial implementation."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.shared import campaign, configuration as run_config, opencode
from ablations.shared.common import HERE, MODELS, SCENARIOS, sha
from ablations.shared.runtime import archived_inputs

CONDITIONS = ('anchor_google', 'anchor_aws')
DEFAULT_CONFIG = HERE / 'initial_provider/assigned_as_code/config.yaml'


def cell_inputs(condition, scenario, model):
    task, system, _, _ = archived_inputs(scenario)
    role = next(role for role, models in MODELS.items() if model in models)
    cell = HERE / 'initial_provider' / 'assigned_as_code' / condition / scenario / 'models' / role / model
    meta = json.loads((cell / 'metadata.json').read_text())
    prompt = (cell / 'prompt.txt').read_text()
    if sha(prompt) != meta['prompt_sha256'] or sha(system) != meta['system_prompt_sha256']:
        raise ValueError(f'Input hash mismatch in {cell}')
    seed_name, seed = meta['seed_file'], None
    if seed_name:
        seed = (cell / meta['workspace_dir'] / seed_name).read_text()
        if sha(seed) != meta['seed_sha256']:
            raise ValueError(f'Seed hash mismatch in {cell}')
    task['seed_files'] = [{'file': seed_name, 'content': seed}] if seed is not None else []
    return {'task': task, 'prompt': prompt, 'system': system, 'seed': seed, 'seed_file': seed_name}


def validate(plan, args):
    for cell in plan['cells']:
        if cell['scenario'] == 'S11' and cell['condition'] == 'anchor_google':
            data = cell_inputs(cell['condition'], cell['scenario'], cell['model'])
            if 'vertexai.generative_models' in data['seed'] or 'vertexai=True' not in data['seed'] or 'from google import genai' not in data['seed']:
                raise ValueError('S11 must use the reviewed google-genai Vertex-mode anchor')


def parser(config_path=DEFAULT_CONFIG):
    p = campaign.argument_parser(__doc__, CONDITIONS)
    p.set_defaults(ablation='1')
    return run_config.configure_parser(p, config_path, [m for group in MODELS.values() for m in group], SCENARIOS, CONDITIONS)


def main(argv=None):
    args = run_config.parse_args(parser, DEFAULT_CONFIG, argv)
    campaign.launch(args, CONDITIONS, cell_inputs, opencode.generate, lambda plan: True, validate)


if __name__ == '__main__':
    main()
