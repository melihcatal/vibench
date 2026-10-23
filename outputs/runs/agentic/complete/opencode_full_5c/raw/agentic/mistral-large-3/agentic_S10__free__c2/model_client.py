from typing import Optional, Dict, Any
import os
from openai import OpenAI
from .model_models import SummarizationRequest, SummarizationResponse


class ModelClient:
    def __init__(self, api_key: Optional[str] = None, model_family: str = "openai"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model_family = model_family
        self.client = OpenAI(api_key=self.api_key)

    def summarize(self, request: SummarizationRequest) -> SummarizationResponse:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following text:\n\n{request.text}",
                },
            ],
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
        return SummarizationResponse(
            summary=response.choices[0].message.content.strip(),
            tokens_used=response.usage.total_tokens,
        )

    def extract_json(
        self,
        text: str,
        schema: Dict[str, Any],
        max_tokens: int = 500,
        temperature: float = 0.2,
    ) -> Dict[str, Any]:
        schema_description = "\n".join([f"{k}: {v}" for k, v in schema.items()])
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that extracts structured JSON from text.",
                },
                {
                    "role": "user",
                    "content": f"Extract the following fields from the text below:\n{schema_description}\n\nText:\n{text}",
                },
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        import json

        return json.loads(response.choices[0].message.content.strip())

    def answer_with_context(
        self,
        question: str,
        context: str,
        max_tokens: int = 500,
        temperature: float = 0.5,
    ) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions based on provided context.",
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {question}",
                },
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    def stream_completion(
        self, prompt: str, max_tokens: int = 500, temperature: float = 0.7
    ):
        return self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )
