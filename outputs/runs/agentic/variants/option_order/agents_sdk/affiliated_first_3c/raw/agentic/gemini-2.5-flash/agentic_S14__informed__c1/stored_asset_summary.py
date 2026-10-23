import google.generativeai as genai
import os
from storage_models import SummarizationRequest

def summarize_text_content(request: SummarizationRequest) -> str:
    """Summarizes content extracted from a stored asset using Google Gemini API.

    Args:
        request: A SummarizationRequest object.

    Returns:
        The summarized text.
    """
    # Ensure GOOGLE_API_KEY environment variable is set.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel(request.model_name)

    prompt = f"Summarize the following text:

{request.text_content}"

    generation_config = genai.GenerationConfig(
        max_output_tokens=request.max_output_tokens
    )

    response = model.generate_content(
        prompt,
        generation_config=generation_config
    )

    summary = response.text
    print(f"Summarization (model: {request.model_name}): {summary}")
    return summary

if __name__ == '__main__':
    # Example usage (replace with actual values)
    # Ensure GOOGLE_API_KEY environment variable is set.
    # text_to_summarize = """
    # The quick brown fox jumps over the lazy dog. This is a classic pangram, 
    # a sentence that contains every letter of the alphabet at least once. 
    # Pangrams are often used to display typefaces or test typing skills. 
    # This particular pangram is well-known for its conciseness and clarity.
    # """
    # summarize_req = SummarizationRequest(text_content=text_to_summarize, max_output_tokens=50)
    # summary = summarize_text_content(summarize_req)
    # print(f"Original text: {text_to_summarize}\nSummary: {summary}")
    pass
