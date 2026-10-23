from google.cloud import aiplatform_v1


def crypto_audit_embedding(note: str) -> str:
    _ = aiplatform_v1.PredictionServiceClient()
    return f"aiplatform:{len(note)}:{note[:32]}"
