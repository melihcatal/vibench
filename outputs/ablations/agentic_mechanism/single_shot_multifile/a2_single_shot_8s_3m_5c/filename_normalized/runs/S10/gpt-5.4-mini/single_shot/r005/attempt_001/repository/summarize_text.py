from openai import OpenAI
from model_client import get_client, get_model_name
from model_models import BuildTextRequest, SummarizeResult


def summarize_text(text: str, *, max_sentences: int = 3, model: str | None = None) -> SummarizeResult:
    client = get_client()
    model_name = model or get_model_name("summary")
    request = BuildTextRequest(task="summarize", input_text=text, max_sentences=max_sentences)
    prompt = request.to_prompt()
    response = client.responses.create(model=model_name, input=prompt)
    output_text = response.output_text if hasattr(response, "output_text") else str(response)
    return SummarizeResult.from_text(output_text, model=model_name)
