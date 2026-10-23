import openai


def embed_batch(texts):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Embedding.create(input=texts, model="text-embedding-ada-002")
    return [item["embedding"] for item in response["data"]]
