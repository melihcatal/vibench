import json
from safety_models import (
    ModerationResult,
    get_category_summary,
    get_unsafe_spans_summary,
)


def summarize_moderation(results: list[ModerationResult]) -> str:
    """Summarize a list of moderation decisions into a concise markdown report."""
    lines = ["## Moderation Summary"]
    for i, result in enumerate(results, start=1):
        lines.append(f"### Result {i}")
        lines.append(f"**Unsafe:** {result.unsafe}")
        lines.append(f"**Categories:** {get_category_summary(result)}")
        lines.append(f"**Unsafe spans:** {get_unsafe_spans_summary(result)}")
        lines.append("---")
    return "\n".join(lines)


# Example usage (for development purposes only)
if __name__ == "__main__":
    sample = [
        ModerationResult(
            unsafe=True,
            categories={"hate": 0.85, "violence": 0.20},
            unsafe_spans=["hate"],
        ),
        ModerationResult(unsafe=False, categories={"spam": 0.05}),
    ]
    print(summarize_moderation(sample))
