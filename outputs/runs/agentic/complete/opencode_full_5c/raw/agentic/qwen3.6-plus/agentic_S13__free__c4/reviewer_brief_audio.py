from safety_client import (
    call_tts,
    call_chat,
    OPENAI_TTS_MODEL,
    OPENAI_CHAT_MODEL,
    OPENAI_TTS_VOICE,
)
from safety_models import AudioBrief


def _generate_brief_text(moderation_case):
    case_id = moderation_case.get("case_id", "unknown")
    flagged = moderation_case.get("flagged", False)
    categories = moderation_case.get("categories", [])
    scores = moderation_case.get("category_scores", [])
    user_appeal = moderation_case.get("appeal_text", "")
    original_content = moderation_case.get("original_content", "")

    max_score = 0.0
    primary_category = "none"
    for s in scores:
        if s.get("score", 0) > max_score:
            max_score = s["score"]
            primary_category = s["name"]

    messages = [
        {
            "role": "system",
            "content": "You are a moderation assistant. Generate a concise spoken brief for a human reviewer. Keep it under 100 words. Use clear, professional language.",
        },
        {
            "role": "user",
            "content": f"""Generate a reviewer brief for case {case_id}.

Content was {"flagged" if flagged else "not flagged"}.
Primary violation: {primary_category} (score: {max_score})
Categories: {", ".join(categories) if categories else "none"}
User appeal: {user_appeal if user_appeal else "No appeal submitted"}
Original content preview: {original_content[:200]}

Provide a brief summary for the reviewer to read aloud.""",
        },
    ]

    response = call_chat(
        messages, model=OPENAI_CHAT_MODEL, temperature=0.3, max_tokens=256
    )
    return response.choices[0].message.content.strip()


def generate_reviewer_brief_audio(moderation_case, voice=None, model=None):
    brief_text = _generate_brief_text(moderation_case)
    tts_response = call_tts(
        brief_text,
        voice=voice or OPENAI_TTS_VOICE,
        model=model or OPENAI_TTS_MODEL,
    )
    audio_bytes = tts_response.content
    word_count = len(brief_text.split())
    duration_estimate = word_count / 2.5

    return AudioBrief(
        text=brief_text,
        audio_bytes=audio_bytes,
        format="mp3",
        duration_estimate=round(duration_estimate, 1),
    )


def generate_reviewer_briefs_audio(cases, voice=None, model=None):
    briefs = []
    for case in cases:
        brief = generate_reviewer_brief_audio(case, voice=voice, model=model)
        briefs.append(brief)
    return briefs
