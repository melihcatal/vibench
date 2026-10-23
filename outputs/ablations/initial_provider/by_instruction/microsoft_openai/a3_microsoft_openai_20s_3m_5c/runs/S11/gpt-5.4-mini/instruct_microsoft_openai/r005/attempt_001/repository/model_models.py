def normalize_text_output(response) -> str:
    text = getattr(response, "output_text", None)
    if text:
        return text
    output = getattr(response, "output", None) or []
    chunks = []
    for item in output:
        content = getattr(item, "content", None) or []
        for part in content:
            value = getattr(part, "text", None)
            if value:
                chunks.append(value)
    return "".join(chunks)


def collect_response_metadata(response) -> dict:
    return {
        "text": normalize_text_output(response),
        "usage": getattr(response, "usage", None),
        "model": getattr(response, "model", None),
        "id": getattr(response, "id", None),
    }
