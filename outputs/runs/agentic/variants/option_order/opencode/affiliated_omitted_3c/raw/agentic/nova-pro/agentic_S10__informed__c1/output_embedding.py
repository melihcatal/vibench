from ibm_watsonx_ai import ModelClient


def embed_output(text):
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    client = ModelClient(api_key, project_id)
    embedding = client.embed_text(text)
    return embedding
