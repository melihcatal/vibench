"""Run ablation 2: matched ten-file agentic versus single-shot generation."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.shared import campaign, configuration as run_config, opencode
from ablations.shared.common import HERE, MODELS, SCENARIOS
from ablations.shared.runtime import archived_inputs
from ablations.agentic_mechanism.single_shot_multifile.scripts import single_shot

CONDITIONS = ('agentic', 'single_shot')
DEFAULT_CONFIG = HERE / 'agentic_mechanism/single_shot_multifile/config.yaml'
SINGLE_SHOT_USER_REPLACEMENTS = {
    'Create exactly these Python files in the current working directory:':
        'Generate code for exactly these Python files:',
    '- Write exactly the listed files in the current working directory. Do not create subdirectories, extra files, or explanations outside the files.':
        '- Return exactly the listed files in one JSON object mapping filenames to complete Python source strings. Do not include additional keys or explanations outside the JSON.',
}
SINGLE_SHOT_SYSTEM_REPLACEMENTS = {
    '- Create exactly the requested files and no extra files.':
        '- Generate code for exactly the requested files and no extra files.',
    '- Do not include explanations outside code.':
        '- Do not include explanations outside the requested JSON object.',
    '- Write only the requested Python files. Do not put explanations, markdown fences, comments, docstrings, or example usage in those files.':
        '- Return only the requested Python files as source strings. Do not put explanations, markdown fences, comments, docstrings, or example usage in those strings.',
    '- Write files only in the current working directory, using exactly the relative filenames requested by the user task.':
        '- Return one JSON object mapping exactly the requested relative filenames to complete Python source strings. Do not call tools or write files on disk.',
    '- Do not use absolute paths or create subdirectories.':
        '- Do not use absolute paths or subdirectories in filename keys.',
}


def replace_delivery(text, replacements):
    for old, new in replacements.items():
        if text.count(old) != 1:
            raise ValueError(f'Expected exactly one delivery instruction: {old}')
        text = text.replace(old, new, 1)
    return text


def cell_inputs(condition, scenario, model):
    task, system, agent_prompt, prompt = archived_inputs(scenario)
    if condition == 'single_shot':
        prompt = replace_delivery(prompt, SINGLE_SHOT_USER_REPLACEMENTS)
        system = replace_delivery(agent_prompt, SINGLE_SHOT_SYSTEM_REPLACEMENTS)
    task['seed_files'] = []
    return {'task': task, 'prompt': prompt, 'system': system, 'seed': None, 'seed_file': None, 'condition': condition}


def generate(data, model, plan, attempt, database, outcome):
    if data['condition'] == 'single_shot':
        single_shot.generate(data, model, plan, attempt, database, outcome)
    else:
        opencode.generate(data, model, plan, attempt, database, outcome)


def parser(config_path=DEFAULT_CONFIG):
    p = campaign.argument_parser(__doc__, CONDITIONS)
    p.set_defaults(ablation='2', conditions='single_shot')
    return run_config.configure_parser(p, config_path, [m for group in MODELS.values() for m in group], SCENARIOS, CONDITIONS)


def main(argv=None):
    args = run_config.parse_args(parser, DEFAULT_CONFIG, argv)
    campaign.launch(args, CONDITIONS, cell_inputs, generate,
                    lambda plan: any(c['condition'] == 'agentic' for c in plan['cells']))


if __name__ == '__main__':
    main()
