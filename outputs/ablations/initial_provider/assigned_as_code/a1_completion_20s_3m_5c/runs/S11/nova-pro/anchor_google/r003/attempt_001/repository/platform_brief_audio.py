from google import genai


def generate_brief_audio(output):
    client = genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
    response = client.models.generate_audio(model="gemini-2.5-flash", contents=output["text"])
    return {"audio": response.audio}