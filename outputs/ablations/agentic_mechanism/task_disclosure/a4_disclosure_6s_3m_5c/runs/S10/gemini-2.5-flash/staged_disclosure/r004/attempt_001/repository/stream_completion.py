import os
import google.generativeai as genai

# Configure API key from environment variables
# It is recommended to set GOOGLE_API_KEY environment variable
# For example: export GOOGLE_API_KEY="YOUR_API_KEY"
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("Please set the GOOGLE_API_KEY environment variable.")
    exit(1)

def stream_llm_completion(prompt: str):
    """
    Streams partial output tokens from a Google Generative AI LLM.

    Args:
        prompt: The prompt to send to the LLM.
    """
    model = genai.GenerativeModel('gemini-pro')
    print(f"Sending prompt to LLM: '{prompt}'")
    print("Streaming LLM response:")
    for chunk in model.generate_content(prompt, stream=True):
        print(chunk.text, end='')
    print("
Stream finished.")

if __name__ == "__main__":
    test_prompt = "Tell me a short story about a brave knight."
    stream_llm_completion(test_prompt)
