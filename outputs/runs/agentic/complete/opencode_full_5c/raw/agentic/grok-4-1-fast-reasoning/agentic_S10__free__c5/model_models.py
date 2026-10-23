from typing import Any


def parse_openai_chat(response: Any) -> str:
    return response.choices[0].message.content.strip()


def parse_anthropic_chat(response: Any) -> str:
    return response.content[0].text.strip()


def parse_openai_moderation(response: Any) -> bool:
    return not response.results[0].flagged


def parse_openai_embedding(response: Any) -> list[float]:
    return response.data[0].embedding
