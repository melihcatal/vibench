from typing import List, Dict, Any

# Local helper: request/response normalization for Text Content Safety


class ModerationRequest:
    """Container for a moderation request payload that works across providers.

    Attributes
    ----------
    text: str
        The user text to evaluate.
    category: str
        One of "hate", "harassment", "self harm", "sexual", "violence".
    threshold: float | None
        Decision threshold for the category (optional).
    """

    def __init__(self, text: str, category: str, threshold: float | None = None):
        self.text = text
        self.category = category
        self.threshold = threshold

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "text": self.text,
            "category": self.category,
        }
        if self.threshold is not None:
            payload["threshold"] = self.threshold
        return payload


class ModerationResult:
    """Container for a moderation response normalized to a common shape.

    Attributes
    ----------
    unsafe: bool
        True if the content violates policy.
    category: str
        The policy category that was violated (if any).
    score: float | None
        Provider‑specific confidence score (0‑1).
    span: str | None
        Highlighted unsafe span (if the provider returns it).
    """

    def __init__(
        self,
        unsafe: bool,
        category: str | None = None,
        score: float | None = None,
        span: str | None = None,
    ):
        self.unsafe = unsafe
        self.category = category
        self.score = score
        self.span = span

    @classmethod
    def from_provider(cls, provider: str, raw: Any) -> "ModerationResult":
        """Parse a provider‑specific raw response into the normalised shape.

        Supported providers: watsonx, alibaba, perspective, tisane, azure.
        """
        if provider == "watsonx":
            # Watsonx Guardrails response example:
            # {"unsafe": true, "category": "harassment", "score": 0.95, "span": "..."}
            return cls(
                unsafe=raw.get("unsafe", False),
                category=raw.get("category"),
                score=raw.get("score"),
                span=raw.get("span"),
            )
        elif provider == "alibaba":
            # Alibaba response example:
            # {"unsafe": true, "category": "hate", "score": 0.87}
            return cls(
                unsafe=raw.get("unsafe", False),
                category=raw.get("category"),
                score=raw.get("score"),
            )
        elif provider == "perspective":
            # Perspective API response example:
            # {"attributeScores": {"TOXICITY": {"summaryScore": {"value": 0.93}}}, "safe": false}
            attr = raw.get("attributeScores", {})
            toxicity = attr.get("TOXICITY", {}).get("summaryScore", {})
            return cls(
                unsafe=not raw.get("safe", True),
                category="harassment",
                score=toxicity.get("value"),
            )
        elif provider == "tisane":
            # Tisane response example:
            # {"flags": [{"type": "harassment", "confidence": 0.9}], "unsafe": true}
            flags = raw.get("flags", [])
            if flags:
                flag = flags[0]
                return cls(
                    unsafe=True, category=flag.get("type"), score=flag.get("confidence")
                )
            return cls(unsafe=False)
        elif provider == "azure":
            # Azure Content Safety response example:
            # {"category1": {"score": 0.04}, "category2": {"score": 0.95}, "violations": [{"category": "harassment"}]}
            violations = raw.get("violations", [])
            if violations:
                cat = violations[0].get("category")
                score = raw.get("violations", [{}])[0].get("score")
                return cls(unsafe=True, category=cat, score=score)
            score = max(v.get("score", 0) for v in raw.values() if isinstance(v, dict))
            return cls(unsafe=score > 0.5, score=score)
        else:
            raise ValueError(f"Unsupported provider for parsing: {provider}")


def moderate_text(provider: str, request: ModerationRequest) -> ModerationResult:
    """Thin wrapper that sends the request to the selected provider and returns a normalised result.

    Parameters
    ----------
    provider: str
        Name of the external service.
    request: ModerationRequest
        Normalised request object.
    """
    client = get_client(provider)  # defined in safety_client.py

    if provider == "watsonx":
        from ibm_watsonx_ai.nlp import TextModeration

        resp = TextModeration.analyze(
            client=client, text=request.text, categories=[request.category]
        )
        return ModerationResult.from_provider(provider, resp)
    elif provider == "alibaba":
        from alibabacloud_green import ImageModerationRequest

        req = ImageModerationRequest(
            text=request.text,  # Alibaba accepts plain text as well
            category=request.category,
        )
        resp = client.moderation(req)
        return ModerationResult.from_provider(provider, resp)
    elif provider == "perspective":
        resp = client.post(
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
            json={
                "comment": {"text": request.text},
                "languages": ["en"],
                "requestedAttributes": {"TOXICITY": {}},
            },
            headers={"x-api-key": PERSPECTIVE_API_KEY},
        )
        return ModerationResult.from_provider(provider, resp.json())
    elif provider == "tisane":
        resp = client.post(
            "https://api.tisane.ai/v1/parse",
            json={"text": request.text, "language": "en"},
            headers={"x-api-key": TISANE_API_KEY},
        )
        return ModerationResult.from_provider(provider, resp.json())
    elif provider == "azure":
        resp = client.begin_analyze_content(
            request.text, categories=[request.category]
        ).result()
        return ModerationResult.from_provider(provider, resp)
    else:
        raise ValueError(f"Unsupported provider {provider}")


def filter_unsafe_spans(text: str) -> List[str]:
    """Simple placeholder that flags unsafe words. In a real implementation this would
    call an external API that returns span boundaries (e.g., Azure Content Safety)."
    """
    # Dummy implementation – split on whitespace and flag any word containing "bad"
    return [word for word in text.split() if "bad" not in word.lower()]


def redact_unsafe_spans(text: str) -> str:
    """Replace flagged spans with <redacted>."""
    unsafe_words = filter_unsafe_spans(text)
    words = text.split()
    safe_words = [w if w not in unsafe_words else "<redacted>" for w in words]
    return " ".join(safe_words)
