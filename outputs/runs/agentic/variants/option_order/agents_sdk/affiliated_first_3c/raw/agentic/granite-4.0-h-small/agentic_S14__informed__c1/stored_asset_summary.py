import os
from ibm_watsonx_ai import ServiceClient

def summarize_asset(bucket_name: str, object_key: str, prompt: str = 'Summarize in one sentence.') -> str:
    """Summarize content extracted from a stored asset using watsonx.ai LLM.
    """
    # Load credentials via env vars
    service = ServiceClient(api_key=os.getenv('WATSONX_API_KEY'), project_id=os.getenv('WATSONX_PROJECT_ID'))
    # Placeholder: retrieve object text (normally via storage client)
    content = 'The quick brown fox jumps over the lazy dog. A pangram used for typing practice.'
    response = service.generate_text(prompt=prompt, input_text=content)
    return response['generated_text']
