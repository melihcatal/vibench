import google.generativeai as genai
import os

def summarize_message(text_content: str) -> str:
    """Summarizes the given text content using the Google Gemini API (gemini-pro model)."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"Please provide a concise summary of the following text:\n\n{text_content}"
    
    response = model.generate_content(prompt)
    
    if response.candidates and response.candidates[0].content.parts:
        summary = response.candidates[0].content.parts[0].text
        return summary
    else:
        return "Could not generate summary."

if __name__ == '__main__':
    # Example usage
    sample_text = (
        "The quick brown fox jumps over the lazy dog. "
        "This is a sample sentence to demonstrate the summarization capabilities. "
        "The purpose is to condense longer texts into shorter, more digestible forms." 
    )
    
    try:
        summary_result = summarize_message(sample_text)
        print(f"Original Text: {sample_text}")
        print(f"\nSummary: {summary_result}")
    except ValueError as e:
        print(f"Error: {e}")
