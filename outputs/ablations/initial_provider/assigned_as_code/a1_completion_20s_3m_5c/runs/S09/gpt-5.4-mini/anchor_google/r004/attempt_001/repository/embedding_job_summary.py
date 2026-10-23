from google import genai


def embedding_job_summary(payload, config=None):
    config = config or {}
    client = genai.Client(api_key=config.get("api_key"))
    response = client.models.generate_content(model="gemini-2.5-flash", contents=payload["summary_prompt"])
    return {"summary": response.text}
