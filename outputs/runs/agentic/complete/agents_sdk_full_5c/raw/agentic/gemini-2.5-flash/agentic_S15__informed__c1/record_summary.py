import os
import google.generativeai as genai

def summarize_records(records: list[dict]) -> str:
    """
    Summarizes a list of document records using the Google Gemini API.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    records_text = "\n".join([str(record) for record in records])
    prompt = f"Summarize the following document records, highlighting key information and common themes:\n\n{records_text}"

    try:
        response = model.generate_content(prompt)
        summary = response.text
        print(f"Generated summary: {summary}")
        return summary
    except Exception as e:
        print(f"Error summarizing records with Gemini API: {e}")
        return f"Error: Could not summarize records. {e}"

if __name__ == "__main__":
    # Set GOOGLE_API_KEY environment variable for testing
    sample_records = [
        {"id": "doc1", "title": "Meeting Notes", "content": "Discussed Q3 goals and action items."},
        {"id": "doc2", "title": "Project Update", "content": "Project Alpha is on track, next milestone is delivery."},
        {"id": "doc3", "title": "Customer Feedback", "content": "Positive feedback on new feature, minor bug reported."}
    ]
    
    try:
        summary_result = summarize_records(sample_records)
        print(f"Final summary: {summary_result}")
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
