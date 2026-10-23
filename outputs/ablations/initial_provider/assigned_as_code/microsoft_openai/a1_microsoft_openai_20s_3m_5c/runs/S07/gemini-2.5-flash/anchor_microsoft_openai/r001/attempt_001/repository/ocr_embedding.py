from openai import AzureOpenAI

def ocr_embedding(text: str, config=None):
    config = config or {}
    # Endpoint for Azure OpenAI should be like "https://<your-resource-name>.openai.azure.com/"
    client = AzureOpenAI(
        azure_endpoint=config['azure_openai_endpoint'],
        api_key=config['azure_openai_api_key'],
        api_version=config.get('azure_openai_api_version', '2023-05-15') # Or other supported API version
    )
    
    # Model deployment name for embeddings, e.g., "text-embedding-ada-002"
    response = client.embeddings.create(input=text, model=config['azure_openai_embedding_deployment_name'])
    return {'embedding': response.data[0].embedding}
