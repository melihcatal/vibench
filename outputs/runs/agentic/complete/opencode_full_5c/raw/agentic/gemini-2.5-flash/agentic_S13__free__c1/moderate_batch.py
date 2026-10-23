import os
from typing import List
from safety_models import (
    TextModerationRequest,
    TextModerationResponse,
    ModerationCategory,
)
from safety_client import AzureSafetyClient


def moderate_batch_content(
    requests: List[TextModerationRequest],
) -> List[TextModerationResponse]:
    subscription_key = os.environ.get("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY")
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")

    if not subscription_key or not endpoint:
        raise ValueError(
            "Azure Content Moderator subscription key and endpoint must be set in environment variables."
        )

    client = AzureSafetyClient(subscription_key, endpoint)
    responses: List[TextModerationResponse] = []

    for req in requests:
        # Azure Content Moderator doesn't have a direct batch text moderation API in a single call
        # for multiple distinct texts. It processes one text at a time.
        # The TextModeration API is for a single piece of text.
        # This simulates a batch by iterating.
        moderation_result = client.content_moderator_client.text_moderation.screen_text(
            text_content=req.text_content,
            language="eng",  # Assuming English for this example
            autocorrect=True,
            pii=True,
        )

        is_safe = True
        decision_reason_list = []
        categories: List[ModerationCategory] = []

        if moderation_result.terms:
            is_safe = False
            decision_reason_list.append("Offensive terms detected.")
            # Azure Content Moderator returns boolean for terms and other detections, not scores.
            # For consistency with ModerationCategory, we'll assign a high score if detected.
            categories.append(ModerationCategory(category="OFFENSIVE_TERMS", score=1.0))

        if moderation_result.pii:
            if (
                moderation_result.pii.email
                or moderation_result.pii.phone
                or moderation_result.pii.address
                or moderation_result.pii.ip_address
            ):
                is_safe = False
                decision_reason_list.append("PII detected.")
                categories.append(
                    ModerationCategory(
                        category="PERSONAL_IDENTIFIABLE_INFORMATION", score=1.0
                    )
                )

        # For custom defined lists
        if moderation_result.classification:
            # Azure Classification returns scores for different categories
            # We map them to our ModerationCategory
            if (
                moderation_result.classification.review_recommended
            ):  # Overall recommendation
                is_safe = False
                decision_reason_list.append("Review recommended by classification.")

            if (
                moderation_result.classification.category1
                and moderation_result.classification.category1.score is not None
            ):
                categories.append(
                    ModerationCategory(
                        category="CATEGORY1_ADULT",
                        score=moderation_result.classification.category1.score,
                    )
                )
                if (
                    moderation_result.classification.category1.score > 0.5
                ):  # Example threshold
                    is_safe = False
                    decision_reason_list.append(
                        f"CATEGORY1_ADULT detected (score: {moderation_result.classification.category1.score:.2f})."
                    )

            if (
                moderation_result.classification.category2
                and moderation_result.classification.category2.score is not None
            ):
                categories.append(
                    ModerationCategory(
                        category="CATEGORY2_RACIAL_OFFENSIVE",
                        score=moderation_result.classification.category2.score,
                    )
                )
                if (
                    moderation_result.classification.category2.score > 0.5
                ):  # Example threshold
                    is_safe = False
                    decision_reason_list.append(
                        f"CATEGORY2_RACIAL_OFFENSIVE detected (score: {moderation_result.classification.category2.score:.2f})."
                    )

            if (
                moderation_result.classification.category3
                and moderation_result.classification.category3.score is not None
            ):
                categories.append(
                    ModerationCategory(
                        category="CATEGORY3_VIOLENCE_OFFENSIVE",
                        score=moderation_result.classification.category3.score,
                    )
                )
                if (
                    moderation_result.classification.category3.score > 0.5
                ):  # Example threshold
                    is_safe = False
                    decision_reason_list.append(
                        f"CATEGORY3_VIOLENCE_OFFENSIVE detected (score: {moderation_result.classification.category3.score:.2f})."
                    )

        responses.append(
            TextModerationResponse(
                categories=categories,
                is_safe=is_safe,
                decision_reason=" ".join(decision_reason_list).strip()
                or "Text is safe.",
            )
        )

    return responses
