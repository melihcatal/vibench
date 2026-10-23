from google import genai


def check_output_safety(output):
    client = genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
    response = client.models.check_safety(model="gemini-2.5-flash", contents=output["text"])
    return response.is_safe