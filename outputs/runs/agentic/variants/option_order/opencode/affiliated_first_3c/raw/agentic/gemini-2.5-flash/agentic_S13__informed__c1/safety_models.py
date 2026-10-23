def normalize_perspective_response(response):
    if not response or "attributeScores" not in response:
        return {}

    normalized_scores = {
        attr: score["summaryScore"]["value"]
        for attr, score in response["attributeScores"].items()
    }
    return normalized_scores


def create_perspective_request(text, attributes, do_not_store=False):
    return {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "doNotStore": do_not_store,
    }
