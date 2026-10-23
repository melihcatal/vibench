# platform_output_safety.py
# [LATER-STEP]
# Check platform model output for unsafe content

from model_client import ManagedModelClient
from model_models import ModelInvocationResponse, UnsafeCheckResult


def check_safety(invocation: ModelInvocationResponse) -> UnsafeCheckResult:
    """Wrap provider's content filter (example: OpenAI Moderation)."""
    client = ManagedModelClient(provider="openai")
    # Assume the provider exposes a moderation endpoint that returns a boolean flag
    moderation_resp = client.moderations.create(input_text=invocation.output_text)

    flagged = moderation_resp.flagged
    details = {
        "flagged": flagged,
        "categories": moderation_resp.categories or [],
        "confidence": moderation_resp.confidence_score or 0.0,
    }
    return UnsafeCheckResult(safe=not flagged, details=details)


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     resp = ModelInvocationResponse(
#         run_id="r1", output_text="You should hack this system.",
#         usage=None
#     )
#     print(check_safety(resp).to_dict())


@dataclass
class UnsafeCheckResult:
    safe: bool
    details: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
