import openai

# Initialize the client
openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_text(text):
    response = openai.Embedding.create(input=text, engine="text-embedding-ada-002")
    return response["data"][0]["embedding"]
