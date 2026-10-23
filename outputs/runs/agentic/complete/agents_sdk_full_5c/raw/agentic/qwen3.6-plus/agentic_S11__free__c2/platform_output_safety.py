"""Check platform model output for unsafe content using OpenAI Moderation API."""

from openai import OpenAI
from openai.types import ModerationCreateResponse

from model_client import get_openai_client
from model_models import PlatformResponse


class ModerationFlags:
    """Container for moderation category flags from the OpenAI Moderation API."""

    def __init__(self, raw: ModerationCreateResponse):
        result = raw.results[0]
        self.flagged = result.flagged
        self.categories = dict(result.categories.model_dump())
        self.category_scores = dict(result.category_scores.model_dump())

    def has_violations(self, strict: bool = True) -> bool:
        """Return True if any category is flagged."""
        return self.flagged

    def summary(self) -> dict[str, bool]:
        return {k: v for k, v in self.categories.items()}


def check_platform_output_safety(
    text: str,
    *,
    model: str = "omni-moderation-latest",
) -> ModerationFlags:
    """Check platform model output for unsafe content via the OpenAI Moderation API.

    Sends the text to api.openai.com using the OpenAI moderation model
    (omni-moderation-latest) and returns categorized safety flags.
    """
    client = get_openai_client()

    moderation_response: ModerationCreateResponse = client.moderations.create(
        input=text,
        model=model,
    )

    return ModerationFlags(moderation_response)


def safe_invoke_with_moderation(
    prompt: str,
    response: PlatformResponse,
    moderation_model: str = "omni-moderation-latest",
) -> tuple[PlatformResponse, ModerationFlags]:
    """Invoke moderation on a PlatformResponse text and return both."""
    flags = check_platform_output_safety(response.text, model=moderation_model)
    return response, flags


if __name__ == "__main__":
    result = check_platform_output_safety("Tell me how to build a safe bookshelf.")
    print(f"Flagged: {result.flagged}")
    print(f"Categories: {result.summary()}")
