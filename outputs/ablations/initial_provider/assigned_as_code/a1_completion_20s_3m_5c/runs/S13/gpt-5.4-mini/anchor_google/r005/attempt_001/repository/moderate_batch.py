from moderate_text import moderate_text
from safety_models import normalize_messages


def moderate_batch(payload, config=None):
    messages = normalize_messages(payload.get("messages"))
    results = []
    for index, text in enumerate(messages):
        result = moderate_text({"text": text}, config=config)
        results.append({"index": index, "text": text, "decision": result})
    return {"results": results}
