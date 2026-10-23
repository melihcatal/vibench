"""Execute the unchanged OpenCode adapter and retain per-run traces."""
import json
from pathlib import Path
import shutil
import tempfile

from .common import encoded, redact, write_json
from .runtime import agentic
from .traces import audit_anchor, export_trace


def generate(data, model, plan, attempt, database, outcome):
    workspace = Path(tempfile.mkdtemp(prefix='vb-run-')).resolve()
    trace = {}
    try:
        try:
            outcome['response'] = agentic.run_opencode(
                data['task'], data['prompt'], workspace, model,
                timeout=plan['timeout'], system_prompt=data['system'], sampling=plan['sampling'])
        finally:
            outcome['files'] = {k: v for k, v in agentic.collect_files(
                workspace, data['task']['expected_files']).items() if v is not None}
            try:
                trace = export_trace(database, workspace)
                if not trace['sessions']:
                    outcome['errors'].append('No matching OpenCode session trace')
            except Exception as exc:
                outcome['errors'].append(f'Trace export failed: {type(exc).__name__}: {exc}')
            write_json(attempt / 'trace.json', redact(trace))
            outcome['audit'] = audit_anchor(trace, workspace, data['seed_file'],
                                           data['seed'], outcome['files'].get(data['seed_file']))
            write_json(attempt / 'anchor_audit.json', outcome['audit'])
    finally:
        try:
            for name in ('opencode.json', 'vibench_agent_prompt.md'):
                path = workspace / name
                if path.exists():
                    content = path.read_text()
                    saved = redact(json.loads(content)) if name.endswith('.json') else redact(content)
                    (attempt / name).write_text(encoded(saved) if isinstance(saved, dict) else saved)
        finally:
            shutil.rmtree(workspace)
