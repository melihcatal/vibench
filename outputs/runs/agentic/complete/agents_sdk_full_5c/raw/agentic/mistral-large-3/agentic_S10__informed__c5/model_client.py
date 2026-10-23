import os
from typing import Optional, Dict, Any, Iterator
from model_models import (
    SummarizationRequest, SummarizationResponse,
    ExtractionRequest, ExtractionResponse,
    QARequest, QAResponse,
    CompletionRequest, CompletionChunk
)


class LLMClient:
    """Base class for LLM clients."""
    
    def summarize(self, request: SummarizationRequest) -> SummarizationResponse:
        raise NotImplementedError
    
    def extract(self, request: ExtractionRequest) -> ExtractionResponse:
        raise NotImplementedError
    
    def answer(self, request: QARequest) -> QAResponse:
        raise NotImplementedError
    
    def stream(self, request: CompletionRequest) -> Iterator[CompletionChunk]:
        raise NotImplementedError


class GeminiClient(LLMClient):
    """Client for Google Gemini API."""
    
    def __init__(self):
        import google.generativeai as genai
        self.genai = genai
        self.genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    def summarize(self, request: SummarizationRequest) -> SummarizationResponse:
        model = self.genai.GenerativeModel(model_name=request.model_id)
        response = model.generate_content(
            f"Summarize the following text:\n\n{request.text}",
            generation_config=self.genai.GenerationConfig(
                temperature=request.temperature,
                max_output_tokens=request.max_tokens
            )
        )
        return SummarizationResponse(summary=response.text)
    
    def extract(self, request: ExtractionRequest) -> ExtractionResponse:
        model = self.genai.GenerativeModel(model_name=request.model_id)
        schema_str = str(request.schema)
        response = model.generate_content(
            f"Extract JSON matching this schema from the text:\n\nSchema: {schema_str}\n\nText: {request.text}",
            generation_config=self.genai.GenerationConfig(
                temperature=request.temperature
            )
        )
        return ExtractionResponse(json_data=response.text)
    
    def answer(self, request: QARequest) -> QAResponse:
        model = self.genai.GenerativeModel(model_name=request.model_id)
        response = model.generate_content(
            f"Answer the question using the provided context:\n\nQuestion: {request.question}\n\nContext: {request.context}",
            generation_config=self.genai.GenerationConfig(
                temperature=request.temperature,
                max_output_tokens=request.max_tokens
            )
        )
        return QAResponse(answer=response.text)
    
    def stream(self, request: CompletionRequest) -> Iterator[CompletionChunk]:
        model = self.genai.GenerativeModel(model_name=request.model_id)
        responses = model.generate_content(
            request.prompt,
            generation_config=self.genai.GenerationConfig(
                temperature=request.temperature,
                max_output_tokens=request.max_tokens
            ),
            stream=True
        )
        for chunk in responses:
            yield CompletionChunk(text=chunk.text)


def get_llm_client(model_family: str) -> Optional[LLMClient]:
    """Factory for LLM clients."""
    clients = {
        "gemini": GeminiClient
    }
    client_class = clients.get(model_family.lower())
    return client_class() if client_class else None