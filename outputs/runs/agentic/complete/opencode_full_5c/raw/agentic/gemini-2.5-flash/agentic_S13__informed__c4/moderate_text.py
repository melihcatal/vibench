from safety_client import ContentSafetyClientWrapper
from safety_models import TextContent, ModerationResult


def moderate_single_text(user_text: str) -> ModerationResult:
    client_wrapper = ContentSafetyClientWrapper()
    text_content = TextContent(text=user_text)
    result = client_wrapper.moderate_text(text_content)
    return result
