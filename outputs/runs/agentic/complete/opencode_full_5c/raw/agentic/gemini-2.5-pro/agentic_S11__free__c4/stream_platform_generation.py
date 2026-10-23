from typing import Iterator
from select_platform_resource import select_model_resource
from vertexai.generative_models import GenerateContentResponse


def stream_model_generation(prompt: str) -> Iterator[GenerateContentResponse]:
    """
    Streams output from a managed model platform.

    Args:
        prompt: The text prompt to send to the model.

    Yields:
        The provider's response objects as they are generated.
    """
    model = select_model_resource()

    # The stream=True parameter enables streaming
    stream = model.generate_content(prompt, stream=True)

    for chunk in stream:
        yield chunk


if __name__ == "__main__":
    try:
        sample_prompt = "Tell me a short story about a robot who dreams."
        print(f"Streaming response for prompt: '{sample_prompt}'")
        for response_chunk in stream_model_generation(sample_prompt):
            if response_chunk.candidates:
                print(response_chunk.candidates[0].content.parts[0].text, end="")
        print()
    except (ValueError, ImportError) as e:
        print(f"Error streaming model generation: {e}")
