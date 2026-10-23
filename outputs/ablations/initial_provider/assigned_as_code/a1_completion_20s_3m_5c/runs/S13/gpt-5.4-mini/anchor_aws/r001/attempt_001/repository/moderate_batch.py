from safety_client import get_comprehend_client
from safety_models import normalize_texts


def moderate_batch(payload, config=None):
    config = config or {}
    client = get_comprehend_client(config)
    texts = normalize_texts(payload)
    response = client.detect_toxic_content(
        TextSegments=[{"Text": text} for text in texts],
        LanguageCode=config.get("language", "en"),
    )
    results = []
    for item in response.get("ResultList", []):
        results.append(
            {
                "text_index": item.get("Index"),
                "toxicity": item.get("Toxicity"),
                "allow": item.get("Toxicity", 0) < config.get("threshold", 0.5),
            }
        )
    return {"results": results}
