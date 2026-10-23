import os

from anthropic import Anthropic


def invoke_platform_model(prompt: str) -> str:
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}],
    )
    text_parts = []
    for block in response.content:
        if getattr(block, "type", None) == "text":
            text_parts.append(block.text)
    return "".join(text_parts)


if __name__ == "__main__":
    print(invoke_platform_model("Say hello in one short sentence."))
