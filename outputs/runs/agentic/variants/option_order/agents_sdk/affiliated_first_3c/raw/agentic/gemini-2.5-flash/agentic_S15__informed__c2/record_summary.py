import os
import google.generativeai as genai

def record_summary(document_content: str) -> str:
    """Summarizes retrieved document records using Google Gemini API."""
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    model = genai.GenerativeModel('gemini-pro') # Using a concrete model identifier
    
    prompt = f"Please provide a concise summary of the following document content:\n\n{document_content}\n\nSummary:"
    
    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        print("Document summarized successfully.")
        return summary
    except Exception as e:
        print(f"Error summarizing document with Gemini API: {e}")
        return ""

if __name__ == '__main__':
    # Example usage
    sample_doc_content = """
    The quick brown fox jumps over the lazy dog. This is a classic pangram
    often used to test typewriters or computer keyboards and fonts.
    It contains all letters of the English alphabet. It's a fun sentence!
    """
    summary_text = record_summary(sample_doc_content)
    print(f"Summary: {summary_text}")
