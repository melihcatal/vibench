import os
import google.generativeai as genai

def summarize_message_results(results_data: list[dict]) -> str:
    """Summarizes a list of message processing results using the Google Gemini API.

    Args:
        results_data: A list of dictionaries, where each dictionary represents a message processing result.
                      Example: [{'message_id': '123', 'status': 'SUCCESS', 'errors': []}, ...]

    Returns:
        A string summary of the processing results.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro') # Using a concrete model identifier

    prompt = f"""Summarize the following message processing results. Highlight any failures or important observations:

{results_data}

Summary:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

if __name__ == '__main__':
    # Example usage
    example_results = [
        {"message_id": "msg-1", "status": "SUCCESS", "processed_data": {"user": "alice"}},
        {"message_id": "msg-2", "status": "FAILED", "errors": ["invalid_payload"]},
        {"message_id": "msg-3", "status": "SUCCESS", "processed_data": {"order": "new"}},
        {"message_id": "msg-4", "status": "DEAD_LETTERED", "errors": ["unrecoverable_error"]}
    ]
    summary = summarize_message_results(example_results)
    print(summary)
