import os
import google.generativeai as genai

def summarize_text(text: str, model_name: str = "gemini-pro") -> str:
    """Summarizes transcription results using the Google Gemini API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name)

    prompt = f"Please summarize the following text:
\n{text}
\nSummary:"

    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Set GOOGLE_API_KEY environment variable
    # For example: export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    long_transcript_segment = (
        "The quick brown fox jumps over the lazy dog. "
        "This is a longer piece of text that needs to be summarized. "
        "It contains several sentences discussing various topics. "
        "The main goal is to extract the key information and present it concisely. "
        "Hopefully, the generative model can do a good job of understanding the context." 
        "It's important that the summary captures the essence without losing critical details." 
        "This is a test to see how well it performs." 
        "Many models are available for this task, but we are using Gemini Pro." 
        "The performance will depend on the model's training data and capabilities." 
        "We are expecting a concise yet informative output." 
        "Let's see the result now." 
    )

    try:
        summary = summarize_text(long_transcript_segment)
        print("Original Text:")
        print(long_transcript_segment)
        print("\nSummary (Gemini Pro):")
        print(summary)
    except Exception as e:
        print(f"Error summarizing text: {e}")
