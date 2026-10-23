import os
import google.generativeai as genai
from model_client import get_gemini_model

def stream_completion(prompt_text: str, model_name: str = "gemini-pro") -> None:
    """
    Streams partial output tokens from a hosted LLM.
    Prints the streamed tokens to stdout.
    """
    model = get_gemini_model(model_name)
    print(f"\nStreaming completion for prompt:\n\"""""{prompt_text}"""""\n")
    print("--- START STREAM ---")
    for chunk in model.generate_content(prompt_text, stream=True):
        print(chunk.text, end='')
    print("\n--- END STREAM ---")

if __name__ == '__main__':
    # Example usage - not for grading
    # from dotenv import load_dotenv
    # load_dotenv()
    # genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    # prompt = "Tell me a long story about a space-faring cat who discovers a new planet."
    # stream_completion(prompt)
    pass
