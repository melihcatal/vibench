import os
from openai import OpenAI
from typing import Dict, Any
import base64


def reviewer_brief_audio(moderation_case: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate spoken briefs for moderation reviewers using OpenAI's Text-to-Speech API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Extract case details
    case_id = moderation_case.get("case_id", "unknown")
    user_text = moderation_case.get("user_text", "")
    moderation_result = moderation_case.get("moderation_result", {})
    decision = moderation_case.get("decision", "pending")

    # Create brief text
    flagged_categories = []
    if moderation_result.get("categories"):
        for category, flagged in moderation_result["categories"].items():
            if flagged:
                flagged_categories.append(category)

    brief_text = f"""
    Moderation Case Brief for Case ID: {case_id}.
    
    User Text: {user_text[:500]}{"..." if len(user_text) > 500 else ""}
    
    Moderation Analysis:
    - Overall Flagged: {"Yes" if moderation_result.get("flagged", False) else "No"}
    - Flagged Categories: {", ".join(flagged_categories) if flagged_categories else "None"}
    - Current Decision: {decision}
    
    Review Instructions:
    1. Verify the moderation categories are accurate.
    2. Check if any context is missing.
    3. Consider user history if available.
    4. Make a final decision: Allow, Remove, or Escalate.
    
    This audio brief was generated for moderator review.
    """

    # Generate speech using OpenAI TTS
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",  # Could also use: shimmer, echo, fable, onyx, nova
            input=brief_text,
            response_format="mp3",
        )

        # Save audio to file
        audio_filename = f"brief_case_{case_id}.mp3"
        audio_path = os.path.join(os.getcwd(), audio_filename)

        with open(audio_path, "wb") as audio_file:
            audio_file.write(response.content)

        # Get file size
        file_size = os.path.getsize(audio_path)

        # Also create a text summary using GPT-4 for reference
        summary_prompt = f"""Create a concise text summary of this moderation case for reviewer reference:

Case ID: {case_id}
User Text: {user_text}
Moderation Result: {moderation_result}
Decision: {decision}

Provide a summary with:
1. Key concerns
2. Recommended review focus
3. Potential resolution options
"""

        summary_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a moderation case summarizer."},
                {"role": "user", "content": summary_prompt},
            ],
            response_format={"type": "json_object"},
        )

        text_summary = eval(summary_response.choices[0].message.content)

        return {
            "case_id": case_id,
            "audio_generated": True,
            "audio_file": audio_filename,
            "audio_path": audio_path,
            "file_size_bytes": file_size,
            "tts_model": "tts-1",
            "voice": "alloy",
            "brief_text": brief_text,
            "text_summary": text_summary,
            "duration_estimate_seconds": len(brief_text.split())
            / 3,  # Rough estimate: 3 words per second
        }

    except Exception as e:
        # Fallback: return text-only brief if TTS fails
        return {
            "case_id": case_id,
            "audio_generated": False,
            "error": str(e),
            "brief_text": brief_text,
            "text_summary": {
                "key_concerns": flagged_categories,
                "review_focus": "Verify moderation categories and context",
                "resolution_options": ["Allow", "Remove", "Escalate"],
            },
        }
