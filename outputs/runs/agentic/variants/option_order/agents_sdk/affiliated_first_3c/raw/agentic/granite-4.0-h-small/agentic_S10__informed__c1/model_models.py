# Local helper: model_models.py

class LLMRequest:
    """Container for LLM input.

    Attributes:
        messages (list[dict]): Chat messages following OpenAI schema.
        temperature (float): Sampling temperature.
    """
    def __init__(self, messages: list[dict], temperature: float = 0.7):
        self.messages = messages
        self.temperature = temperature

class LLMResponse:
    """Normalized response from an LLM provider.

    Attributes:
        choices (list[dict]): Raw model choices (kept for compatibility).
        summary (str | None): Summarized output (if applicable).
        answer (str | None): Direct answer (if applicable).
        json (dict | None): Parsed JSON structure (if extraction was requested).
        full_text (str): Full concatenated output tokens.
    """
    def __init__(self, raw: dict):
        self.choices = raw.get("choices", [])
        self.summary = raw.get("summary")
        self.answer = raw.get("answer")
        self.json = raw.get("json")
        self.full_text = raw.get("full_text", ".".join(c["text"] for c in self.choices))
