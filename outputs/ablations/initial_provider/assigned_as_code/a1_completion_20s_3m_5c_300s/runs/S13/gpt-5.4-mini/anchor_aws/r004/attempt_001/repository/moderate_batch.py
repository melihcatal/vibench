from safety_client import create_comprehend_client
from safety_models import normalize_texts


def moderate_batch(payload, config=None):
    client = create_comprehend_client(config)
    texts = normalize_texts(payload)
    items = []
    for text in texts:
        response = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode="en")
        items.append({"text": text, "toxicity": response["ResultList"][0]["Toxicity"]})
    return {"results": items}
