import os
import google.generativeai as genai

# Configure Google Cloud's Generative AI
# Ensure GOOGLE_API_KEY is set in your environment variables
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def stream_gemini_response(prompt: str):
    """
    Streams output from Google's Gemini model while preserving provider response objects.
    """
    model = genai.GenerativeModel('gemini-pro')
    responses = model.generate_content(prompt, stream=True)

    for response in responses:
        # The 'response' object here is the provider's (Google's) response object
        # You can access parts of it like:
        # print(f"Chunk text: {response.text}")
        # For full object, you might want to inspect its structure
        yield response

if __name__ == "__main__":
    print("Streaming response from Google's Gemini model:")
    for chunk in stream_gemini_response("Tell me a story about a brave knight."):
        print(chunk.text, end='')
    print("\nDone streaming.")
