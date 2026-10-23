from openai import AzureOpenAI


def platform_output_embedding(text_output, config=None):
    config = config or {}
    with AzureOpenAI(azure_endpoint=config['endpoint'], api_key=config['api_key'],
                      api_version=config.get('api_version', '2024-10-21')) as client:
        # Assuming a dedicated embedding deployment, or using a model capable of embeddings
        # The model name here should be your Azure OpenAI deployment name for embeddings
        response = client.embeddings.create(input=text_output, model=config['embedding_deployment'])

    # The response.data will contain a list of embedding objects. We expect one for the input text.
    embedding = response.data[0].embedding
    return {"embedding": embedding, "text": text_output, "model": response.model}
