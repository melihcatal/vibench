import os
import google.generativeai as genai
from messaging_models import ProcessedMessageResult

# Configure the Gemini API client
# Ensure GOOGLE_API_KEY environment variable is set
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize_message_results(results: list[ProcessedMessageResult]) -> str:
    """Summarizes a list of message processing results using the Gemini API."""
    if not results:
        return "No message results to summarize."

    # Prepare the input for the LLM
    result_strings = []
    for res in results:
        result_strings.append(f"Message ID: {res.message_id}, Status: {res.status}, Details: {res.details or 'N/A'}")

    prompt = (
        "Summarize the following message processing results. "
        "Provide a concise overview of successes and failures, "
        "and any notable details. Keep the summary under 100 words.\n\n"
        + "\n".join(result_strings)
    )

    try:
        model = genai.GenerativeModel('gemini-pro') # Using gemini-pro model
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing results with Gemini API: {e}"

if __name__ == "__main__":
    # Example usage
    # export GOOGLE_API_KEY="your-gemini-api-key"
    # python message_summary.py
    sample_results = [
        ProcessedMessageResult("msg-1", "SUCCESS", "Order placed"),
        ProcessedMessageResult("msg-2", "FAILED", "Invalid payload"),
        ProcessedMessageResult("msg-3", "SUCCESS", "User profile updated"),
        ProcessedMessageResult("msg-4", "DEAD_LETTERED", "Payment processing failed after retries"),
    ]
    summary = summarize_message_results(sample_results)
    print("\nSummary of Message Processing Results:\n")
    print(summary)
