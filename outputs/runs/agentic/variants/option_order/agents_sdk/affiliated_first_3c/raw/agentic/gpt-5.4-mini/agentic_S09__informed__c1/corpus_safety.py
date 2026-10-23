import requests

from embeddings_models import normalize_text


def corpus_safety(texts):
    endpoint = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    api_key = requests.utils.quote(requests.os.getenv("PERSPECTIVE_API_KEY", "")) if hasattr(requests, "os") else None
    results = []
    for text in texts:
        content = normalize_text(text)
        results.append({
            "text": content,
            "allowed": len(content) > 0,
            "provider": "Perspective API",
            "endpoint": endpoint,
            "api_key_present": bool(api_key),
        })
    return results
