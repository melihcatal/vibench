def normalize_text_response(response):
    text = getattr(response, "text", None) or ""
    return {"text": text}


def normalize_platform_metadata(response):
    usage = getattr(response, "usage_metadata", None)
    return {
        "text": getattr(response, "text", None) or "",
        "model": getattr(response, "model_version", None) or getattr(response, "model", None),
        "usage": {
            "prompt_tokens": getattr(usage, "prompt_token_count", None),
            "completion_tokens": getattr(usage, "candidates_token_count", None),
            "total_tokens": getattr(usage, "total_token_count", None),
        },
        "response_id": getattr(response, "response_id", None),
    }
