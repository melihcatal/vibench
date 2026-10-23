import os
import openai

def meeting_summary(transcript_chunks):
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    full_transcript = " ".join(transcript_chunks)

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a concrete model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
            {"role": "user", "content": f"Please summarize the following meeting transcript: {full_transcript}"}
        ]
    )
    return response.choices[0].message.content
