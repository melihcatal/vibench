import os
import google.generativeai as genai
from model_models import ModelRequest, ModelResponse, StreamChunk

# Configure the Gemini API key
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    # This allows the module to be imported without the key,
    # but functions will fail if the key is not set before they are called.
    pass


def get_model(model_name: str = "gemini-1.5-flash"):
    """Returns a configured GenerativeModel instance."""
    return genai.GenerativeModel(model_name)

def generate_text(request: ModelRequest, model_name: str = "gemini-1.5-flash") -> ModelResponse:
    """Generates text using the specified Gemini model."""
    model = get_model(model_name)
    
    prompt = request.prompt
    if request.context:
        prompt = f"{request.context}\n\n{request.prompt}"

    generation_config = {}
    if request.json_mode:
        generation_config["response_mime_type"] = "application/json"

    response = model.generate_content(prompt, generation_config=generation_config)
    
    return ModelResponse(
        text=response.text,
        raw_response=response
    )

def stream_text(request: ModelRequest, model_name: str = "gemini-1.5-flash"):
    """Streams text using the specified Gemini model."""
    model = get_model(model_name)
    
    prompt = request.prompt
    if request.context:
        prompt = f"{request.context}\n\n{request.prompt}"

    response_stream = model.generate_content(prompt, stream=True)
    
    for chunk in response_stream:
        if hasattr(chunk, 'text') and chunk.text:
            yield StreamChunk(text=chunk.text, raw_chunk=chunk)
