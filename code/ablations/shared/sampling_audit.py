"""Record requested reasoning settings and observed usage, without exporting reasoning text."""
import json

from .runtime import agentic


def audit_sampling(model, sampling, response, trace_path):
    from run_direct import _reasoning_effort_sent_to_api
    opencode = agentic.build_agentic_sampling_record(model, sampling)
    direct = _reasoning_effort_sent_to_api(model, sampling)[0]
    is_agentic = trace_path.exists()
    errors = []
    reasoning = None
    messages = 0
    if is_agentic:
        trace = json.loads(trace_path.read_text())
        seen = set()
        values = []
        for message in trace.get('messages', []):
            if message['id'] in seen or message['data'].get('role') != 'assistant':
                continue
            seen.add(message['id'])
            tokens = message['data'].get('tokens') or {}
            if tokens.get('reasoning') is not None:
                values.append(tokens['reasoning'])
        messages = len(values)
        reasoning = sum(values) if values else None
    else:
        reasoning = response.get('reasoning_tokens')
    expected = opencode['opencode_variant_sent_to_opencode'] if is_agentic else direct
    if expected == 'none' and reasoning is not None and reasoning > 0:
        errors.append('Reasoning tokens were reported despite the requested none setting; investigate before pooling results.')
    return {'model_id': model['id'], 'sampling_requested': sampling,
            'opencode_variant_resolved': opencode['opencode_variant_sent_to_opencode'],
            'direct_reasoning_effort_resolved': direct,
            'usage_source': 'OpenCode trace' if is_agentic else 'direct response',
            'assistant_messages_with_reasoning_usage': messages,
            'reasoning_tokens_reported': reasoning, 'warnings': errors,
            'note': 'Resolved settings describe client requests, not independent proof of provider enforcement. Missing usage is not zero.'}
