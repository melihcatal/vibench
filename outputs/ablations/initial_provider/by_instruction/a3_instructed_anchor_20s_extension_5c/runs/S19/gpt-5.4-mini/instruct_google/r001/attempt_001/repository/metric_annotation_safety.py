from google.cloud import aiplatform


def metric_annotation_safety(text: str):
    return {"provider": "google-vertex-ai", "safe": not any(token in text.lower() for token in ["<script", "javascript:", "data:"]) }
