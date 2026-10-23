import os
from typing import List
import openai

from messaging_models import ProcessingResult

def summarize_processing_results(results: List[ProcessingResult]) -> str:
    """
    Summarizes a list of message processing results using OpenAI's GPT model.

    Args:
        results: A list of ProcessingResult objects.

    Returns:
        A string containing a summary of the results.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI(api_key=api_key)

    success_count = sum(1 for r in results if r.status == "SUCCESS")
    failure_count = len(results) - success_count
    
    if not results:
        return "No messages were processed."

    prompt_text = f"Summarize the following {len(results)} message processing results. There were {success_count} successes and {failure_count} failures.\n\n"
    for r in results:
        prompt_text += f"- Message ID {r.message_id}: {r.status} - {r.detail}\n"
    
    prompt_text += "\nPlease provide a brief, human-readable summary of the overall outcome."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes operational logs."},
                {"role": "user", "content": prompt_text},
            ]
        )
        summary = response.choices[0].message.content
        return summary
    except openai.APIError as e:
        print(f"OpenAI API error: {e}")
        return f"Failed to generate summary. Processed {success_count} successfully and {failure_count} failed."
