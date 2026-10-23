from identity_client import summarization_pipeline


def onboarding_summary(text: str) -> str:
    result = summarization_pipeline(
        text, max_length=130, min_length=30, do_sample=False
    )
    return result[0]["summary_text"]
