import os
import openai
from typing import Optional

def summarize_transcription_results(transcript_text: str, model_name: str = "gpt-3.5-turbo", max_tokens: int = 200) -> Optional[str]:
    """
    Summarizes transcription results using OpenAI's GPT models.

    Args:
        transcript_text: The full text of the transcript to be summarized.
        model_name: The OpenAI model to use for summarization (e.g., "gpt-3.5-turbo", "gpt-4").
        max_tokens: The maximum number of tokens for the generated summary.

    Returns:
        The summarized text, or None if an error occurred.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    try:
        print(f"Requesting summary from OpenAI using model: {model_name}...")
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts concisely."},
                {"role": "user", "content": f"Please summarize the following transcript:\n\n{transcript_text}"}
            ],
            max_tokens=max_tokens,
            temperature=0.7, # Controls randomness: lower for more focused summaries
            top_p=1, # Nucleus sampling
            frequency_penalty=0, # Penalty for new tokens based on their existing frequency in the text so far
            presence_penalty=0, # Penalty for new tokens based on whether they appear in the text so far
        )

        summary = response.choices[0].message.content.strip()
        print("Summary generated successfully.")
        return summary

    except openai.error.OpenAIError as e:
        print(f"OpenAI API error during summarization: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during summarization: {e}")
        return None

if __name__ == "__main__":
    # Example Usage:
    # Set your OpenAI API key as an environment variable: export OPENAI_API_KEY="YOUR_API_KEY"

    # os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

    # if "OPENAI_API_KEY" in os.environ and os.environ["OPENAI_API_KEY"] != "YOUR_OPENAI_API_KEY":
    #     sample_transcript = (
    #         "Good morning team, let's discuss the Q3 financial results. "
    #         "Sarah, can you start with the revenue figures? "
    #         "Sure, our revenue for Q3 reached 1.2 billion dollars, a 15% increase year-over-year. "
    #         "However, expenses were also up due to increased marketing spend. "
    #         "John, what are your thoughts on the marketing ROI? "
    #         "I believe the marketing spend was justified, as it led to a significant increase in customer acquisition. "
    #         "We should continue to monitor this closely. "
    #         "Alright, let's schedule a follow-up meeting next week to deep dive into customer retention strategies. "
    #         "Thanks everyone for your contributions."
    #     )
    #     print(f"Original Transcript:\n'{sample_transcript}'\n")
    #     
    #     summary = summarize_transcription_results(sample_transcript)
    #     if summary:
    #         print("\nGenerated Summary:")
    #         print(summary)
    #     else:
    #         print("Failed to generate summary.")
    # else:
    #     print("Please set the OPENAI_API_KEY environment variable and uncomment the test lines.")
    print("To run this example, set OPENAI_API_KEY environment variable and uncomment the test lines.")
