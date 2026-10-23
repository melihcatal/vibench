from openai import OpenAI


def moderate_claims(text: str):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Assess whether this identity claim text is safe and return a brief verdict: {text}",
    )
    return response.output_text
