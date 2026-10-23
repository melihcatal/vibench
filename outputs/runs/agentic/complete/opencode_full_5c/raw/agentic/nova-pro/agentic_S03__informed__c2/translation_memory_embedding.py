import openai


def embed_translation_memory(text):
    client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding


if __name__ == "__main__":
    print(embed_translation_memory("This is a sample translation memory segment."))
