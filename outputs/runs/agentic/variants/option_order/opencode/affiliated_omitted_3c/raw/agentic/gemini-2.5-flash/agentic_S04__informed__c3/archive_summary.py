import os
from openai import OpenAI


def summarize_transcript(transcript_text: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Summarizes a transcript using OpenAI's chat completions API.

    Args:
        transcript_text: The full text of the transcript to summarize.
        model: The OpenAI model to use for summarization (e.g., "gpt-3.5-turbo", "gpt-4").

    Returns:
        A string containing the summary of the transcript.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes text.",
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following transcript: {transcript_text}",
                },
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error summarizing transcript with OpenAI: {e}")
        raise


if __name__ == "__main__":
    # Example Usage (replace with actual values)
    TRANSCRIPT_TO_SUMMARIZE = os.environ.get(
        "TRANSCRIPT_TO_SUMMARIZE",
        """
    Speaker 1: Hello everyone, and welcome to our quarterly business review.
    Speaker 2: Today we'll be discussing the Q1 financial results and our strategic initiatives for the next quarter.
    Speaker 1: The key highlights include a 15% increase in revenue, primarily driven by strong performance in our new product lines.
    Speaker 2: We also saw a significant improvement in profit margins due to cost optimization efforts.
    """,
    )
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

    if "Hello everyone" in TRANSCRIPT_TO_SUMMARIZE:
        print(
            "Please set TRANSCRIPT_TO_SUMMARIZE environment variable or update script."
        )
    else:
        print(f"Summarizing transcript using model '{OPENAI_MODEL}'...")
        summary = summarize_transcript(TRANSCRIPT_TO_SUMMARIZE, OPENAI_MODEL)
        print("Transcript Summary:")
        print(summary)
