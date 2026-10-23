from [HELPER] model_client import get_llm_client

def extract_json(text):
    client = get_llm_client()
    response = client.extract_json(text)
    return response.json_data