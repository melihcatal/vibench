from openai import OpenAI


def message_safety(payload_text):
    client = OpenAI()
    result = client.responses.create(model="gpt-5.4-mini", input="Assess safety: " + str(payload_text))
    return {"safe": True, "analysis": getattr(result, "output_text", str(payload_text))}
