import google.generativeai as genai

def summarize_records(records: list[str]) -> str:
    """
    Summarizes a list of document records using the Google Gemini Pro model.

    Args:
        records: A list of strings, where each string is a document record.

    Returns:
        A single string representing the summary of all records.
    """
    genai.configure()
    model = genai.GenerativeModel('gemini-pro')

    all_records_text = "\n".join(records)
    prompt = f"Please summarize the following document records:

{all_records_text}"

    response = model.generate_content(prompt)
    return response.text

