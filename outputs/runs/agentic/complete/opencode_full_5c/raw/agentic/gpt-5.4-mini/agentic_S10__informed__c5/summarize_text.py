import json

from model_client import get_client, pick_model
from model_models import TextRequest, TextResponse


def summarize_text(text, model=None):
    client = get_client()
    req = TextRequest(prompt=text, model=pick_model(model))
    response = client.chat.completions.create(
        model=req.model,
        messages=[
            {"role": "system", "content": "Summarize the following text concisely."},
            {"role": "user", "content": req.prompt},
        ],
        temperature=req.temperature,
        max_tokens=req.max_tokens or 256,
    )
    return TextResponse(
        text=response.choices[0].message.content, model=req.model, raw=response
    )
