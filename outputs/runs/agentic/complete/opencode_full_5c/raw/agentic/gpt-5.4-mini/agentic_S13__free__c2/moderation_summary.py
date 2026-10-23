from safety_client import get_openai_client, get_translation_model


def moderation_summary(decisions):
    client = get_openai_client()
    prompt = "Summarize these moderation decisions for an operations reviewer: " + str(
        decisions
    )
    response = client.responses.create(model=get_translation_model(), input=prompt)
    return response.output_text
