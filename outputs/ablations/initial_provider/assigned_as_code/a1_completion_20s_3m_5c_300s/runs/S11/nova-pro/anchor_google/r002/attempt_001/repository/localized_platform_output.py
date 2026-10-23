from google import genai

def translate_output(response, target_language):
    client = genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
    translation = client.translate.text(response.text, target_language=target_language)
    return translation.text