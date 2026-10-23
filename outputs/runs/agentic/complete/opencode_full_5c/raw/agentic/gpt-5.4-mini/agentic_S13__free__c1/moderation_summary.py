from safety_client import get_openai_client, moderation_model


def moderation_summary(decisions):
    client = get_openai_client()
    prompt = f"Summarize these moderation decisions for ops review: {decisions}"
    res = client.responses.create(model=moderation_model(), input=prompt)
    return {"summary": getattr(res, "output_text", str(res))}
