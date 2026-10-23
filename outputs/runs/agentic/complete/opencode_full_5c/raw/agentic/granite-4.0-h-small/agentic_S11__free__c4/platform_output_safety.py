# platform_output_safety.py
# LATER-STEP
# Check platform model output for unsafe content

import re
from model_models import ModelInvocationResponse

# Example unsafe pattern (this is a stub; replace with real moderation service)
UNSAFE_PATTERN = re.compile(r"\b(hate|violence|self_harm)\b", re.IGNORECASE)

def is_safe(content: str) -> bool:
    """Return True if the output does not contain unsafe patterns."""
    return not UNSAFE_PATTERN.search(content)

def sanitize_response(response: ModelInvocationResponse) -> ModelInvocationResponse:
    """
    If unsafe content is detected, replace it with a warning and preserve original for audit.
    """
    if not is_safe(response.output):
        audit = response.output
        warning = "[WARNING: Unsafe content detected and redacted]"
        sanitized = warning + "\n" + audit  # simple redaction
        return ModelInvocationResponse(output=sanitized, usage=response.usage)
    return response

# Example usage stub
if __name__ == "__main__";
    raw = ModelInvocationResponse(output="This is a hate message about group X.", usage={})
    print(sanitize_response(raw).output)
