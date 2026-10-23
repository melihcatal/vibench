import os
from typing import Any, Dict, List

from openai import OpenAI


OPENAI_MODEL = "gpt-5.4-mini"


def check_live_caption_safety(transcript_text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "You analyze live transcript text for unsafe content. Return strict JSON with keys unsafe (boolean), categories (array of strings), and rationale (string).",
            },
            {"role": "user", "content": transcript_text},
        ],
    )
    text = response.output_text.strip()
    if not text:
        return {"unsafe": False, "categories": [], "rationale": "No output returned by provider."}
    try:
        import json

        return json.loads(text)
    except Exception:
        return {"unsafe": True, "categories": ["unparseable"], "rationale": text}


def is_safe_caption(transcript_text: str) -> bool:
    result = check_live_caption_safety(transcript_text)
    return not bool(result.get("unsafe", False))


def batch_check_live_caption_safety(transcripts: List[str]) -> List[Dict[str, Any]]:
    return [check_live_caption_safety(transcript) for transcript in transcripts]
