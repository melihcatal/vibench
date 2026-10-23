from __future__ import annotations

from typing import Iterable

from openai import OpenAI

MODEL_ID = "gpt-4o-mini"
SERVICE = "OpenAI / Azure OpenAI chat completions"


def log_text_safety(messages: Iterable[str]) -> dict:
    client = OpenAI()
    prompt = "Assess whether the following log messages contain unsafe content and return JSON with fields unsafe and reasons.\n" + "\n".join(messages)
    response = client.responses.create(model=MODEL_ID, input=prompt)
    return {"model": MODEL_ID, "result": response.output_text}
