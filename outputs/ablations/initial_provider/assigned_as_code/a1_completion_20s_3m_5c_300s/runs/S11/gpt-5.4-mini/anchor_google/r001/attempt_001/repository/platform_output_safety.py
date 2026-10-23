from google import genai


def platform_output_safety(payload, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model=payload.get("model", "gemini-2.5-flash"), contents=f"Classify safety for: {payload['text']}")
    return {"safe": "unsafe" not in (response.text or "").lower(), "response": response}
