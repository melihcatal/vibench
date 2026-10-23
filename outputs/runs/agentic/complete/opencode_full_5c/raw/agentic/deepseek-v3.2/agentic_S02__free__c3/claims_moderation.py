import os
import json
from typing import Dict, Any, List, Optional
import openai


class ClaimsModerator:
    def __init__(self):
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = os.environ.get("OPENAI_MODERATION_MODEL", "gpt-4o-mini")

    def moderate_free_text(
        self, text: str, claim_type: str = "user_note"
    ) -> Dict[str, Any]:
        if not text or not text.strip():
            return {
                "approved": True,
                "reason": "Empty text",
                "moderation_categories": {},
                "suggested_replacement": None,
            }

        try:
            response = openai.Moderation.create(
                input=text, model="text-moderation-latest"
            )

            moderation_result = response.results[0]

            categories = moderation_result.categories
            category_scores = moderation_result.category_scores

            flagged_categories = {
                category: {
                    "flagged": getattr(categories, category),
                    "score": getattr(category_scores, category),
                }
                for category in dir(categories)
                if not category.startswith("_")
                and not callable(getattr(categories, category))
            }

            is_flagged = moderation_result.flagged

            if is_flagged:
                suggested_replacement = self._generate_safe_replacement(
                    text, claim_type
                )
            else:
                suggested_replacement = None

            return {
                "approved": not is_flagged,
                "flagged": is_flagged,
                "moderation_categories": flagged_categories,
                "suggested_replacement": suggested_replacement,
                "original_text": text,
                "claim_type": claim_type,
            }

        except Exception as e:
            return {
                "approved": False,
                "error": str(e),
                "original_text": text,
                "claim_type": claim_type,
            }

    def _generate_safe_replacement(self, text: str, claim_type: str) -> Optional[str]:
        try:
            prompt = f"""
            The following user-provided text from a {claim_type} field has been flagged for moderation.
            Please provide a safe, appropriate alternative that preserves the original intent while removing any problematic content.
            
            Original text: {text}
            
            Provide only the safe replacement text, nothing else.
            """

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that rewrites text to be safe and appropriate while preserving meaning.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=200,
                temperature=0.3,
            )

            replacement = response.choices[0].message.content.strip()

            return replacement if replacement and replacement != text else None

        except Exception:
            return None

    def batch_moderate_claims(self, claims: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = {
            "total_claims": len(claims),
            "approved_claims": 0,
            "flagged_claims": 0,
            "claim_results": [],
            "summary_by_type": {},
        }

        for claim in claims:
            text = claim.get("text", "")
            claim_type = claim.get("type", "unknown")
            claim_id = claim.get("id", "")

            moderation_result = self.moderate_free_text(text, claim_type)

            claim_result = {
                "id": claim_id,
                "type": claim_type,
                "original_text": text,
                **moderation_result,
            }

            results["claim_results"].append(claim_result)

            if moderation_result.get("approved", False):
                results["approved_claims"] += 1
            else:
                results["flagged_claims"] += 1

            if claim_type not in results["summary_by_type"]:
                results["summary_by_type"][claim_type] = {
                    "total": 0,
                    "approved": 0,
                    "flagged": 0,
                }

            results["summary_by_type"][claim_type]["total"] += 1
            if moderation_result.get("approved", False):
                results["summary_by_type"][claim_type]["approved"] += 1
            else:
                results["summary_by_type"][claim_type]["flagged"] += 1

        return results

    def check_profile_claims(self, profile_claims: Dict[str, Any]) -> Dict[str, Any]:
        text_fields_to_check = [
            ("name", profile_claims.get("name")),
            ("given_name", profile_claims.get("given_name")),
            ("family_name", profile_claims.get("family_name")),
            ("locale", profile_claims.get("locale")),
        ]

        moderation_results = {}
        flagged_fields = []

        for field_name, field_value in text_fields_to_check:
            if field_value and isinstance(field_value, str):
                result = self.moderate_free_text(field_value, f"profile_{field_name}")
                moderation_results[field_name] = result

                if not result.get("approved", False):
                    flagged_fields.append(field_name)

        overall_approved = len(flagged_fields) == 0

        return {
            "profile_id": profile_claims.get("sub"),
            "overall_approved": overall_approved,
            "flagged_fields": flagged_fields,
            "field_results": moderation_results,
            "provider": profile_claims.get("provider", "unknown"),
        }
