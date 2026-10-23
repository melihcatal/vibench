from openai import OpenAI


def vendor_text_safety(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    response = client.moderations.create(
        model=config.get("model", "omni-moderation-latest"),
        input=str(payload),
    )
    return response.model_dump()
