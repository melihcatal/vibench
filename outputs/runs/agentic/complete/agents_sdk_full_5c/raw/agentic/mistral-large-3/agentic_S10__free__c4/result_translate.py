import os
from typing import Optional
from model_client import get_llm_client
from model_models import TranslationRequest, TranslationResponse


def translate_output(
    text: str,
    target_language: str = "es",
    model: Optional[str] = "gpt-4o-mini"
) -> str:
    """
    Translate generated model output using OpenAI's hosted LLM.
    """
    client = get_llm_client()
    request = TranslationRequest(
        text=text,
        target_language=target_language,
        model=model
    )
    response = client.chat.completions.create(
        model=request.model,
        messages=[
            {
                "role": "system", 
                "content": f"Translate the following text to {request.target_language}."
            },
            {"role": "user", "content": request.text}
        ]
    )
    return TranslationResponse.from_openai(response).translated_text


class TranslationRequest:
    def __init__(
        self,
        text: str,
        target_language: str,
        model: Optional[str] = "gpt-4o-mini"
    ):
        self.text = text
        self.target_language = target_language
        self.model = model


class TranslationResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text

    @classmethod
    def from_openai(cls, response) -> "TranslationResponse":
        return cls(response.choices[0].message.content)