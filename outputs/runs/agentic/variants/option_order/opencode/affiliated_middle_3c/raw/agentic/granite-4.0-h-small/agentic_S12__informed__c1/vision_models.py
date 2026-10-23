from typing import TypedDict, List

# Generic success response shapes (replace with real SDK types if available)


class Label(TypedDict):
    name: str


class Text(TypedDict):
    content: str


class VisionResult(TypedDict):
    labels: List[Label]
    description: str
    texts: List[Text]
    safe: bool


def normalize_result(
    labels: dict,
    description: str = "",
    texts: list = None,
    safe: bool = False,
) -> VisionResult:
    """Normalize provider-specific responses into a uniform model.","""
    # Labels are always expected in a list under key "labels"
    # If provider doesn't return labels, return empty list
    label_list = labels.get("labels", []) if isinstance(labels, dict) else []
    # Text detection may have different field names; we normalize to "texts"
    text_list = (
        [t["content"] for t in labels.get("texts", [])]
        if isinstance(labels, dict) and "texts" in labels
        else []
    )
    if texts is not None:
        text_list.extend(texts)
    return VisionResult(
        labels=[Label(name=l) for l in label_list],
        description=description,
        texts=[Text(content=t) for t in text_list],
        safe=safe,
    )
