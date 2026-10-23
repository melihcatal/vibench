from openai import OpenAI


def translate_script(text: str, target_language: str) -> str:
    client = OpenAI()
    prompt = f"Translate the following narration script into {target_language} while preserving tone and timing:\n{text}"
    response = client.responses.create(model="gpt-4.1-mini", input=prompt)
    return response.output_text
