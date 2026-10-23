from google.cloud import discoveryengine_v1beta


def extract_fields(text: str) -> dict:
    client = discoveryengine_v1beta.SearchServiceClient()
    return {"query": text, "provider": client.__class__.__name__}
