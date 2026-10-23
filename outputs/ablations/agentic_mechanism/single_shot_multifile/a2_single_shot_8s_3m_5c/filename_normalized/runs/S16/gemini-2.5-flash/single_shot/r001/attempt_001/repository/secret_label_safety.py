import os
from typing import List
from security_client import SecurityClients
from security_models import ModerationResult
from azure.cognitiveservices.contentmoderator.models import Screen

def check_secret_text_safety(text_to_check: str) -> ModerationResult:
    client = SecurityClients.get_azure_content_moderator_client()
    try:
        screen_result = client.text_moderation.screen_text(
            text_content=text_to_check,
            language="eng",
            autocorrect=True,
            p_i_i=True,
            list_id=None
        )

        is_safe = True
        flagged_terms = []

        if screen_result.terms:
            is_safe = False
            for term in screen_result.terms:
                flagged_terms.append(term.term)
        
        if screen_result.pii and (screen_result.pii.email or screen_result.pii.phone or screen_result.pii.ipa or screen_result.pii.ssn):
            is_safe = False
            if screen_result.pii.email:
                flagged_terms.extend([e.text for e in screen_result.pii.email])
            if screen_result.pii.phone:
                flagged_terms.extend([p.text for p in screen_result.pii.phone])
            if screen_result.pii.ipa:
                flagged_terms.extend([ip.text for ip in screen_result.pii.ipa])

        return ModerationResult(
            original_text=text_to_check,
            is_safe=is_safe,
            flagged_terms=list(set(flagged_terms))
        )
    except Exception as e:
        raise RuntimeError(f"Error checking text safety with Azure Content Moderator: {e}")