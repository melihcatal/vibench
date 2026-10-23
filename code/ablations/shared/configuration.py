"""Thin YAML/CLI adapter; sampling defaults come from the original paper configs."""
import argparse
from pathlib import Path

from .common import ROOT, selections
from .runtime import agentic

PAPER_AGENTIC_CONFIG = ROOT / 'code/configs/vibench/agentic/complete/opencode_full_5c.yaml'
PAPER_DIRECT_CONFIG = ROOT / 'code/configs/vibench/direct/complete/full_5c.yaml'
MAX_TIMEOUT_SECONDS = 300


def timeout_seconds(value):
    try:
        seconds = int(value)
    except (TypeError, ValueError) as exc:
        raise argparse.ArgumentTypeError('timeout must be an integer number of seconds') from exc
    if not 1 <= seconds <= MAX_TIMEOUT_SECONDS:
        raise argparse.ArgumentTypeError(f'timeout must be between 1 and {MAX_TIMEOUT_SECONDS} seconds')
    return seconds


def paper_sampling():
    from run_direct import load_config
    direct = load_config(PAPER_DIRECT_CONFIG)['sampling']
    agent = agentic.load_config(PAPER_AGENTIC_CONFIG)['sampling']
    for key in direct.keys() & agent.keys():
        if direct[key] != agent[key]:
            raise ValueError(f'Original direct/agentic sampling policies disagree on {key}')
    return {**direct, **agent}


def run_settings(path, models, scenarios, conditions):
    path = Path(path).resolve()
    if not path.is_file():
        raise ValueError(f'Run config not found: {path}')
    settings = agentic.load_config(path)
    if settings.get('type') != 'agentic' or settings.get('benchmark') != 'vibench':
        raise ValueError('Ablation campaigns require an agentic VIBench task config')
    if settings.get('variants') != ['free']:
        raise ValueError('These ablations currently support archived NLI/free prompts only')
    defaults = {}
    for key, dest, available in [('models', 'models', models), ('tasks', 'scenarios', scenarios),
                                 ('conditions', 'conditions', conditions)]:
        values = settings.get(key, 'all')
        if values != 'all' and (not isinstance(values, list) or not all(isinstance(x, str) for x in values)):
            raise ValueError(f'{key} must be a list of IDs or all')
        defaults[dest] = ','.join(selections('all' if values == 'all' else ','.join(values), available))
    for key, dest in [('completions', 'repetitions'), ('timeout', 'timeout'),
                      ('max_workers', 'workers'), ('max_consecutive_errors', 'max_consecutive_errors')]:
        value = settings.get(key, 3 if key == 'max_consecutive_errors' else None)
        if value is None and key == 'max_workers':
            continue
        if type(value) is not int or value < 1:
            raise ValueError(f'{key} must be a positive integer')
        if key == 'timeout' and value > MAX_TIMEOUT_SECONDS:
            raise ValueError(f'timeout must not exceed {MAX_TIMEOUT_SECONDS} seconds')
        defaults[dest] = value
    overrides = settings.get('sampling') or {}
    if not isinstance(overrides, dict):
        raise ValueError('sampling must be a mapping')
    sampling = paper_sampling()
    if set(overrides) - sampling.keys():
        raise ValueError(f'Unknown sampling settings: {sorted(set(overrides) - sampling.keys())}')
    for key, value in overrides.items():
        if isinstance(sampling.get(key), dict):
            if not isinstance(value, dict):
                raise ValueError(f'{key} must be a mapping')
            sampling[key] = {**sampling[key], **value}
        else:
            sampling[key] = value
    defaults.update(sampling=sampling, run_config=path)
    return defaults


def configure_parser(parser, path, models, scenarios, conditions):
    parser.add_argument('--config', type=Path, default=path, help='YAML run configuration; CLI scope flags override it')
    parser.set_defaults(**run_settings(path, models, scenarios, conditions))
    return parser


def parse_args(parser_factory, default_config, argv=None):
    bootstrap = argparse.ArgumentParser(add_help=False)
    bootstrap.add_argument('--config', type=Path, default=default_config)
    config_args, _ = bootstrap.parse_known_args(argv)
    return parser_factory(config_args.config).parse_args(argv)
