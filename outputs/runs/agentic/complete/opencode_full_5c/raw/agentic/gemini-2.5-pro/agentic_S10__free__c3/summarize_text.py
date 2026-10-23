from model_client import get_model_client
from model_models import TextResponse


def summarize(long_text: str) -> TextResponse:
    """
    Summarizes the provided long text using a generative model.
    """
    model = get_model_client()
    prompt = f"Please summarize the following text:\n\n{long_text}"
    response = model.generate_content(prompt)

    summary = ""
    finish_reason = None
    if response.parts:
        summary = response.text
    if response.candidates and response.candidates[0].finish_reason:
        finish_reason = response.candidates[0].finish_reason.name

    return TextResponse(text=summary, finish_reason=finish_reason)
