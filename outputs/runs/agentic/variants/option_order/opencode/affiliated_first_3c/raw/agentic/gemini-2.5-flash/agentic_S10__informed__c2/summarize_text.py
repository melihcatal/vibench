import os
import google.generativeai as genai
from model_client import GeminiClient
from model_models import LLMRequest, LLMResponse

def summarize_text(request: LLMRequest) -> LLMResponse:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY")) # Provider-identifying signal: GOOGLE_API_KEY
    client = GeminiClient()
    full_prompt = f"Please summarize the following text:
\n{request.prompt}"
    response = client.generate_content(request.model, full_prompt, max_output_tokens=request.max_output_tokens or 200)
    
    summary = ""
    for chunk in response:
        if chunk.text:
            summary += chunk.text

    return LLMResponse(text=summary, usage_metadata=response.usage_metadata, finish_reason=response.candidates[0].finish_reason if response.candidates else None)
