from google.cloud import aiplatform

def collect_metadata(response):
    metadata = {
        "usage": response.metadata.get("usage"),
        "resource_ids": response.metadata.get("resource_ids"),
        "model_handles": response.metadata.get("model_handles")
    }
    return metadata
