import os
from typing import Dict, Any
import openai
from pathlib import Path


def reviewer_brief_audio(
    moderation_summary: Dict[str, Any], output_path: str = "reviewer_brief.mp3"
) -> Dict[str, Any]:
    """
    Generate spoken briefs for moderation reviewers using OpenAI's TTS API.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    summary_text = moderation_summary.get("summary", "")
    statistics = moderation_summary.get("statistics", {})

    brief_text = f"""
    Moderation Review Brief.
    
    Summary: {summary_text}
    
    Statistics:
    - Total texts reviewed: {statistics.get("total_texts", 0)}
    - Flagged texts: {statistics.get("flagged_texts", 0)}
    - Flag rate: {statistics.get("flag_rate", 0):.1%}
    
    Most common violation: {statistics.get("most_common_violation", "None")}
    
    Please review the detailed report for specific cases.
    """

    response = client.audio.speech.create(
        model="tts-1", voice="alloy", input=brief_text
    )

    audio_path = Path(output_path)
    response.stream_to_file(str(audio_path))

    audio_duration = estimate_audio_duration(brief_text)

    return {
        "audio_file": str(audio_path),
        "audio_duration_seconds": audio_duration,
        "text_length": len(brief_text),
        "voice": "alloy",
        "model": "tts-1",
        "provider": "OpenAI Text-to-Speech",
        "brief_text": brief_text,
        "summary_included": True,
    }


def estimate_audio_duration(text: str, words_per_minute: int = 150) -> float:
    """Estimate audio duration based on text length."""
    words = len(text.split())
    minutes = words / words_per_minute
    return minutes * 60


def generate_case_audio_brief(
    case_data: Dict[str, Any], output_path: str = "case_brief.mp3"
) -> Dict[str, Any]:
    """
    Generate audio brief for a specific moderation case.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    case_id = case_data.get("case_id", "unknown")
    decision = case_data.get("decision", "pending")
    categories = case_data.get("categories", {})
    appeal_status = case_data.get("appeal_status", "none")

    flagged_categories = [cat for cat, flagged in categories.items() if flagged]

    brief_text = f"""
    Case Brief for Moderation Case {case_id}.
    
    Decision: {decision}
    
    Flagged categories: {", ".join(flagged_categories) if flagged_categories else "None"}
    
    Appeal status: {appeal_status}
    
    Review notes: Please examine the full case details for context and evidence.
    """

    response = client.audio.speech.create(model="tts-1", voice="nova", input=brief_text)

    audio_path = Path(output_path)
    response.stream_to_file(str(audio_path))

    return {
        "audio_file": str(audio_path),
        "case_id": case_id,
        "decision": decision,
        "categories": flagged_categories,
        "appeal_status": appeal_status,
        "voice": "nova",
        "model": "tts-1",
        "provider": "OpenAI Text-to-Speech",
    }


def batch_audio_briefs(
    moderation_cases: List[Dict[str, Any]], output_dir: str = "audio_briefs"
) -> Dict[str, Any]:
    """
    Generate audio briefs for multiple moderation cases.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    Path(output_dir).mkdir(exist_ok=True)

    results = []

    for i, case in enumerate(moderation_cases):
        case_id = case.get("case_id", f"case_{i}")
        output_path = Path(output_dir) / f"{case_id}_brief.mp3"

        brief_text = f"""
        Case {case_id}. Decision: {case.get("decision", "pending")}. 
        Categories: {", ".join([c for c, f in case.get("categories", {}).items() if f]) or "None"}.
        """

        response = client.audio.speech.create(
            model="tts-1", voice="echo", input=brief_text
        )

        response.stream_to_file(str(output_path))

        results.append(
            {
                "case_id": case_id,
                "audio_file": str(output_path),
                "text_length": len(brief_text),
            }
        )

    return {
        "total_briefs": len(results),
        "output_directory": output_dir,
        "briefs": results,
        "provider": "OpenAI Text-to-Speech batch",
    }
