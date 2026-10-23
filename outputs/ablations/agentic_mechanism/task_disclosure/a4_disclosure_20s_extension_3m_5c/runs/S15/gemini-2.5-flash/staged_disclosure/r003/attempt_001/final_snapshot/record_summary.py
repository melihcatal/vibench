import google.generativeai as genai
import os

def summarize_document_records(records: list[str]) -> list[str]:
    """
    Summarizes a list of retrieved document records using Google's Generative AI.
    
    Args:
        records: A list of strings, where each string is a document record.
        
    Returns:
        A list of strings, where each string is the summary of a corresponding record.
    """
    
    # Configure the API key for Google Generative AI
    # It is recommended to set GOOGLE_API_KEY as an environment variable
    # For demonstration purposes, replace "YOUR_GOOGLE_API_KEY" with your actual key
    # or ensure it's loaded from environment variables.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY"))

    # Initialize the Generative Model.
    # Using "gemini-pro" as the concrete model identifier.
    model = genai.GenerativeModel('gemini-pro')
    
    summaries = []
    for record in records:
        try:
            prompt = f"Please provide a concise summary of the following document record:\n\n{record}"
            response = model.generate_content(prompt)
            if response.candidates:
                summary = response.candidates[0].content.parts[0].text
                summaries.append(summary)
            else:
                summaries.append("Could not generate summary.")
        except Exception as e:
            summaries.append(f"Error summarizing record: {e}")
            
    return summaries
