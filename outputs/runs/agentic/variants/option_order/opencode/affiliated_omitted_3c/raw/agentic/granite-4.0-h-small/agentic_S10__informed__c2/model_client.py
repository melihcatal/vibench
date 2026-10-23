import os

dashscope = None

# Deterministic provider selection based on environment variables
if "DASHSCOPE_API_KEY" in os.environ:
    from dashscope import ChatCompletion

    dashscope = ChatCompletion()

# Helper to perform a generic chat completion using the selected provider
# Returns raw response object from the provider SDK
from typing import Any


def chat_completion(messages: list[dict[str, str]], model: str = "qwen") -> Any:
    if dashscope is None:
        raise RuntimeError("No configured LLM provider. Set DASHSCOPE_API_KEY.")
    return dashscope.chat(model=model, messages=messages)


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     response = chat_completion([{"role": "user", "content": "Summarize python closures"}])
#     print(response.choices[0].message.content)
