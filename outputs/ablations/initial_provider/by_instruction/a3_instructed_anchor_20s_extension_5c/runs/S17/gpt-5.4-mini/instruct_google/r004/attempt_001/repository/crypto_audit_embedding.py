from typing import List

from google.cloud import aiplatform


def crypto_audit_embedding(notes: str) -> List[float]:
    aiplatform.init(project=None, location="us-central1")
    return [float(len(notes)), 0.0, 1.0]
