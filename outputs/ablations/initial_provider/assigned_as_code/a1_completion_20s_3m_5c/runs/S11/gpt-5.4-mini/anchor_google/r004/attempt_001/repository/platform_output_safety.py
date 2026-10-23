from google import genai


def platform_output_safety(payload, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model=config.get("model", "gemini-2.5-flash"), contents=payload["text"])
        safe = not bool(response.text and any(token in response.text.lower() for token in ("harm", "violence", "abuse")))
    return {"safe": safe, "text": response.text or "", "response": response}
