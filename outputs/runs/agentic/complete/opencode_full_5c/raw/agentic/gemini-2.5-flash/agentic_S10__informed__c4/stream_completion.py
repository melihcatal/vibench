from model_client import call_gemini_stream_content
from model_models import StreamCompletionRequest


def stream_completion(prompt: str, model_name: str = "gemini-pro"):
    request = StreamCompletionRequest(prompt=prompt, model_name=model_name)
    for chunk in call_gemini_stream_content(request):
        yield chunk
