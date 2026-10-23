from openai import OpenAI


def meeting_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    transcript = payload["transcript"]
    response = client.responses.create(model=config.get("model", "gpt-4.1-mini"), input=f"Summarize this meeting transcript in concise bullets:\n{transcript}")
    return {"summary": response.output_text, "is_final": True}
