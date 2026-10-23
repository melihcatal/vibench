"""Independent OpenCode sessions per file; repository state persists within a run."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

from ablations.shared.common import encoded, redact, timestamp, write_json
from ablations.shared.runtime import agentic
from ablations.shared.scoring import score_files
from ablations.shared.traces import export_trace
from ablations.agentic_mechanism.task_disclosure.scripts.audit import event_order, snapshot, step_audit
from ablations.agentic_mechanism.task_disclosure.scripts.build_inputs import single_file_agent_prompt


def fresh_session(trace, previous_roots, prompt):
    roots = {s['id'] for s in trace['sessions'] if not s.get('parent_id')}
    new = roots - previous_roots
    if len(new) != 1 or not previous_roots.issubset(roots):
        raise RuntimeError('Expected exactly one fresh root OpenCode session per file')
    session = next(iter(new))
    users = [m for m in trace['messages'] if m['session_id'] == session and m['data'].get('role') == 'user']
    if len(users) != 1:
        raise RuntimeError('Fresh session must contain exactly one user request; possible history carryover')
    texts = [p['data'].get('text', '') for p in trace['parts']
             if p['message_id'] == users[0]['id'] and p['data'].get('type') == 'text']
    if texts not in ([prompt], ['"' + prompt + '"']):
        raise RuntimeError('Recorded user prompt differs from the current file request')
    return session, roots


def response_errors(stdout, trace, old_messages):
    errors = []
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if isinstance(event, dict) and event.get('type') == 'error':
            errors.append(event)
    for row in trace['messages']:
        if row['id'] not in old_messages and row['data'].get('error'):
            errors.append(row['data']['error'])
    return errors


class Conversation:
    def __init__(self, workspace, model, system, sampling):
        self.workspace, self.server = workspace, None
        self.route, self.identity_mode, self.identity_note = agentic.resolve_opencode_model(model['id'])
        agentic.prepare_opencode_workspace(workspace, model, self.route, system, sampling=sampling)
        (workspace / 'vibench_agent_prompt.md').write_text(single_file_agent_prompt(system))
        config_path = workspace / 'opencode.json'
        config = json.loads(config_path.read_text())
        config['agent']['vibench']['description'] = 'Python integration coding agent'
        config_path.write_text(encoded(config))
        self.sampling = agentic.build_agentic_sampling_record(model, sampling)
        self.env = os.environ.copy()
        for source, target in agentic.OPENCODE_ENV_MAP.items():
            if source in self.env and target not in self.env:
                self.env[target] = self.env[source]

    def __enter__(self):
        port = agentic._free_port()
        self.url = f'http://127.0.0.1:{port}'
        self.server = subprocess.Popen(['opencode', 'serve', '--port', str(port)],
            cwd=str(self.workspace), env=self.env, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL, start_new_session=True)
        try:
            if not agentic._wait_for_port(port):
                raise RuntimeError('OpenCode server did not become ready')
        except BaseException:
            self.close()
            raise
        return self

    def send(self, prompt, timeout):
        cmd = ['opencode', 'run', '--attach', self.url, '--format', 'json',
               '-m', self.route, '--agent', 'vibench']
        # No --session/--continue: each file receives a new conversation.
        if self.sampling.get('opencode_variant'):
            cmd.extend(['--variant', self.sampling['opencode_variant']])
        started = time.monotonic()
        result = subprocess.run(cmd + [prompt], cwd=str(self.workspace), env=self.env,
                                capture_output=True, text=True, timeout=timeout)
        return {'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr,
                'command': cmd + ['<prompt_text>'], 'elapsed_seconds': time.monotonic() - started,
                'error': agentic._classify_opencode_provider_error(result.stderr)}

    def close(self):
        if self.server is not None:
            self.server.terminate()
            try:
                self.server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server.kill()
                self.server.wait(timeout=5)

    def __exit__(self, *_):
        self.close()


def save_repository(directory, contents):
    directory.mkdir(parents=True, exist_ok=True)
    for name, content in contents.items():
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(redact(content))


def generate(data, model, plan, attempt, database, outcome, step_limit=None):
    if step_limit is not None and not 1 <= step_limit <= len(data['prompts']):
        raise ValueError('Invalid pilot step limit')
    workspace = Path(tempfile.mkdtemp(prefix='vb-staged-')).resolve()
    names, task = data['task']['expected_files'], data['task']
    trace = {'sessions': [], 'messages': [], 'parts': []}
    roots, part_steps, records = set(), {}, []
    started = time.monotonic()
    deadline = started + plan['timeout']
    outcome['response'] = {'condition': task['disclosure_condition'], 'steps': records,
                           'conversation_mode': 'fresh_session_per_file', 'pilot_step_limit': step_limit,
                           'timeout_scope': 'whole_repository_run'}
    try:
        with Conversation(workspace, model, data['system'], plan['sampling']) as conversation:
            outcome['response'].update({'opencode_model': conversation.route,
                'identity_mode': conversation.identity_mode, 'identity_note': conversation.identity_note,
                'sampling': conversation.sampling})
            for index, (name, prompt) in enumerate(zip(names, data['prompts']), 1):
                if step_limit is not None and index > step_limit:
                    break
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError('Whole-repository time budget exhausted')
                step_dir = attempt / 'steps' / f'{index:02d}'
                step_dir.mkdir(parents=True)
                (step_dir / 'prompt.txt').write_text(prompt)
                before, _ = snapshot(workspace)
                previous_messages = {m['id'] for m in trace['messages']}
                response, failure = {}, None
                record = {'step': index, 'requested_file': name, 'started': timestamp()}
                try:
                    response = conversation.send(prompt, remaining)
                except Exception as exc:
                    failure = f'{type(exc).__name__}: {exc}'
                    response = {'error': failure, 'exit_code': -1}
                    if isinstance(exc, subprocess.TimeoutExpired):
                        for key in ('stdout', 'stderr'):
                            value = getattr(exc, key, None) or ''
                            response[key] = value.decode(errors='replace') if isinstance(value, bytes) else value
                finally:
                    # Partial outputs survive API failures, timeouts, and interruption.
                    after, unsafe = snapshot(workspace)
                    outcome['files'] = {n: after[n] for n in names if n in after}
                    save_repository(step_dir / 'repository', after)
                    audit = step_audit(before, after, name, names[index:], unsafe, names)
                    write_json(step_dir / 'audit.json', audit)
                    write_json(step_dir / 'metrics.json', score_files(task, outcome['files']))
                    write_json(step_dir / 'response.json', redact(response))
                    record.update({'finished': timestamp(), 'audit': audit, 'response': response})
                    records.append(record)
                    write_json(attempt / 'step_summary.json', redact(records))
                trace = export_trace(database, workspace)
                session, roots = fresh_session(trace, roots, prompt)
                record['session_id'] = session
                record['prompt_verified'] = True
                record['user_message_count'] = 1
                for part in trace['parts']:
                    part_steps.setdefault(part['id'], index)
                write_json(step_dir / 'trace.json', redact(trace))
                errors = response_errors(response.get('stdout', ''), trace, previous_messages)
                if failure or response.get('exit_code') != 0 or response.get('error') or errors:
                    raise RuntimeError(f'Step {index} failed: {failure or response.get("error") or errors or response.get("stderr")}')
                if not any(m['id'] not in previous_messages and m['data'].get('role') == 'assistant'
                           for m in trace['messages']):
                    raise RuntimeError(f'No assistant response recorded for step {index}')
                # Continue despite file-protocol noncompliance; retain all assigned runs.
        outcome['response']['exit_code'] = 0
    except Exception as exc:
        outcome['response']['error'] = f'{type(exc).__name__}: {exc}'
    finally:
        try:
            after, _ = snapshot(workspace)
            outcome['files'] = {n: after[n] for n in names if n in after}
            save_repository(attempt / 'final_snapshot', after)
            try:
                trace = export_trace(database, workspace)
                if not trace['sessions']:
                    outcome['errors'].append('No matching OpenCode session trace')
            except Exception as exc:
                outcome['errors'].append(f'Trace export failed: {exc}')
            write_json(attempt / 'trace.json', redact(trace))
            timeline = event_order(trace, workspace, part_steps, names)
            targets = {r['step']: r['requested_file'] for r in records}
            off_target = [e for e in timeline['events'] if e['file'] != targets.get(e['step'])]
            first = {}
            for event in timeline['events']:
                first.setdefault(event['file'], event)
            relations = {}
            anchor = first.get(task['primary_component_file'])
            for name in task['downstream_files']:
                later = first.get(name)
                if timeline['uncertain_activity'] or anchor is None or later is None:
                    relation = 'unknown'
                elif anchor['message'] == later['message']:
                    relation = 'same_turn'
                elif anchor['end'] < later['turn_start']:
                    relation = 'sequential'
                elif later['end'] < anchor['turn_start']:
                    relation = 'reverse'
                else:
                    relation = 'overlapping'
                relations[name] = relation
            audit = {'condition': task['disclosure_condition'],
                     'conversation_mode': 'fresh_session_per_file', 'root_session_ids': sorted(roots),
                     'pilot_step_limit': step_limit,
                     'steps_attempted': len(records), 'expected_steps': len(names),
                     'file_order': names, 'off_target_mutations': off_target,
                     'snapshot_noncompliance_steps': [r['step'] for r in records if
                         r['audit']['off_target_changes'] or r['audit']['future_files_present'] or
                         r['audit']['symlinks'] or not r['audit']['requested_file_present']],
                     'generation_order': timeline,
                     'primary_first_mutation_vs_downstream': relations,
                     'filtering': 'Noncompliant runs retained; report adherence separately.'}
            outcome['audit'] = audit
            outcome['response']['elapsed_seconds'] = time.monotonic() - started
            write_json(attempt / 'disclosure_audit.json', redact(audit))
            write_json(attempt / 'step_summary.json', redact(records))
            for name in ('opencode.json', 'vibench_agent_prompt.md'):
                path = workspace / name
                if path.exists() and not path.is_symlink():
                    content = path.read_text()
                    (attempt / name).write_text(encoded(redact(json.loads(content))) if name.endswith('.json') else redact(content))
        finally:
            shutil.rmtree(workspace)
