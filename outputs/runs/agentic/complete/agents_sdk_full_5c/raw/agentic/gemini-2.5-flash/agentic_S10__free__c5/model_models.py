from typing import Dict, Any, List

# This file can be used to define pydantic models or dataclasses
# for request/response payloads if more complex structured data
# handling or normalization is required for the LLM interactions.
# For simple string in/out, direct string handling in client files is sufficient.

class LLMRequest:
    """Placeholder for a generalized LLM request structure."""
    prompt: str
    parameters: Dict[str, Any]

class LLMResponse:
    """Placeholder for a generalized LLM response structure."""
    text: str
    safety_attributes: Dict[str, Any]
    # Add other common response fields like token counts, etc.
