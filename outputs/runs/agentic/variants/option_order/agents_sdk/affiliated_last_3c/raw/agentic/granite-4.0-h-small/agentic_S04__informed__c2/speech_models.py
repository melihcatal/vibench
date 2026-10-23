import enum

# Define common transcription configuration options and response fields

class Model(enum.Enum):
    """Supported speech-to-text models for AssemblyAI."""
    EN_USA = "assemblyai-english"
    EN_UK = "assemblyai-english-uk"
    # Add additional language models as needed


class Feature(enum.Enum):
    """Model features that can be toggled."""
    DIARIZATION = "diarization"
    TIMESTAMPED = "timestamp"
    PUNCTUATION = "punctuation"

    @property
    def flag(self) -> str:
        return f"with_{self.value}"

# Helper to build transcription request payload based on selection

def build_request(**overrides) -> dict:
    """Build a request dictionary for AssemblyAI with optional overrides."""
    base = {
        "model": Model.EN_USA.value,
        "boost_performance": True,
    }
    base.update(overrides)
    return base

# Normalization utility for responses (e.g., error handling)

def normalize_response(raw) -> dict:
    """Return a dict or raise an exception if the API indicates a failure."""
    if not raw:
        raise ValueError("Empty API response")
    # The SDK already normalises success vs error, but we keep this simple wrapper
    if isinstance(raw, dict) and raw.get("error"):
        raise RuntimeError(f"API error: {raw['error']}")
    return raw
