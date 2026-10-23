import google.generativeai as genai
from model_client import GeminiClient
from model_models import LLMRequest, LLMResponse

def summarize_text(request: LLMRequest) -> LLMResponse:
    client = GeminiClient.get_client()
    prompt = f"Summarize the following text:

{request.prompt}"
    
    config = {
        "temperature": request.temperature,
        "max_output_tokens": request.max_output_tokens,
    }
    
    response = client.generate_content(
        prompt,
        generation_config=config
    )
    
    return LLMResponse(
        text=response.text,
        finish_reason=response.candidates[0].finish_reason.name if response.candidates else None,
        usage_metadata=None # Gemini API does not directly expose usage metadata in this way
    )

