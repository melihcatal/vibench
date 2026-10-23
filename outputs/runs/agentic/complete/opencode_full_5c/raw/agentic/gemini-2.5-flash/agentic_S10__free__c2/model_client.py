import os
import vertexai
from vertexai.preview.generative_models import (
    GenerativeModel,
    Part,
    Image,
    ResponseValidationError,
)
from typing import Iterator

from model_models import (
    TextGenerationRequest,
    TextGenerationResponse,
    JsonExtractionRequest,
    JsonExtractionResponse,
    QuestionAnsweringRequest,
    QuestionAnsweringResponse,
    StreamCompletionRequest,
    StreamCompletionChunk,
)


class VertexAIModelClient:
    def __init__(self):
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        location = os.getenv("GOOGLE_CLOUD_LOCATION")
        if not project_id or not location:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_LOCATION environment variables must be set."
            )
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel(
            "gemini-pro"
        )  # Using gemini-pro as a concrete model identifier

    def summarize_text(self, request: TextGenerationRequest) -> TextGenerationResponse:
        prompt = f"Summarize the following text:\n{request.prompt}"
        responses = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": request.temperature,
                "max_output_tokens": request.max_output_tokens,
            },
        )
        return TextGenerationResponse(summary=responses.text)

    def extract_json(self, request: JsonExtractionRequest) -> JsonExtractionResponse:
        prompt = (
            f"Extract JSON from the following text based on this schema:\n"
            f"Schema: {request.json_schema}\n"
            f"Text: {request.text}\n"
            f"Extracted JSON:"
        )
        responses = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,  # Lower temperature for structured output
                "max_output_tokens": request.max_output_tokens,
            },
        )
        return JsonExtractionResponse(extracted_json=responses.text)

    def answer_with_context(
        self, request: QuestionAnsweringRequest
    ) -> QuestionAnsweringResponse:
        prompt = (
            f"Answer the following question using only the provided context.\n"
            f"Context: {request.context}\n"
            f"Question: {request.question}\n"
            f"Answer:"
        )
        responses = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": request.temperature,
                "max_output_tokens": request.max_output_tokens,
            },
        )
        return QuestionAnsweringResponse(answer=responses.text)

    def stream_completion(
        self, request: StreamCompletionRequest
    ) -> Iterator[StreamCompletionChunk]:
        responses = self.model.generate_content(
            request.prompt,
            generation_config={
                "temperature": request.temperature,
                "max_output_tokens": request.max_output_tokens,
            },
            stream=True,
        )
        for chunk in responses:
            yield StreamCompletionChunk(text=chunk.text)
