import json
import openai

def archive_summary(transcript_path: str, model="gpt-4o-mini") -> str:
    """Summarize a completed transcript using OpenAI's GPT models.
    The transcript_path is expected to contain raw transcript text.
    Returns a concise summary.
    """
    # Load the raw transcript
    with open(transcript_path, "r", encoding="utf-8") as f:
        full_text = f.read()
    # Craft system and user messages for a chat completion
    messages = [
        {"role": "system", "content": "You are an AI assistant summarizing meeting transcripts."},
        {"role": "user", "content": f"Summarize the following transcript in no more than 150 words:\n\n{full_text}"},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.3,
    )
    summary = response.choices[0].message.content.strip()
    return summary
