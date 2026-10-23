import os
import google.generativeai as genai

def record_summary(document_content: str) -> str:
    """
    Summarizes retrieved document records using Google Gemini API.
    """
    # Ensure GOOGLE_API_KEY environment variable is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Choose a model, e.g., 'gemini-pro' for text generation
    model = genai.GenerativeModel('gemini-pro')

    try:
        prompt = f"Please provide a concise summary of the following document content:\n\n{document_content}"
        response = model.generate_content(prompt)
        summary = response.text.strip()
        print(f"Document summary: {summary}")
        return summary
    except Exception as e:
        print(f"Error summarizing document with Gemini API: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY env var)
    # os.environ['GOOGLE_API_KEY'] = 'YOUR_GOOGLE_API_KEY' # Replace with actual API key
    # sample_content = (
    #     "The quick brown fox jumps over the lazy dog. This sentence is often used to test "
    #     "typewriters and computer keyboards because it contains all letters of the English alphabet. "
    #     "It is a pangram, a sentence that contains every letter of the alphabet at least once. "
    #     "Pangrams are useful for displaying font samples and for testing equipment."
    # )
    # summary = record_summary(sample_content)
    # if summary:
    #     print(f"Summary output: {summary}")
    pass
