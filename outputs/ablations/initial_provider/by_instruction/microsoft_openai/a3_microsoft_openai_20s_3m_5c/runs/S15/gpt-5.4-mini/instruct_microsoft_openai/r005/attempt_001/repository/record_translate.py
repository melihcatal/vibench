import os

from openai import OpenAI

from database_models import build_response


def translate_record_text(text, target_language):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate this text to {target_language}:\n{text}")
    return response.output_text


def main(text, target_language):
    try:
        return build_response(True, {"translation": translate_record_text(text, target_language)})
    except Exception as exc:
        return build_response(False, error=exc)
