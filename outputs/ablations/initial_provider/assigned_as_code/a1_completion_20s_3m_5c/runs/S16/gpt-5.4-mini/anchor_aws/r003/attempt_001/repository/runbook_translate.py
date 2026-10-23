from openai import OpenAI


def runbook_translate(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    text = payload["notes"]
    target_language = payload.get("target_language", "English")
    result = client.responses.create(model="gpt-5.4-mini", input=f"Translate this secret-rotation runbook note into {target_language}:\n{text}")
    return {"translation": result.output_text}
