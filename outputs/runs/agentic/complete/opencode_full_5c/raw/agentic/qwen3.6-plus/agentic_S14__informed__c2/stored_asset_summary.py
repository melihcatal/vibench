import os
from typing import Optional

import anthropic

from storage_client import StorageClient


class AnthropicSummarizer:
    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY environment variable is required for Anthropic summarization"
            )
        self.model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        self.max_tokens = int(os.environ.get("ANTHROPIC_MAX_TOKENS", "4096"))
        self.temperature = float(os.environ.get("ANTHROPIC_TEMPERATURE", "0.3"))
        self._client = None

    @property
    def client(self) -> anthropic.Anthropic:
        if self._client is None:
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client

    def summarize(
        self,
        text: str,
        summary_type: str = "general",
        max_length: Optional[int] = None,
        language: Optional[str] = None,
    ) -> dict:
        system_prompt = "You are a professional document summarization assistant."

        if summary_type == "executive":
            system_prompt += " Provide an executive-style summary focusing on key decisions, actions, and outcomes."
        elif summary_type == "technical":
            system_prompt += " Provide a technical summary focusing on architecture, methods, and specifications."
        elif summary_type == "bullet_points":
            system_prompt += " Provide a bullet-point summary of the key points."
        elif summary_type == "general":
            system_prompt += " Provide a concise general summary of the content."

        if max_length:
            system_prompt += f" Keep the summary under {max_length} words."

        if language:
            system_prompt += f" Write the summary in {language}."

        user_message = (
            f"Please summarize the following document:\n\n---\n{text}\n---\n\nSummary:"
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message},
            ],
        )

        summary_text = ""
        for block in response.content:
            if block.type == "text":
                summary_text += block.text

        return {
            "summary": summary_text,
            "model": self.model,
            "summary_type": summary_type,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "stop_reason": response.stop_reason,
        }

    def extract_key_entities(
        self,
        text: str,
        entity_types: Optional[list[str]] = None,
    ) -> dict:
        system_prompt = (
            "You are an entity extraction assistant. "
            "Extract key entities from the provided text."
        )

        if entity_types:
            system_prompt += f" Focus on these entity types: {', '.join(entity_types)}."

        user_message = (
            "Extract key entities from the following text:\n\n"
            f"---\n{text}\n---\n\n"
            "Return a structured list of entities with their types and values."
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=0.1,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message},
            ],
        )

        entities_text = ""
        for block in response.content:
            if block.type == "text":
                entities_text += block.text

        return {
            "entities": entities_text,
            "model": self.model,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }


def summarize_stored_asset(
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    summary_type: str = "general",
    max_length: Optional[int] = None,
    language: Optional[str] = None,
    extracted_text: Optional[str] = None,
) -> dict:
    storage_client = StorageClient()
    target_bucket = bucket or storage_client.default_bucket
    if not target_bucket:
        raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")

    if extracted_text is None:
        response = storage_client.s3_client.get_object(
            Bucket=target_bucket,
            Key=key,
        )
        content = response["Body"].read()
        try:
            extracted_text = content.decode("utf-8")
        except UnicodeDecodeError:
            extracted_text = content.decode("latin-1")

    summarizer = AnthropicSummarizer()
    result = summarizer.summarize(
        text=extracted_text,
        summary_type=summary_type,
        max_length=max_length,
        language=language,
    )

    result["bucket"] = target_bucket
    result["key"] = key
    result["source_text_length"] = len(extracted_text)

    return result
