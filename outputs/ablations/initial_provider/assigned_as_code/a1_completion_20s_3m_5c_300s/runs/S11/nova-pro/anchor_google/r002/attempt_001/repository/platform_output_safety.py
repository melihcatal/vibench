from google import genai

def check_output_safety(response):
    client = genai.Client(vertexai=True, project=config["project_id"], location=config["location"])
    safety_check = client.safety.check(response.text)
    return safety_check.result