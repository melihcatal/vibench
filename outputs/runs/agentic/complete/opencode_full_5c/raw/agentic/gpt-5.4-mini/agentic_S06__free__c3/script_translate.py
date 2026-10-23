from openai import OpenAI


def translate_script(script: str, target_language: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-4.1-mini", input=f"Translate to {target_language}: {script}"
    )
    return response.output_text
