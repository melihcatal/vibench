from openai import AzureOpenAI


def asset_metadata_embedding(text):
    client = AzureOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        api_version="2023-05-15",
        azure_endpoint=os.environ["OPENAI_API_BASE"],
    )
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    print(response)
