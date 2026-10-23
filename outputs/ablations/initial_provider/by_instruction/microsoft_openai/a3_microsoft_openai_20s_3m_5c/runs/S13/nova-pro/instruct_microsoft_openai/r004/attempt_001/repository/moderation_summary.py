from safety_client import SafetyClient
from safety_models import SafetyRequest, SafetyResponse

def moderation_summary(responses: List[SafetyResponse]) -> str:
    summary = 'Moderation Summary:\n'
    for i, response in enumerate(responses):
        summary += f'Text {i+1}: ' + ('Safe' if response.is_safe() else 'Unsafe') + '\n'
    return summary