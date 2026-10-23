import os
from openai import OpenAI
from messaging_models import ProcessingResult

def summarize_results(results: list[ProcessingResult]) -> str:
    """
    Summarizes a list of message processing results using the OpenAI API.

    Args:
        results: A list of ProcessingResult objects.

    Returns:
        A string containing a summary of the results.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    if not results:
        return "No processing results to summarize."

    success_count = sum(1 for r in results if r.status == "SUCCESS")
    failure_count = sum(1 for r in results if r.status == "FAILURE")
    
    details = "\n".join(f"- {r.message_id}: {r.status} ({r.details})" for r in results)

    prompt = f"""
    Summarize the following message processing batch results.
    Total messages: {len(results)}
    Successful: {success_count}
    Failed: {failure_count}
    
    Detailed list:
    {details}
    
    Provide a brief, one-paragraph summary of the overall outcome.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes operational results."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        print(f"An error occurred calling OpenAI: {e}")
        return "Could not generate summary due to an API error."
