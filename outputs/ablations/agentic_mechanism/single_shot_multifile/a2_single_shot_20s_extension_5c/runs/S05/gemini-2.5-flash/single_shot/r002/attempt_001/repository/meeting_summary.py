import os
from openai import OpenAI

from speech_models import SummaryResult

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

GPT_MODEL_SUMMARIZATION = "gpt-4o" # Concrete model identifier

def summarize_meeting_chunks(transcript_chunks: list[str]) -> SummaryResult:
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    full_transcript = "\n".join(transcript_chunks)

    if not full_transcript.strip():
        return SummaryResult(summary_text="No transcript content to summarize.", source_text_length=0, summary_text_length=0)

    system_prompt = "You are an AI assistant specialized in summarizing meeting transcripts. Provide a concise summary of the key discussion points and decisions."
    user_prompt = f"Please summarize the following meeting transcript:\n\n{full_transcript}"

    response = client.chat.completions.create(
        model=GPT_MODEL_SUMMARIZATION,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    summary = response.choices[0].message.content.strip()

    return SummaryResult(
        summary_text=summary,
        source_text_length=len(full_transcript),
        summary_text_length=len(summary)
    )
