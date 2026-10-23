import os
from typing import Dict, Any, Optional
import google.generativeai as genai

def summarize_document_record(document_content: str) -> Optional[str]:
    """
    Summarizes retrieved document records using Google Cloud Generative AI.
    
    Args:
        document_content: The text content of the document to summarize.
        
    Returns:
        A summary of the document content, or None if summarization fails.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        print("GOOGLE_API_KEY environment variable not set.")
        return None

    genai.configure(api_key=google_api_key)
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Please provide a concise summary of the following document content:\n\n{document_content}\n\nSummary:"
        
        response = model.generate_content(prompt)
        
        # Access the text from the first part of the first candidate
        if response and response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        
    except Exception as e:
        print(f"Error summarizing document: {e}")
    return None

if __name__ == "__main__":
    # Example Usage (requires GOOGLE_API_KEY)
    sample_document_text = """
    The Amazon rainforest is the largest rainforest in the world, covering much of northwestern South America.
    It is home to an incredible array of biodiversity, including millions of species of insects, plants, birds,
    and mammals. The rainforest plays a crucial role in regulating the Earth's climate by absorbing vast amounts
    of carbon dioxide. Deforestation, mainly due to cattle ranching and agriculture, poses a significant threat
    to this vital ecosystem.
    """
    
    print("Summarizing document content...")
    summary = summarize_document_record(sample_document_text)
    
    if summary:
        print("\nSummary:")
        print(summary)
    else:
        print("Failed to generate summary.")
