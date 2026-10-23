import openai


def embed_platform_output(text):
    client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding
