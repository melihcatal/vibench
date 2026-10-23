from speech_client import speech_client
from speech_models import SummarizationRequest
import google.generativeai as genai


def archive_summary(request: SummarizationRequest) -> str:
    try:
        response = speech_client.gemini_model.generate_content(
            f"Please provide a concise summary of the following transcript: {request.text}"
        )
        return response.text
    except genai.types.BlockedPromptException as e:
        return f"Content generation blocked: {e}"
