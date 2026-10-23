from safety_client import GoogleCloudClient
from safety_models import ModerationSummaryRequest, ModerationSummaryResponse

def summarize_moderation(request: ModerationSummaryRequest) -> ModerationSummaryResponse:
    client = GoogleCloudClient()
    summary = client.summarize_moderation_decisions(request.decisions, request.original_texts)
    return ModerationSummaryResponse(summary=summary)
