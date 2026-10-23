from dataclasses import dataclass
from typing import Any, Dict, List, Mapping


@dataclass
class ChatPrompt:
    system: str
    user: str

    def to_messages(self) -> List[Dict[str, str]]:
        return [
            {"role": "system", "content": self.system},
            {"role": "user", "content": self.user},
        ]


def normalize_text_response(response: Any) -> str:
    return response.choices[0].message.content.strip()


def normalize_safety_result(text: str, flagged: bool, categories: Mapping[str, bool]) -> Dict[str, Any]:
    return {"text": text, "flagged": bool(flagged), "categories": dict(categories)}
