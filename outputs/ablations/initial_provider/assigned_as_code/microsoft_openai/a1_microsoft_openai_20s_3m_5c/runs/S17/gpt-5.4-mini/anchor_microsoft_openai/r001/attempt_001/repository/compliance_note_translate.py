from openai import OpenAI


def compliance_note_translate(payload=None, config=None):
    payload = payload or {}
    config = config or {}
    client = OpenAI(api_key=config["api_key"])
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate for reviewers: {payload.get('note', '')}",
    )
    return {"translation": response.output_text, "model": "gpt-5.4-mini"}
