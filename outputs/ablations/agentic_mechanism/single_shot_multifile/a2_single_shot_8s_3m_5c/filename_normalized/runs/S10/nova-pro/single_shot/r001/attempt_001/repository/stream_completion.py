from [HELPER] model_client import get_llm_client

def stream_completion(prompt):
    client = get_llm_client()
    for token in client.stream_completion(prompt):
        yield token