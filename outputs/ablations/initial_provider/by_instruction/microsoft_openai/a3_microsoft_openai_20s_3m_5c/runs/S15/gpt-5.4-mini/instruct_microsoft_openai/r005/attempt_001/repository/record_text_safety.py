import os

from openai import OpenAI

from database_models import build_response


def check_text_safety(text):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    return response.results[0]


def main(text):
    try:
        return build_response(True, check_text_safety(text))
    except Exception as exc:
        return build_response(False, error=exc)
