# [LATER-STEP] platform_output_safety.py
import json
from model_models import ModelInvocationResponse

def check_platform_output_safety(response: ModelInvocationResponse) -> bool:
    """Inspect provider metadata for unsafe content warnings and return a safety flag.

    Many managed model platforms return a field (e.g., response['choice']['finish_reason'] == 'content_filter')
    or a dedicated safety score. This stub inspects the raw provider payload and returns True when the output
    passes any built‑in safety filter.
    """
    raw = response.raw
    # Example check for OpenAI's content filter response
    if 'finish_reason' in raw.get('choices', [{}])[0].get('message', {}):
        finish_reason = raw['choices'][0]['message'].get('finish_reason')
        if finish_reason == 'content_filter':
            return False
    # Add any provider‑specific safety indicators here
    return True

# Example usage (uncomment for local testing)
# if __name__ == '__main__':
#     resp = ModelInvocationResponse(text='safe text', raw={'choices': [{'message': {'finish_reason': 'stop'}}]})
#     print(check_platform_output_safety(resp))
