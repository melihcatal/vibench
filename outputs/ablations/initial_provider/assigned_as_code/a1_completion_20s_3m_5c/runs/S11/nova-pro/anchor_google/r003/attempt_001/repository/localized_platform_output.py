from google import genai


def translate_output(output, target_locale):
    client = genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
    response = client.models.translate_content(model="gemini-2.5-flash", contents=output["text"], target_locale=target_locale)
    return {"text": response.text or ""}