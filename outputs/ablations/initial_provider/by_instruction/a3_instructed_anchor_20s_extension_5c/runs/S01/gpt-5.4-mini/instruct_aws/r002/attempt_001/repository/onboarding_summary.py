from identity_client import sns_client
from identity_models import OnboardingSummaryRequest


def summarize_onboarding(request: OnboardingSummaryRequest):
    client = sns_client()
    message = f"Onboarding summary for {request.user_id} in {request.locale}"
    client.publish(TopicArn=__import__("os").environ["ONBOARDING_SUMMARY_TOPIC_ARN"], Message=message)
    return {"user_id": request.user_id, "locale": request.locale, "summary": message}
