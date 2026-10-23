import google.generativeai as genai
import os
from model_models import LLMRequest, LLMResponse, EmbeddingRequest, EmbeddingResponse


def get_gemini_model(model_name: str):
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    return genai.GenerativeModel(model_name)


def call_gemini_generate_content(request: LLMRequest) -> LLMResponse:
    model = get_gemini_model(request.model_name)
    response = model.generate_content(
        request.prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=request.temperature, max_output_tokens=request.max_output_tokens
        ),
    )
    return LLMResponse(text=response.text)


def call_gemini_stream_content(request: LLMRequest):
    model = get_gemini_model(request.model_name)
    responses = model.generate_content(
        request.prompt,
        stream=True,
        generation_config=genai.types.GenerationConfig(
            temperature=request.temperature, max_output_tokens=request.max_output_tokens
        ),
    )
    for response in responses:
        yield response.text


def call_gemini_embed_content(request: EmbeddingRequest) -> EmbeddingResponse:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    result = genai.embed_content(model=request.model_name, content=request.text)
    return EmbeddingResponse(embedding=result["embedding"])
