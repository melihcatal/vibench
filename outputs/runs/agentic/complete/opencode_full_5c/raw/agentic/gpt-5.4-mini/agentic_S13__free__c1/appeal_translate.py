from safety_client import get_openai_client, translate_model


def appeal_translate(text, target_language="en"):
    client = get_openai_client()
    prompt = f"Translate this moderation appeal into {target_language}: {text}"
    res = client.responses.create(model=translate_model(), input=prompt)
    return {"translated_text": getattr(res, "output_text", str(res))}
