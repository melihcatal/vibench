"""Reuse replication model routing without changing its defaults."""
import importlib.metadata
import json
import shutil
import sqlite3
import subprocess
import sys

from .common import HERE, ROOT

sys.path.insert(0, str(ROOT / 'code/scripts/generation'))
import run_agentic as agentic

# First-party routes checked 2026-09-18; never relabel successor outputs as old models.
RETIRED_ROUTES = {
    'deepseek-v3.2': 'deepseek-chat was redirected to V4-Flash, then discontinued on 2026-07-24 (https://api-docs.deepseek.com/updates/)',
    'grok-4-1-fast-reasoning': 'retired on 2026-05-15; the slug redirects to grok-4.3 (https://docs.x.ai/developers/migration/may-15-retirement)',
}


def validate_model_routes(plan):
    blocked = sorted({c['model'] for c in plan['cells']} & RETIRED_ROUTES.keys())
    if blocked:
        details = '; '.join(f'{model}: {RETIRED_ROUTES[model]}' for model in blocked)
        raise ValueError('Refusing retired model routes. Review the control roster before execution. ' + details)
    if 'sampling' not in plan:
        return
    from run_direct import _reasoning_effort_request, _reasoning_effort_sent_to_api
    for model_id in sorted({c['model'] for c in plan['cells']}):
        model = agentic.load_models(model_id)[0]
        if any(c['model'] == model_id and c['condition'] != 'single_shot' for c in plan['cells']):
            record = agentic.build_agentic_sampling_record(model, plan['sampling'])
            if record['opencode_variant_requested'] != record['opencode_variant_sent_to_opencode']:
                raise ValueError(f'{model_id}: requested OpenCode reasoning setting would be dropped')
        if any(c['model'] == model_id and c['condition'] == 'single_shot' for c in plan['cells']):
            requested = _reasoning_effort_request(model, plan['sampling'])[0]
            if requested != _reasoning_effort_sent_to_api(model, plan['sampling'])[0]:
                raise ValueError(f'{model_id}: requested direct reasoning setting would be dropped')


def archived_inputs(scenario):
    source = HERE / 'paper_inputs' / scenario
    task = json.loads((source / 'agentic_task.json').read_text())
    system = (source / 'system_prompt.txt').read_text()
    agent_prompt = (source / 'opencode_agent_prompt.txt').read_text()
    if agentic._build_opencode_agent_prompt(system) != agent_prompt:
        raise ValueError('Current agent instructions differ from archived instructions')
    return task, system, agent_prompt, (source / 'original_prompt.txt').read_text()


def runtime_record(needs_opencode=True):
    packages = {}
    for package in ('litellm', 'openai', 'anthropic', 'boto3'):
        try:
            packages[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            packages[package] = None
    version = None
    if needs_opencode:
        oc = subprocess.run(['opencode', '--version'], capture_output=True, text=True, timeout=30)
        if oc.returncode:
            raise ValueError('Cannot determine OpenCode version')
        version = oc.stdout.strip()
    return {'python': sys.version, 'packages': packages, 'opencode': version}


def preflight(plan, args, needs_opencode):
    validate_model_routes(plan)
    if needs_opencode and shutil.which('opencode') is None:
        raise ValueError('OpenCode is not installed')
    if needs_opencode:
        with sqlite3.connect(args.trace_db.resolve().as_uri() + '?mode=ro', uri=True) as db:
            for table in ('session', 'message', 'part'):
                db.execute(f'SELECT id FROM {table} LIMIT 0')
    env_path = ROOT / 'code/configs/.env'
    agentic.load_dotenv(env_path, override=True)
    models = [agentic.load_models(m)[0] for m in sorted({c['model'] for c in plan['cells']})]
    agentic.validate_model_env(models, env_path)
    return runtime_record(needs_opencode)
