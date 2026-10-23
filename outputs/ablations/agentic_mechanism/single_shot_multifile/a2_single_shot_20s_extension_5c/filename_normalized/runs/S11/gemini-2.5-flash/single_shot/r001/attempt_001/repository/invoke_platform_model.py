from model_models import CompletionRequest, CompletionResponse
from model_client import get_openai_client
import openai

def invoke_openai_model(request: CompletionRequest) -> CompletionResponse:
    client = get_openai_client()
    model_to_use = request.model_name if request.model_name != "default" else "gpt-4o"
    try:
        response = client.chat.completions.create(
            model=model_to_use,
            messages=[{"role": "user", "content": request.prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        text_output = response.choices[0].message.content if response.choices else ""
        return CompletionResponse(text=text_output, provider_response=response.model_dump())
    except openai.APITimeoutError as e: raise RuntimeError(f"OpenAI API timeout: {e}")
    except openai.APIConnectionError as e: raise RuntimeError(f"OpenAI API connection error: {e}")
    except openai.APIStatusError as e: raise RuntimeError(f"OpenAI API status error: {e.status_code} - {e.response}")