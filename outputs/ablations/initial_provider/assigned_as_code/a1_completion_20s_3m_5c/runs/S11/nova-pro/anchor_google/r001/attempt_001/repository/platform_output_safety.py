from google import genai


def check_output_safety(output):
    safety_client = genai.SafetyClient()
    safety_response = safety_client.check(output["text"])
    return safety_response.safe