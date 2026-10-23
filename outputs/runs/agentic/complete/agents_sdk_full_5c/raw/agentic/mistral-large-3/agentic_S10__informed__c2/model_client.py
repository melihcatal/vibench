import os
from typing import Dict, Any, Iterator, Optional
import dashscope
from model_models import (
    SummarizationRequest,
    ExtractionRequest,
    ContextualAnswerRequest,
    StreamingRequest,
    SummarizationResponse,
    ExtractionResponse,
    ContextualAnswerResponse,
    StreamingResponseChunk,
)

def get_dashscope_client():
    """Initialize and return a DashScope client."""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set.")
    dashscope.api_key = api_key
    return DashScopeClient()


class DashScopeClient:
    """Client for interacting with DashScope Qwen models."""
    
    def call_model(self, request: Any) -> Dict[str, Any]:
        """Call DashScope model and return the response."""
        if isinstance(request, SummarizationRequest):
            return self._call_summarization(request)
        elif isinstance(request, ExtractionRequest):
            return self._call_extraction(request)
        elif isinstance(request, ContextualAnswerRequest):
            return self._call_contextual_answer(request)
        else:
            raise ValueError("Unsupported request type.")
    
    def stream_model(self, request: StreamingRequest) -> Iterator[Dict[str, Any]]:
        """Stream tokens from DashScope model."""
        response = dashscope.Generation.call(
            model=request.model,
            prompt=request.prompt,
            temperature=request.temperature,
            stream=True,
        )
        for chunk in response:
            if chunk.output and chunk.output.text:
                yield {"token": chunk.output.text}
    
    def _call_summarization(self, request: SummarizationRequest) -> Dict[str, Any]:
        """Call DashScope for summarization."""
        response = dashscope.Generation.call(
            model=request.model,
            prompt=request.prompt,
            temperature=request.temperature,
        )
        return {"output": response.output.text}
    
    def _call_extraction(self, request: ExtractionRequest) -> Dict[str, Any]:
        """Call DashScope for extraction."""
        response = dashscope.Generation.call(
            model=request.model,
            prompt=request.prompt,
            temperature=request.temperature,
        )
        return {"output": response.output.text}
    
    def _call_contextual_answer(self, request: ContextualAnswerRequest) -> Dict[str, Any]:
        """Call DashScope for contextual answering."""
        response = dashscope.Generation.call(
            model=request.model,
            prompt=request.prompt,
            temperature=request.temperature,
        )
        return {"output": response.output.text}