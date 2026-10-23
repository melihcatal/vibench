import os
from openai import OpenAI


def summarize_transcript(transcript_text: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Using a concrete model identifier
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes meeting transcripts concisely.",
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following transcript:\n\n{transcript_text}",
                },
            ],
            temperature=0.7,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error summarizing transcript: {e}")
        return ""


if __name__ == "__main__":
    example_transcript = (
        "The meeting started with a discussion about the Q3 financial results. "
        "Sarah presented the revenue figures, which were up by 15% year-over-year. "
        "Mark then talked about the marketing campaigns for the upcoming product launch. "
        "He mentioned that social media engagement was higher than expected. "
        "Finally, John brought up the challenges with supply chain logistics and proposed some solutions."
        "The team agreed to review the proposals next week."
    )
    summary = summarize_transcript(example_transcript)
    print("\n--- Transcript Summary ---")
    print(summary)
