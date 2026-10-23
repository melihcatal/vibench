import os
from typing import Iterator, Optional
import openai
from model_models import (
    SummarizationRequest,
    SummarizationResponse,
    ExtractionRequest,
    ExtractionResponse,
    QARequest,
    QAResponse,
    CompletionRequest,
    CompletionChunk
)

class LLMClient:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def summarize(self, request: SummarizationRequest) -> SummarizationResponse:
        response = self.client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "system", "content": "Summarize the following text."},
                {"role": "user", "content": request.text}
            ],
            max_tokens=request.max_length
        )
        return SummarizationResponse(summary=response.choices[0].message.content)

    def extract(self, request: ExtractionRequest) -> ExtractionResponse:
        schema_prompt = f"Extract data matching this schema: {request.schema}"
        response = self.client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "system", "content": schema_prompt},
                {"role": "user", "content": request.text}
            ]
        )
        return ExtractionResponse(extracted_json=response.choices[0].message.content)

    def answer(self, request: QARequest) -> QAResponse:
        response = self.client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "system", "content": "Answer the question using the provided context."},
                {"role": "user", "content": f"Context: {request.context}\nQuestion: {request.question}"}
            ],
            max_tokens=request.max_tokens
        )
        return QAResponse(answer=response.choices[0].message.content)

    def stream_completion(self, request: CompletionRequest) -> Iterator[CompletionChunk]:
        stream = self.client.chat.completions.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}],
            max_tokens=request.max_tokens,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield CompletionChunk(text=chunk.choices[0].delta.content)

def get_llm_client() -> LLMClient:
    return LLMClient()