from model_client import HostedLLMClient
from model_models import ModerationRequest, ModerationResponse, ModelConfig


SAFETY_CATEGORIES = [
    "hate",
    "hate/threatening",
    "harassment",
    "harassment/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
]


def check_prompt_safety(
    text: str,
    model: str = "omni-moderation-latest",
    config: ModelConfig | None = None,
) -> ModerationResponse:
    client = HostedLLMClient(config=config)
    request = ModerationRequest(input=text, model=model)
    return client.moderate(request)


def is_content_safe(
    text: str,
    model: str = "omni-moderation-latest",
    config: ModelConfig | None = None,
) -> bool:
    response = check_prompt_safety(text, model=model, config=config)
    return all(not r.flagged for r in response.results)


def get_safety_flags(
    text: str,
    model: str = "omni-moderation-latest",
    config: ModelConfig | None = None,
) -> dict[str, bool]:
    response = check_prompt_safety(text, model=model, config=config)
    flags = {}
    for result in response.results:
        for category, flagged in result.categories.items():
            if flagged:
                flags[category] = True
    return flags


def check_and_filter(
    prompt: str,
    generated_text: str,
    model: str = "omni-moderation-latest",
    config: ModelConfig | None = None,
) -> tuple[bool, ModerationResponse, ModerationResponse]:
    prompt_check = check_prompt_safety(prompt, model=model, config=config)
    output_check = check_prompt_safety(generated_text, model=model, config=config)
    safe = is_content_safe(prompt, model=model, config=config) and is_content_safe(
        generated_text, model=model, config=config
    )
    return safe, prompt_check, output_check


if __name__ == "__main__":
    sample = "This is a completely safe and benign text about programming."
    result = check_prompt_safety(sample)
    print(f"Flagged: {result.results[0].flagged}")
    print(f"Categories: {result.results[0].categories}")
