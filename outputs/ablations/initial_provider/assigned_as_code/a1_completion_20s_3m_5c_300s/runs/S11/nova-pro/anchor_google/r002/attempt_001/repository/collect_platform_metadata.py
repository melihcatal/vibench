from google import genai

def collect_platform_metadata(response):
    metadata = {
        "usage": response.usage,
        "resource_id": response.resource_id,
        "model_handle": response.model_handle
    }
    return metadata