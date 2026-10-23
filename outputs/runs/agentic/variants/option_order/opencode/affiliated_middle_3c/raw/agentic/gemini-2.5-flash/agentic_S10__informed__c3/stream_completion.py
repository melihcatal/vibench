import os
from model_client import GeminiClient
from model_models import ChatMessage, GenerateContentRequest


def stream_completion(prompt: str, model_name: str = "gemini-pro") -> str:
    """
    Streams partial output tokens from a hosted LLM (Gemini API).
    """
    gemini_client = GeminiClient().get_model(model_name)

    request = GenerateContentRequest(
        contents=[ChatMessage(role="user", content=prompt)],
        model=model_name,
        temperature=0.7,
    )

    full_response_text = ""
    try:
        response_stream = gemini_client.generate_content(
            contents=[
                {"role": msg.role, "parts": [{"text": msg.content}]}
                for msg in request.contents
            ],
            generation_config={"temperature": request.temperature},
            stream=True,
        )
        for chunk in response_stream:
            if (
                chunk.candidates
                and chunk.candidates[0].content
                and chunk.candidates[0].content.parts
            ):
                for part in chunk.candidates[0].content.parts:
                    if hasattr(part, "text"):
                        full_response_text += part.text
            # print(f"Streamed chunk: {full_response_text}") # For real-time display
        return full_response_text.strip()
    except Exception as e:
        print(f"Error during streaming: {e}")
        return ""


if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_API_KEY is set in your environment
    os.environ["GOOGLE_API_KEY"] = os.environ.get(
        "GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY"
    )

    sample_prompt = "Write a short story about a robot who discovers emotions."
    # streamed_story = stream_completion(sample_prompt)
    # print(f"Full streamed story: {streamed_story}")
