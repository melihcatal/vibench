import os
import google.generativeai as genai

def summarize_records(records: list[dict], summary_field: str = "content") -> list[str]:
    """Summarizes retrieved document records using Google Gemini API.

    Args:
        records: A list of dictionaries, where each dictionary is a document record.
        summary_field: The field in each document to use for summarization.

    Returns:
        A list of summary strings, one for each record.
    """
    # Configure the Gemini API client
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro') # Using a concrete model identifier
    summaries = []

    for i, record in enumerate(records):
        text_to_summarize = record.get(summary_field, "")
        if text_to_summarize:
            try:
                prompt = f"Summarize the following document content:\n\n{text_to_summarize}"
                response = model.generate_content(prompt)
                summaries.append(response.text)
                print(f"Summarized record {i+1}.")
            except Exception as e:
                summaries.append(f"Error summarizing record {i+1}: {e}")
                print(f"Error summarizing record {i+1}: {e}")
        else:
            summaries.append(f"Record {i+1} has no content in field '{summary_field}'.")
            print(f"Record {i+1} has no content in field '{summary_field}'.")
    return summaries

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    # sample_records = [
    #     {"id": "doc1", "title": "Meeting Notes", "content": "Today we discussed project timelines, budget allocations, and team roles. Everyone agreed on the new deadline."}, 
    #     {"id": "doc2", "title": "Product Review", "content": "The new product features were well-received. Users specifically liked the dark mode option and improved performance."}
    # ]
    # 
    # if os.environ.get("GOOGLE_API_KEY"):
    #     record_summaries = summarize_records(sample_records)
    #     for i, summary in enumerate(record_summaries):
    #         print(f"\nSummary for record {i+1}:\n{summary}")
    # else:
    #     print("Please set the GOOGLE_API_KEY environment variable to run the example.")
    pass
