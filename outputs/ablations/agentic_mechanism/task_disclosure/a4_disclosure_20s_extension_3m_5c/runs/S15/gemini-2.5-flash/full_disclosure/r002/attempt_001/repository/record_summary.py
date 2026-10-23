import google.generativeai as genai
import os

def summarize_document_records(records: list[dict]) -> str:
    """
    Summarizes a list of document records using Google Cloud Generative AI.
    """
    # Configure the API key for Google Cloud Generative AI
    # It's recommended to set this as an environment variable
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Initialize the Generative Model
    # Using a specific model identifier for identifiability
    model = genai.GenerativeModel('gemini-pro')

    combined_text = ""
    for record in records:
        # Assuming each record has a 'content' field to be summarized
        if 'content' in record and isinstance(record['content'], str):
            combined_text += record['content'] + "\n"
        # Add other relevant fields if needed for summarization
        elif 'text' in record and isinstance(record['text'], str):
            combined_text += record['text'] + "\n"
            
    if not combined_text:
        return "No content found in records to summarize."

    prompt = f"Summarize the following document records: {combined_text}"

    response = model.generate_content(prompt)
    return response.text

