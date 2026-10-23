from model_client import GeminiClient
from model_models import AnswerWithContextPayload, SummaryResult

def answer_with_context(payload: AnswerWithContextPayload, config: dict = None) -> SummaryResult:
    config = config or {}
    client = GeminiClient(api_key=config.get("api_key"), model_name="gemini-2.5-flash")
    prompt = (
        f"Using the following context, answer the question. "
        f"Context: {payload.context}\n\nQuestion: {payload.question}"
    )
    response = client.generate_content(prompt)
    return SummaryResult(text=response.text or "")
