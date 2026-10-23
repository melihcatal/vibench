import os

def get_azure_document_intelligence_config():
    return {
        'endpoint': os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT'),
        'api_key': os.environ.get('AZURE_DOCUMENT_INTELLIGENCE_API_KEY')
    }

def get_openai_config():
    return {
        'api_key': os.environ.get('OPENAI_API_KEY')
    }

def get_google_cloud_language_config():
    # Google Cloud client libraries typically pick up credentials automatically
    # from GOOGLE_APPLICATION_CREDENTIALS environment variable or default service account.
    # No explicit config needed here, but keeping the function for consistency.
    return {}

def get_google_cloud_translate_config():
    # Similar to Natural Language API, credentials are handled automatically.
    return {}

def get_aws_dynamodb_config():
    return {
        'region_name': os.environ.get('AWS_REGION_NAME'),
        'aws_access_key_id': os.environ.get('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': os.environ.get('AWS_SECRET_ACCESS_KEY')
    }

def get_google_cloud_function_normalization_config():
    return {
        'endpoint': os.environ.get('GOOGLE_CLOUD_FUNCTION_NORMALIZATION_ENDPOINT')
    }
