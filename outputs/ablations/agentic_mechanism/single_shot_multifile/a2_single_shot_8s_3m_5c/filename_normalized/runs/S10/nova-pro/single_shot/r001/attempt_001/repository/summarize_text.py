from [HELPER] model_client import get_llm_client

def summarize_text(text):
    client = get_llm_client()
    response = client.summarize(text)
    return response.summary