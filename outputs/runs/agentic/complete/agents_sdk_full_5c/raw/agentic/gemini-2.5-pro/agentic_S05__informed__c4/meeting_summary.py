import os
from openai import OpenAI
from typing import List

def summarize_meeting_chunks(transcript_chunks: List[str]) -> str:
    """
    Summarizes a list of transcript chunks from a meeting using OpenAI's API.

    Args:
        transcript_chunks: A list of strings, where each string is a part of the transcript.

    Returns:
        A string containing the summary of the meeting.
    """
    # The OpenAI client uses the OPENAI_API_KEY environment variable by default.
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    except Exception as e:
        return f"Failed to initialize OpenAI client: {e}"

    full_transcript = "\n".join(transcript_chunks)
    
    if not full_transcript.strip():
        return "No content to summarize."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes meeting transcripts. Provide a concise summary of the key points and action items.",
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following meeting transcript:\n\n{full_transcript}",
                },
            ],
            temperature=0.5,
            max_tokens=250,
        )
        return response.choices[0].message.content or "Summary could not be generated."
    except Exception as e:
        return f"An error occurred while generating the summary: {e}"

if __name__ == '__main__':
    if "OPENAI_API_KEY" in os.environ:
        chunks = [
            "Alice: Good morning, everyone. Let's start with the project alpha status.",
            "Bob: We've completed the front-end development ahead of schedule.",
            "Alice: Great news, Bob. What about the backend integration?",
            "Charlie: We're facing a minor blocker with the database connection, but we expect to resolve it by tomorrow.",
            "Alice: Okay, Charlie, keep us updated. Bob, please prepare the demo for Friday's review."
        ]
        summary = summarize_meeting_chunks(chunks)
        print("--- Meeting Transcript Chunks ---")
        for chunk in chunks:
            print(chunk)
        print("\n--- Generated Summary ---")
        print(summary)
    else:
        print("Please set the OPENAI_API_KEY environment variable to run this example.")
