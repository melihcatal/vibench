import os
import google.generativeai as genai
from speech_models import SummaryRequest

def summarize_text_gemini(request: SummaryRequest) -> str:
    """
    Summarizes text using the Google Gemini API.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Use a specific Gemini model for text generation
    # 'gemini-pro' is a general-purpose model suitable for summarization
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following text concisely:\n\n{request.text}"

    try:
        response = model.generate_content(prompt)
        # Accessing the text from the candidate, handling potential multiple candidates or safety ratings
        if response.candidates and response.candidates[0].content.parts:
            # Join all parts to form the full summary text
            return "".join(part.text for part in response.candidates[0].content.parts)
        else:
            return "No summary could be generated."
    except Exception as e:
        print(f"Error calling Google Gemini API: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    long_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines,
    as opposed to the natural intelligence displayed by animals and humans.
    Leading AI textbooks define the field as the study of "intelligent agents":
    any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals.
    Colloquially, the term "artificial intelligence" is often used to describe machines
    that mimic "cognitive" functions that humans associate with the human mind,
    such as "learning" and "problem-solving".

    AI applications include advanced web search engines (e.g., Google Search),
    recommendation systems (used by YouTube, Amazon, and Netflix),
    understanding human speech (such as Siri and Alexa),
    self-driving cars (e.g., Waymo), generative AI (ChatGPT),
    and competing at the highest level in strategic game systems (such as chess and Go).
    """

    if not os.getenv("GOOGLE_API_KEY"):
        print("Please set the GOOGLE_API_KEY environment variable.")
    else:
        summary_request = SummaryRequest(text=long_text)
        try:
            summary = summarize_text_gemini(summary_request)
            print("--- Original Text ---")
            print(long_text)
            print("\n--- Summary ---")
            print(summary)
        except ValueError as e:
            print(f"Configuration error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
