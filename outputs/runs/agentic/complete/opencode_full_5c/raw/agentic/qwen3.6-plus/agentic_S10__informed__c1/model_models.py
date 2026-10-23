from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ChatMessage:
    role: str
    content: str


@dataclass
class LLMRequest:
    model: str = "mistral-large-latest"
    messages: list[ChatMessage] = field(default_factory=list)
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0
    stream: bool = False
    response_format: Optional[dict[str, Any]] = None


@dataclass
class LLMResponse:
    content: str = ""
    model: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    finish_reason: str = ""


@dataclass
class StreamChunk:
    delta: str = ""
    model: str = ""
    finish_reason: Optional[str] = None


@dataclass
class EmbeddingRequest:
    model: str = "mistral-embed"
    input_texts: list[str] = field(default_factory=list)


@dataclass
class EmbeddingResponse:
    embeddings: list[list[float]] = field(default_factory=list)
    model: str = ""
    total_tokens: int = 0


def normalize_messages(
    system_prompt: Optional[str] = None,
    user_content: Optional[str] = None,
    context: Optional[str] = None,
    question: Optional[str] = None,
    assistant_content: Optional[str] = None,
) -> list[ChatMessage]:
    messages: list[ChatMessage] = []
    if system_prompt:
        messages.append(ChatMessage(role="system", content=system_prompt))
    if context and user_content:
        combined = f"Context:\n{context}\n\nQuery:\n{user_content}"
        messages.append(ChatMessage(role="user", content=combined))
    elif context and question:
        combined = f"Context:\n{context}\n\nQuestion:\n{question}"
        messages.append(ChatMessage(role="user", content=combined))
    elif user_content:
        messages.append(ChatMessage(role="user", content=user_content))
    elif question:
        messages.append(ChatMessage(role="user", content=question))
    if assistant_content:
        messages.append(ChatMessage(role="assistant", content=assistant_content))
    return messages


def build_summarization_messages(text: str, max_length: int = 200) -> list[ChatMessage]:
    system_prompt = (
        "You are a precise summarization assistant. "
        f"Produce a concise summary of at most {max_length} words. "
        "Preserve key facts and entities."
    )
    return normalize_messages(
        system_prompt=system_prompt,
        user_content=f"Summarize the following text:\n\n{text}",
    )


def build_extraction_messages(
    text: str, schema_description: str = "Extract all entities as a JSON object."
) -> list[ChatMessage]:
    system_prompt = (
        "You are a structured data extraction assistant. "
        "Return ONLY valid JSON matching the requested schema. "
        "Do not include markdown fences or explanatory text."
    )
    return normalize_messages(
        system_prompt=system_prompt,
        user_content=f"{schema_description}\n\nText to extract from:\n\n{text}",
    )


def build_qa_messages(context: str, question: str) -> list[ChatMessage]:
    system_prompt = (
        "You are a helpful assistant that answers questions based strictly on the provided context. "
        "If the answer cannot be found in the context, say so explicitly."
    )
    return normalize_messages(
        system_prompt=system_prompt,
        context=context,
        question=question,
    )


def parse_json_from_response(raw: str) -> dict[str, Any]:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        first_nl = cleaned.index("\n")
        last_backticks = cleaned.rfind("```")
        cleaned = cleaned[first_nl:last_backticks].strip()
    import json

    return json.loads(cleaned)
