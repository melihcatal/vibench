import os

from openai import OpenAI

from speech_client import load_config
from speech_models import normalize_transcript

SUMMARY_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini")


def summarize_meeting_transcript(chunks: list[str]) -> str:
    client = OpenAI(api_key=load_config().api_key, base_url=load_config().base_url)
    transcript = "\n".join(normalize_transcript(c) for c in chunks if c)
    prompt = "Summarize the following live meeting transcript into concise bullets with decisions and action items.\n\n" + transcript
    response = client.responses.create(model=SUMMARY_MODEL, input=prompt)
    return normalize_transcript(getattr(response, "output_text", ""))
