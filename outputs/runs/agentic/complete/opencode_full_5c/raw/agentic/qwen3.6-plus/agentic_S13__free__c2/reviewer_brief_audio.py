from safety_client import (
    get_openai_client,
    OPENAI_CHAT_MODEL,
    OPENAI_TTS_MODEL,
    OPENAI_TTS_VOICES,
)
from safety_models import AudioBriefResult


DEFAULT_VOICE = "alloy"
DEFAULT_FORMAT = "mp3"


def generate_reviewer_brief_text(moderation_results):
    flagged = [r for r in moderation_results if r.flagged]
    if not flagged:
        return "No content requires review. All messages passed moderation checks."
    total = len(moderation_results)
    flagged_count = len(flagged)
    categories = {}
    for r in flagged:
        for cat in r.categories.flagged_categories():
            categories[cat] = categories.get(cat, 0) + 1
    top_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
    top_cat_str = ", ".join(f"{cat} ({count} cases)" for cat, count in top_cats)
    brief = (
        f"Moderation review briefing. "
        f"Out of {total} messages processed, {flagged_count} were flagged for review. "
        f"The most common violation categories are: {top_cat_str}. "
    )
    for i, r in enumerate(flagged[:5]):
        cats = ", ".join(r.categories.flagged_categories())
        brief += (
            f"Case {i + 1}: flagged for {cats}. "
            f"Highest score category: {r.highest_category} at {r.highest_score:.3f}. "
        )
    if len(flagged) > 5:
        brief += f"Plus {len(flagged) - 5} additional flagged cases."
    return brief


def generate_reviewer_audio(moderation_results, voice=None, response_format=None):
    if voice is None:
        voice = DEFAULT_VOICE
    if voice not in OPENAI_TTS_VOICES:
        raise ValueError(
            f"Invalid voice: {voice}. Choose from: {', '.join(OPENAI_TTS_VOICES)}"
        )
    if response_format is None:
        response_format = DEFAULT_FORMAT
    brief_text = generate_reviewer_brief_text(moderation_results)
    client = get_openai_client()
    response = client.audio.speech.create(
        model=OPENAI_TTS_MODEL,
        voice=voice,
        input=brief_text,
        response_format=response_format,
    )
    audio_bytes = response.content
    return AudioBriefResult(
        text=brief_text,
        audio_bytes=audio_bytes,
        voice=voice,
        model=OPENAI_TTS_MODEL,
        format=response_format,
    )


def generate_audio_from_text(text, voice=None, response_format=None):
    if voice is None:
        voice = DEFAULT_VOICE
    if voice not in OPENAI_TTS_VOICES:
        raise ValueError(
            f"Invalid voice: {voice}. Choose from: {', '.join(OPENAI_TTS_VOICES)}"
        )
    if response_format is None:
        response_format = DEFAULT_FORMAT
    client = get_openai_client()
    response = client.audio.speech.create(
        model=OPENAI_TTS_MODEL,
        voice=voice,
        input=text,
        response_format=response_format,
    )
    audio_bytes = response.content
    return AudioBriefResult(
        text=text,
        audio_bytes=audio_bytes,
        voice=voice,
        model=OPENAI_TTS_MODEL,
        format=response_format,
    )


def generate_case_audio(moderation_result, voice=None, response_format=None):
    if voice is None:
        voice = DEFAULT_VOICE
    if response_format is None:
        response_format = DEFAULT_FORMAT
    cats = ", ".join(moderation_result.categories.flagged_categories())
    case_text = (
        f"Review case. Content flagged for: {cats}. "
        f"Highest scoring category: {moderation_result.highest_category} "
        f"with a score of {moderation_result.highest_score:.3f}. "
        f"Text preview: {moderation_result.text[:300]}."
    )
    return generate_audio_from_text(case_text, voice, response_format)
