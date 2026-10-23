from google import genai



def translate_platform_output(payload, target_language, config=None):
    config = config or {}
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=payload["text"])
        translated_text = client.translation.translate(response.text, target_language=target_language)
    return translated_text
