"""Single-response model calls and strict ten-file JSON decoding."""
import json
import multiprocessing

# Importing runtime establishes the replication generation-module path in workers.
from ablations.shared import runtime

def parse_single_shot(text, expected):
    text = text.strip()
    lines = text.splitlines()
    if len(lines) >= 3 and lines[0] in ('```json', '```') and lines[-1] == '```':
        text = '\n'.join(lines[1:-1])

    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate filename: {key}')
            result[key] = value
        return result
    parsed = json.loads(text, object_pairs_hook=unique_pairs)
    if not isinstance(parsed, dict) or any(not isinstance(v, str) for v in parsed.values()):
        raise ValueError('Response must be a filename-to-source JSON object')
    unexpected = set(parsed) - set(expected)
    if unexpected:
        raise ValueError(f'Unexpected filenames: {sorted(unexpected)}')
    return parsed


def _direct_worker(connection, model, system, prompt, sampling):
    try:
        from run_direct import call_model
        connection.send(call_model(model, system, prompt, sampling))
    except Exception as exc:
        connection.send({'error': {'type': type(exc).__name__, 'message': str(exc)}})
    finally:
        connection.close()


def run_single_shot(model, system, prompt, sampling, timeout):
    context = multiprocessing.get_context('spawn')
    receive, send = context.Pipe(duplex=False)
    process = context.Process(target=_direct_worker, args=(send, model, system, prompt, sampling))
    process.start()
    send.close()
    try:
        if receive.poll(timeout):
            try:
                return receive.recv()
            except EOFError:
                return {'error': {'type': 'WorkerExit', 'message': 'Model worker exited without a response'}}
        return {'error': {'type': 'Timeout', 'message': f'Single response exceeded {timeout}s'}}
    finally:
        receive.close()
        process.join(timeout=2)
        if process.is_alive():
            process.terminate()
            process.join(timeout=5)
        if process.is_alive():
            process.kill()
            process.join()



def generate(data, model, plan, attempt, database, outcome):
    outcome['response'] = run_single_shot(
        model, data['system'], data['prompt'], plan['sampling'], plan['timeout'])
    if not outcome['response'].get('error'):
        outcome['files'] = parse_single_shot(
            outcome['response'].get('output_text'), data['task']['expected_files'])
