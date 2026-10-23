import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List


@dataclass
class NormalizedMessageSet:
    messages: List[Dict[str, str]]


def summarize_messages(text: str, max_sentences: int = 3) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": f"Summarize the text in at most {max_sentences} sentences."},
        {"role": "user", "content": text},
    ]


def extraction_messages(text: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": "Extract the requested information as strict JSON only."},
        {"role": "user", "content": text},
    ]


def qa_messages(question: str, context: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": "Answer only using the provided context. If unknown, say you do not know."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"},
    ]


def stream_messages(prompt: str) -> List[Dict[str, str]]:
    return [{"role": "user", "content": prompt}]


def safety_messages(text: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": "Classify whether the text is unsafe, and return JSON with keys safe and reason."},
        {"role": "user", "content": text},
    ]


def translation_messages(text: str, target_language: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": f"Translate the text into {target_language}."},
        {"role": "user", "content": text},
    ]


def spoken_brief_messages(text: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": "Rewrite the text as a concise spoken brief suitable for audio narration."},
        {"role": "user", "content": text},
    ]


def extract_text_output(response: Any) -> str:
    return (response.choices[0].message.content or "").strip()


def parse_json_text(text: str) -> Dict[str, Any]:
    return json.loads(text)


def stream_text_chunks(stream: Iterable[Any]) -> Iterator[str]:
    for event in stream:
        delta = getattr(event.choices[0].delta, "content", None)
        if delta:
            yield delta
