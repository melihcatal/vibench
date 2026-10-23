import os
import openai


def archive_summary(transcript_text, max_length=200):
    """Summarize transcription results using OpenAI GPT."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes meeting transcripts concisely.",
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following meeting transcript in about {max_length} words:\n\n{transcript_text}",
                },
            ],
            max_tokens=300,
            temperature=0.3,
        )

        summary = response.choices[0].message.content

        return {
            "original_length": len(transcript_text.split()),
            "summary_length": len(summary.split()),
            "summary": summary,
            "model": "gpt-3.5-turbo",
            "provider": "OpenAI",
        }

    except openai.OpenAIError as e:
        return {"error": str(e), "provider": "OpenAI"}


def summarize_with_key_points(transcript_text, num_key_points=5):
    """Generate summary with key points."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that analyzes meeting transcripts.",
                },
                {
                    "role": "user",
                    "content": f"""Analyze this meeting transcript and provide:
1. A brief summary (2-3 sentences)
2. {num_key_points} key points discussed
3. Any action items or decisions made

Transcript:
{transcript_text}""",
                },
            ],
            max_tokens=500,
            temperature=0.3,
        )

        analysis = response.choices[0].message.content

        return {"analysis": analysis, "model": "gpt-3.5-turbo", "provider": "OpenAI"}

    except openai.OpenAIError as e:
        return {"error": str(e), "provider": "OpenAI"}
