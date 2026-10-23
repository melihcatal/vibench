import os
import json
from typing import Dict, Any, List, Optional
from openai import OpenAI


class ClaimsModerator:
    def __init__(self):
        self.openai_client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        )

    def moderate_claim(
        self, claim_text: str, claim_type: str = "note"
    ) -> Dict[str, Any]:
        try:
            response = self.openai_client.moderations.create(
                model="text-moderation-latest", input=claim_text
            )

            moderation_result = response.results[0]

            categories = moderation_result.categories
            category_scores = moderation_result.category_scores

            flagged = moderation_result.flagged

            moderation_details = {
                "flagged": flagged,
                "categories": {
                    category: {
                        "flagged": getattr(categories, category, False),
                        "score": getattr(category_scores, category, 0.0),
                    }
                    for category in [
                        "sexual",
                        "hate",
                        "harassment",
                        "self_harm",
                        "sexual_minors",
                        "hate_threatening",
                        "violence",
                        "violence_graphic",
                    ]
                },
            }

            if flagged:
                flagged_categories = [
                    category
                    for category, details in moderation_details["categories"].items()
                    if details["flagged"]
                ]

                return {
                    "approved": False,
                    "reason": f"Content flagged for: {', '.join(flagged_categories)}",
                    "moderation_details": moderation_details,
                    "suggestion": "Please revise the content to remove inappropriate language.",
                }
            else:
                return {
                    "approved": True,
                    "moderation_details": moderation_details,
                    "suggestion": "Content is appropriate.",
                }

        except Exception as e:
            return {
                "approved": False,
                "reason": f"Moderation check failed: {str(e)}",
                "error": True,
            }

    def moderate_user_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        moderation_results = {}

        text_fields_to_check = [
            ("name", profile_data.get("name")),
            ("bio", profile_data.get("bio")),
            ("notes", profile_data.get("notes")),
            ("company", profile_data.get("company")),
            ("location", profile_data.get("location")),
        ]

        for field_name, field_value in text_fields_to_check:
            if field_value and isinstance(field_value, str) and field_value.strip():
                result = self.moderate_claim(field_value, field_name)
                moderation_results[field_name] = result

        all_approved = all(
            result.get("approved", False)
            for result in moderation_results.values()
            if not result.get("error", False)
        )

        flagged_fields = [
            field_name
            for field_name, result in moderation_results.items()
            if not result.get("approved", False) and not result.get("error", False)
        ]

        return {
            "overall_approved": all_approved,
            "moderation_results": moderation_results,
            "flagged_fields": flagged_fields,
            "profile_approved": all_approved,
        }

    def sanitize_claim(self, claim_text: str) -> Dict[str, Any]:
        try:
            prompt = f"""Please sanitize the following user-provided text by removing any inappropriate content while preserving the original meaning as much as possible. 
            If the text is already appropriate, return it as-is.
            
            Text to sanitize: "{claim_text}"
            
            Return only the sanitized text."""

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a content sanitization assistant. Remove inappropriate content while preserving meaning.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=200,
                temperature=0.1,
            )

            sanitized_text = response.choices[0].message.content.strip()

            moderation_check = self.moderate_claim(sanitized_text)

            return {
                "original": claim_text,
                "sanitized": sanitized_text,
                "moderation_check": moderation_check,
                "success": True,
            }

        except Exception as e:
            return {
                "original": claim_text,
                "sanitized": claim_text,
                "error": str(e),
                "success": False,
            }

    def batch_moderate_claims(self, claims: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = []
        approved_count = 0
        rejected_count = 0

        for claim in claims:
            claim_text = claim.get("text", "")
            claim_id = claim.get("id", "")
            claim_type = claim.get("type", "note")

            if claim_text:
                moderation_result = self.moderate_claim(claim_text, claim_type)
                result = {
                    "id": claim_id,
                    "type": claim_type,
                    "text_preview": claim_text[:50] + "..."
                    if len(claim_text) > 50
                    else claim_text,
                    **moderation_result,
                }

                if moderation_result.get("approved", False):
                    approved_count += 1
                else:
                    rejected_count += 1

                results.append(result)

        return {
            "total_claims": len(results),
            "approved": approved_count,
            "rejected": rejected_count,
            "approval_rate": (approved_count / len(results) * 100) if results else 0,
            "results": results,
        }
