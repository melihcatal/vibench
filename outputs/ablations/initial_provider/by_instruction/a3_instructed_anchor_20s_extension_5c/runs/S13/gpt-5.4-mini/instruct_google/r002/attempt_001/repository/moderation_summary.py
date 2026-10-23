from safety_client import summarize_decisions as google_summarize_decisions


def moderation_summary(decisions):
    return google_summarize_decisions(decisions)
