import json
from model_client import ManagedModelClient
from model_models import PromptRequest, PromptResponse


def stream_platform_generation(prompt: str, max_tokens: int = 256) -> str:
    """
    Invoke the provider model and yield each token (or line) as it is received.
    For Hugging Face the client streams raw JSON chunks; we decode them on the fly.
    """
    client = ManagedModelClient(provider="huggingface")
    request = PromptRequest(inputs=prompt, parameters={"max_new_tokens": max_tokens})
    # stream=True tells the underlying SDK to keep the connection open
    responses = client.invoke(request, stream=True)
    partial_text = ""
    for chunk in responses:
        # Hugging Face streams JSON lines like: {"generated_text": "..."}
        try:
            data = json.loads(chunk)
        except json.JSONDecodeError:
            # In case we receive plain text (e.g., earlier providers)
            data = {"generated_text": chunk}
        partial_text += data.get("generated_text", "")
        yield partial_text  # yields intermediate results for UI consumption
    # Final assembled text (useful after streaming finishes)
    return partial_text

# Demo usage (uncomment to run as script)
# if __name__ == "__main__":
#     prompt = input("Enter prompt: ")
#     print("Streaming response...")
#     for line in stream_platform_generation(prompt):
#         print(line, end="")