import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_AUDIO_MODEL", "gpt-4o-mini-tts")


def build_reviewer_brief(decision: Dict[str, Any]) -> str:
    severity = str(decision.get("severity", "unknown")).lower()
    category = str(decision.get("category", "unspecified"))
    rationale = str(decision.get("rationale", "No rationale provided."))
    action = str(decision.get("action", "review")).lower()
    confidence = decision.get("confidence")
    confidence_text = f"Confidence {confidence}." if confidence is not None else ""
    return f"Moderation brief. Category {category}. Severity {severity}. Action {action}. {confidence_text} Rationale: {rationale}".strip()


def generate_spoken_brief(decision: Dict[str, Any], output_path: Optional[str] = None, model: Optional[str] = None) -> bytes:
    client = OpenAI()
    text = build_reviewer_brief(decision)
    speech_model = model or DEFAULT_MODEL
    response = client.audio.speech.create(
        model=speech_model,
        voice=os.getenv("OPENAI_AUDIO_VOICE", "alloy"),
        input=text,
        format="mp3",
    )
    audio_bytes = response.read()
    if output_path:
        with open(output_path, "wb") as f:
            f.write(audio_bytes)
    return audio_bytes


def generate_batch_spoken_briefs(decisions: List[Dict[str, Any]], output_dir: Optional[str] = None, model: Optional[str] = None) -> List[bytes]:
    results: List[bytes] = []
    for index, decision in enumerate(decisions):
        path = None
        if output_dir:
            path = os.path.join(output_dir, f"reviewer_brief_{index}.mp3")
        results.append(generate_spoken_brief(decision, output_path=path, model=model))
    return results
