from safety_client import post
from safety_models import SafetyBatchRequest, normalize_text


def moderate_batch(texts, language: str = None):
    req = SafetyBatchRequest(
        texts=[normalize_text(t) for t in texts], language=language
    )
    return post(
        "/contentsafety/text:analyze?mode=batch",
        {"texts": req.texts, "language": req.language},
    )
