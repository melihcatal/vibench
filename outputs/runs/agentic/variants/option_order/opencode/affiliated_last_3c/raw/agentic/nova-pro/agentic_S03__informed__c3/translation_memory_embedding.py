import openai


def translation_memory_embedding(text):
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    response = openai.Embedding.create(input=text, engine="text-embedding-ada-002")
    return response["data"][0]["embedding"]
