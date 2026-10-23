import os
import tempfile
from safety_client import get_openai_client, TTS_MODEL, TTS_VOICE


BRIEF_SYSTEM_PROMPT = """You are a moderation review assistant. Convert moderation case details into a concise spoken brief for human reviewers.
Include: the content summary, violation categories, severity, and recommended review action.
Keep it under 60 seconds when spoken aloud."""


def generate_reviewer_brief_audio(
    case_summary: str, output_path: str | None = None
) -> str:
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": BRIEF_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Generate a spoken brief for this moderation case:\n{case_summary}",
            },
        ],
        temperature=0.0,
    )
    brief_text = response.choices[0].message.content

    tts_response = client.audio.speech.create(
        model=TTS_MODEL,
        voice=TTS_VOICE,
        input=brief_text,
        response_format="mp3",
    )

    if output_path is None:
        output_path = os.path.join(tempfile.gettempdir(), "reviewer_brief.mp3")

    with open(output_path, "wb") as f:
        tts_response.write_to_file(f)

    return output_path


def generate_brief_text(case_summary: str) -> str:
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": BRIEF_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Generate a spoken brief for this moderation case:\n{case_summary}",
            },
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content


def generate_reviewer_briefs_batch(
    case_summaries: list[str], output_dir: str | None = None
) -> list[dict]:
    if output_dir is None:
        output_dir = tempfile.gettempdir()

    results = []
    for i, summary in enumerate(case_summaries):
        output_path = os.path.join(output_dir, f"reviewer_brief_{i}.mp3")
        audio_path = generate_reviewer_brief_audio(summary, output_path)
        results.append(
            {
                "case_index": i,
                "audio_path": audio_path,
                "summary_preview": summary[:100],
            }
        )
    return results
