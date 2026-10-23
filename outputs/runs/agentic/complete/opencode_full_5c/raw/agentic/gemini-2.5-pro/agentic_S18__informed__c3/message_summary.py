import os
import google.generativeai as genai


def summarize_message_processing(results: str) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"Summarize the following message processing results in one sentence:\n\n{results}"

    response = model.generate_content(prompt)

    return response.text.strip()


if __name__ == "__main__":
    processing_results = """
    - Message 1: Successfully processed.
    - Message 2: Failed due to invalid payload. Sent to dead-letter queue.
    - Message 3: Successfully processed after retry.
    """
    summary = summarize_message_processing(processing_results)
    print("Processing Summary:")
    print(summary)
