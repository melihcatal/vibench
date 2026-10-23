import json
from typing import Dict, List, Any, Optional
from document_models import ExpenseRecord


def moderate_vendor_text(
    vendor_name: str, notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Moderate vendor notes or memo fields using Google Perspective API for content safety.
    """
    from googleapiclient import discovery
    from googleapiclient.errors import HttpError

    api_key = os.getenv("GOOGLE_PERSPECTIVE_API_KEY")

    if not api_key:
        return {
            "moderated": False,
            "error": "Google Perspective API key not configured",
            "safety_scores": {},
            "is_safe": True,
        }

    # Combine vendor name and notes for moderation
    text_to_analyze = vendor_name
    if notes:
        text_to_analyze += f". Notes: {notes}"

    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    analyze_request = {
        "comment": {"text": text_to_analyze},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    try:
        response = client.comments().analyze(body=analyze_request).execute()

        # Extract scores
        attribute_scores = response.get("attributeScores", {})

        safety_scores = {}
        for attribute, data in attribute_scores.items():
            safety_scores[attribute.lower()] = {
                "score": data.get("summaryScore", {}).get("value", 0),
                "threshold_exceeded": data.get("summaryScore", {}).get("value", 0)
                > 0.7,
            }

        # Determine overall safety
        high_risk_attributes = [
            "toxicity",
            "severe_toxicity",
            "identity_attack",
            "threat",
        ]
        is_safe = True

        for attr in high_risk_attributes:
            if attr in safety_scores and safety_scores[attr]["threshold_exceeded"]:
                is_safe = False
                break

        moderation_result = {
            "moderated": True,
            "text_analyzed": text_to_analyze,
            "safety_scores": safety_scores,
            "is_safe": is_safe,
            "high_risk_attributes": [
                attr
                for attr, data in safety_scores.items()
                if data["threshold_exceeded"] and attr in high_risk_attributes
            ],
            "moderation_timestamp": datetime.utcnow().isoformat(),
            "api_used": "google_perspective",
        }

        return moderation_result

    except HttpError as e:
        return {
            "moderated": False,
            "error": f"Google Perspective API error: {str(e)}",
            "safety_scores": {},
            "is_safe": True,
            "moderation_timestamp": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {
            "moderated": False,
            "error": f"Unexpected error: {str(e)}",
            "safety_scores": {},
            "is_safe": True,
            "moderation_timestamp": datetime.utcnow().isoformat(),
        }


def check_vendor_against_blocklist(vendor_name: str) -> Dict[str, Any]:
    """
    Check vendor name against a blocklist using a simple pattern matching approach.
    In a real scenario, this would integrate with a vendor risk management service.
    """
    # Example blocklist patterns (in reality, this would come from a managed service)
    blocklist_patterns = [
        r"(?i)test.*vendor",
        r"(?i)dummy.*supplier",
        r"(?i)example.*company",
        r"(?i)fraud.*enterprise",
        r"(?i)suspicious.*corp",
    ]

    import re

    matches = []

    for pattern in blocklist_patterns:
        if re.search(pattern, vendor_name):
            matches.append(pattern)

    return {
        "checked": True,
        "vendor_name": vendor_name,
        "blocklist_matches": matches,
        "is_blocked": len(matches) > 0,
        "risk_level": "high" if len(matches) > 0 else "low",
        "check_timestamp": datetime.utcnow().isoformat(),
    }


def moderate_expense_notes(expense_record: ExpenseRecord) -> Dict[str, Any]:
    """
    Moderate all text fields in an expense record.
    """
    moderation_results = {}

    # Moderate vendor name
    vendor_moderation = moderate_vendor_text(expense_record.vendor_name)
    moderation_results["vendor_moderation"] = vendor_moderation

    # Check against blocklist
    blocklist_check = check_vendor_against_blocklist(expense_record.vendor_name)
    moderation_results["blocklist_check"] = blocklist_check

    # Moderate line item descriptions if any suspicious patterns
    item_moderations = []
    for item in expense_record.line_items:
        description = item.get("description", "")
        if description:
            # Simple keyword check for suspicious descriptions
            suspicious_keywords = ["test", "sample", "dummy", "placeholder"]
            has_suspicious = any(
                keyword in description.lower() for keyword in suspicious_keywords
            )

            item_moderations.append(
                {
                    "description": description,
                    "has_suspicious_keywords": has_suspicious,
                    "suspicious_keywords_found": [
                        kw for kw in suspicious_keywords if kw in description.lower()
                    ],
                }
            )

    moderation_results["item_moderations"] = item_moderations

    # Overall safety assessment
    overall_safe = (
        vendor_moderation.get("is_safe", True)
        and not blocklist_check.get("is_blocked", False)
        and not any(
            item.get("has_suspicious_keywords", False) for item in item_moderations
        )
    )

    moderation_results["overall_assessment"] = {
        "is_safe": overall_safe,
        "risk_factors": [
            "vendor_moderation_failed"
            if not vendor_moderation.get("is_safe", True)
            else None,
            "vendor_blocklisted" if blocklist_check.get("is_blocked", False) else None,
            "suspicious_item_descriptions"
            if any(
                item.get("has_suspicious_keywords", False) for item in item_moderations
            )
            else None,
        ],
        "assessment_timestamp": datetime.utcnow().isoformat(),
    }

    # Clean up None values from risk factors
    moderation_results["overall_assessment"]["risk_factors"] = [
        factor
        for factor in moderation_results["overall_assessment"]["risk_factors"]
        if factor is not None
    ]

    return moderation_results


if __name__ == "__main__":
    # Example usage
    from document_models import ExpenseRecord

    sample_record = ExpenseRecord(
        vendor_name="Test Vendor Corp",
        transaction_date="2024-01-15",
        total_amount=1000.00,
        currency="USD",
        line_items=[
            {
                "description": "Test equipment",
                "quantity": 1,
                "unit_price": 1000,
                "amount": 1000,
            }
        ],
        metadata={"notes": "This is a test invoice for demonstration purposes."},
    )

    moderation_result = moderate_expense_notes(sample_record)
    print(json.dumps(moderation_result, indent=2))
