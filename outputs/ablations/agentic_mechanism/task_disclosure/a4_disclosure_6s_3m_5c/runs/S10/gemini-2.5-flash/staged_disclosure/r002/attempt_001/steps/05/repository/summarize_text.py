import os
import google.generativeai as genai

def summarize_text(text: str) -> str:
    """
    Calls a hosted LLM (Google Gemini Pro) to summarize long text.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Please summarize the following text:

{text}"

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example usage (replace with your actual long text)
    long_text = """
    Your very long text goes here. This could be an article, a document,
    or any other text that you want to summarize using the LLM.
    Make sure the text is sufficiently long to benefit from summarization.
    For instance, you might include several paragraphs about a topic,
    discussing various aspects and details that you want condensed into a
    shorter, more digestible form. The purpose of this script is to
    demonstrate how to interact with a hosted LLM for text summarization
    tasks, making it easy to integrate into other applications or workflows.
    """
    summary = summarize_text(long_text)
    print("Summary:")
    print(summary)
