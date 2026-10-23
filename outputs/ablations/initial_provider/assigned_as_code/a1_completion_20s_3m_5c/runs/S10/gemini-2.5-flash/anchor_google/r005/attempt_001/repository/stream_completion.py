from model_client import GeminiClient
from model_models import TextPayload, CompletionStreamResult

def stream_completion(payload: TextPayload, config: dict = None) -> CompletionStreamResult:
    config = config or {}
    client = GeminiClient(api_key=config.get("api_key"), model_name="gemini-2.5-flash")
    prompt = "Continue the following text:\n\n" + payload.text
    responses = client.stream_generate_content(prompt)
    tokens = []
    for chunk in responses:
        tokens.append(chunk.text)
    return CompletionStreamResult(tokens=tokens)
