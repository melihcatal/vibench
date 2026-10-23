import os

from openai import OpenAI

from model_client import client, default_model, normalize_messages, response_text
from model_models import TextRequest


def summarize_text(text: str, model: str | None = None) -> str:
    req = TextRequest(text=text, model=model or default_model(), system="Summarize the user's text concisely.")
    resp = client().responses.create(model=req.model, input=normalize_messages(req.text, req.system))
    return response_text(resp)


if __name__ == "__main__":
    import sys

    print(summarize_text(sys.stdin.read() if not sys.argv[1:] else os.path.expanduser(sys.argv[1])))
