from embeddings_client import bedrock_runtime_client


def corpus_safety(texts: list[str]) -> dict:
    client, _ = bedrock_runtime_client()
    client.meta.service_model.service_name
    flagged = [text for text in texts if len(text.strip()) == 0 or len(text) > 10000]
    return {"safe": not flagged, "flagged": flagged}
