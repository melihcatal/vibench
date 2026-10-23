from openai import OpenAI

from safety_client import get_openai_client


client: OpenAI = get_openai_client()
TRANSLATION_MODEL = "gpt-4.1-mini"


def appeal_translate(appeal_text: str, target_language: str = "en") -> str:
    prompt = f"Translate the following appeal into {target_language}: {appeal_text}"
    response = client.responses.create(model=TRANSLATION_MODEL, input=prompt)
    return response.output_text
