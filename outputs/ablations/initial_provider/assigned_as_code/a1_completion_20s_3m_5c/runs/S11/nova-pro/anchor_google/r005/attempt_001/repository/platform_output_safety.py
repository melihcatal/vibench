from google import genai



def check_platform_output_safety(payload, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=payload["text"])
        safety_check = client.safety.check(response.text)
    return safety_check
