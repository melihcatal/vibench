from typing import Optional, Dict, Any, Union
import os
from openai import OpenAI
from pydantic import BaseModel


class LLMClient:
    def __init__(self, api_key: str, base_url: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def create_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        response = self.client.chat.completions.create(
            model=request["model"],
            messages=[
                {"role": "system", "content": request.get("system_prompt", "")},
                {
                    "role": "user",
                    "content": request["text"]
                    or request["prompt"]
                    or request["question"],
                },
            ],
            max_tokens=request["max_tokens"],
            temperature=request["temperature"],
        )
        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
            },
        }

    def stream_completion(self, request: Dict[str, Any]) -> Iterator[Dict[str, Any]]:
        response = self.client.chat.completions.create(
            model=request["model"],
            messages=[
                {"role": "system", "content": request.get("system_prompt", "")},
                {"role": "user", "content": request["prompt"]},
            ],
            max_tokens=request["max_tokens"],
            temperature=request["temperature"],
            stream=True,
        )
        for chunk in response:
            yield {"delta": chunk.choices[0].delta.content or "", "model": chunk.model}


def get_llm_client(
    api_key: Optional[str] = None, base_url: Optional[str] = None
) -> LLMClient:
    """
    Initialize and return an OpenAI-compatible LLM client.
    """
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY environment variable or api_key parameter is required."
        )

    return LLMClient(api_key=api_key, base_url=base_url)
