import os
import requests

class SupportSummary(TypedDict):
    user_id: str
    email: str
    created_at: str
    locale: str
    profile_status: str  # 'pending', 'active', 'blocked'
    moderation_score: dict | None
    reset_issued: bool

def build_onboarding_summary(user_id: str, email: str, created_at: str, locale: str, profile_status: str, moderation_score: dict | None = None, reset_issued: bool = False) -> SupportSummary:
    return {
        'user_id': user_id,
        'email': email,
        'created_at': created_at,
        'locale': locale,
        'profile_status': profile_status,
        'moderation_score': moderation_score,
        'reset_issued': reset_issued
    }

