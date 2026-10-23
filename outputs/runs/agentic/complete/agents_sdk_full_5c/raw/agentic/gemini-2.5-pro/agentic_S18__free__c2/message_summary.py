import os
from openai import OpenAI

from messaging_models import ProcessedMessage

def summarize_processing_results(results: list[ProcessedMessage]) -> str:
    """
    Summarizes message processing results using OpenAI's GPT models.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if not results:
        return "No messages were processed."

    successful_count = sum(1 for r in results if r.status == "SUCCESS")
    failed_count = len(results) - successful_count

    prompt = (
        f"Provide a brief, human-readable summary of a message processing batch run.\n"
        f"Total messages processed: {len(results)}\n"
        f"Successful: {successful_count}\n"
        f"Failed: {failed_count}\n\n"
        f"Example successful message ID: {results[0].message_id if successful_count > 0 else 'N/A'}\n"
        "Summarize the outcome."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing system monitoring summaries."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        print(f"An error occurred while summarizing with OpenAI: {e}")
        return "Could not generate summary."
