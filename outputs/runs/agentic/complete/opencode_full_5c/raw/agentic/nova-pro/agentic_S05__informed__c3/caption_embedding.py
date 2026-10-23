import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_caption(caption):
    response = openai.Embedding.create(input=caption, model="text-embedding-ada-002")
    return response["data"][0]["embedding"]
