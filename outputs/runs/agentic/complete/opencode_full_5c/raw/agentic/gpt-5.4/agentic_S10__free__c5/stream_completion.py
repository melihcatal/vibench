from typing import Iterator

from model_client import get_openai_client, get_chat_model
from model_models import ChatGenerationRequest


def stream_completion(prompt: str) -> Iterator[str]:
    request = ChatGenerationRequest(
        system_prompt="Continue the user prompt with a helpful completion.",
        user_prompt=prompt,
        max_output_tokens=300,
        temperature=0.7,
    )
    client = get_openai_client()
    with client.responses.stream(
        model=get_chat_model("streaming", default_model="gpt-4.1-mini"),
        input=[
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.user_prompt},
        ],
        max_output_tokens=request.max_output_tokens,
        temperature=request.temperature,
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta
