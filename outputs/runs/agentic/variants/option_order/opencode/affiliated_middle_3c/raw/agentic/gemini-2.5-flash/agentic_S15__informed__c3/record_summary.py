import os
import google.generativeai as genai


def summarize_record(document_content: dict) -> str:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    genai.configure(api_key=GOOGLE_API_KEY)

    model = genai.GenerativeModel("gemini-pro")  # Using a concrete model identifier

    # Convert the document content to a string for summarization
    content_string = str(document_content)
    prompt = f"Summarize the following document content: {content_string}"

    response = model.generate_content(prompt)
    return response.text
