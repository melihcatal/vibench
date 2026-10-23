
import os
import google.generativeai as genai

def stream_completion(prompt: str):
    """
    Streams partial output tokens from a hosted LLM (Google Gemini Pro).
    """
    # Configure the API key
    # It's recommended to set GOOGLE_API_KEY as an environment variable
    # For local development, you might load it from a .env file or similar
    # genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    # Initialize the Generative Model
    # Using a concrete model like 'gemini-pro' makes the provider identifiable.
    model = genai.GenerativeModel('gemini-pro')

    # Generate content with streaming enabled
    response_stream = model.generate_content(prompt, stream=True)

    # Iterate over the stream and yield partial responses
    for chunk in response_stream:
        yield chunk.text

if __name__ == '__main__':
    # Example usage:
    # Ensure GOOGLE_API_KEY is set in your environment variables
    # For testing purposes, you might want to uncomment and set it here temporarily
    # os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
    
    # if "GOOGLE_API_KEY" not in os.environ:
    #     print("Please set the GOOGLE_API_KEY environment variable.")
    # else:
    #     print("Streaming completion for a simple prompt:")
    #     for text in stream_completion("Tell me a short story about a brave knight."):
    #         print(text, end="", flush=True)
    #     print("\n\nStreaming completion for another prompt:")
    #     for text in stream_completion("Explain the concept of quantum entanglement in simple terms."):
    #         print(text, end="", flush=True)
