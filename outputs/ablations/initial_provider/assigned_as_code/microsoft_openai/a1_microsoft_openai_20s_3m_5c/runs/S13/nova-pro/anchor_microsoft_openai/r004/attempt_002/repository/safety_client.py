import os


def get_config():
    return {
        'endpoint': os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT'),
        'api_key': os.getenv('AZURE_CONTENT_SAFETY_API_KEY')
    }


def get_client(config=None):
    config = config or get_config()
    return ContentSafetyClient(config['endpoint'], AzureKeyCredential(config['api_key']))