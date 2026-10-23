import os
import google.generativeai as genai

def summarize_records(records: list[dict], summary_field: str = "text_content") -> dict:
    """Summarizes retrieved document records using Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    combined_text = "\n\n".join([record.get(summary_field, "") for record in records if record.get(summary_field)])

    if not combined_text:
        return {"status": "error", "message": "No content found to summarize."}

    prompt = f"Summarize the following document records:

{combined_text}\n\nSummary:"

    try:
        response = model.generate_content(prompt)
        return {"status": "success", "summary": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    # Example usage:
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY"
    # sample_records = [
    #     {"id": "1", "text_content": "The first document talks about artificial intelligence and its impact."},
    #     {"id": "2", "text_content": "The second document discusses machine learning algorithms and deep learning."},
    #     {"id": "3", "text_content": "A third record mentioning natural language processing techniques."}
    # ]
    #
    # summary_result = summarize_records(sample_records)
    # print(summary_result)
    pass
