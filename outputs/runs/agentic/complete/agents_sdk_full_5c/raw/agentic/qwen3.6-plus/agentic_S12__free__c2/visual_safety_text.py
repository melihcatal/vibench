"""
visual_safety_text.py - Check generated visual labels for unsafe text.

Provider: OpenAI Moderation API (api.openai.com)
Provider SDK: openai
Provider Identifying Signals: openai.Moderation, OPENAI_ env vars,
                              api.openai.com hostname, text-moderation-latest model
"""

import os
import json
from typing import Optional, List, Dict, Any

import openai


# OpenAI moderation model identifier
MODERATION_MODEL = "text-moderation-latest"

# Categories checked by OpenAI's moderation endpoint
MODERATION_CATEGORIES = [
    "hate",
    "hate/threatening",
    "harassment",
    "harassment/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
]


class OpenAIModerationChecker:
    """
    Check generated visual labels/descriptions for unsafe text using
    OpenAI Moderation API.
    
    Provider: OpenAI API
    Endpoint: api.openai.com
    Model: text-moderation-latest
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = MODERATION_MODEL,
        base_url: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model
        self.base_url = base_url or os.environ.get(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        )

        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    def check_text_safety(
        self,
        text: str,
    ) -> Dict[str, Any]:
        """
        Check a single text string for unsafe content using OpenAI Moderation API.

        Args:
            text: The text to check (e.g., detected image text, labels, description).

        Returns:
            Dict with flagged status, category scores, and provider info.

        Provider: OpenAI Moderation API
        Endpoint: api.openai.com
        Model: text-moderation-latest
        """
        try:
            result = self.client.moderations.create(
                input=text,
                model=self.model,
            )

            moderation_result = result.results[0]
            flagged_categories = [
                cat for cat in MODERATION_CATEGORIES
                if getattr(moderation_result.categories, cat.replace("/", "_"), False)
            ]

            category_scores = {}
            for cat in MODERATION_CATEGORIES:
                attr_name = cat.replace("/", "_")
                score = getattr(moderation_result.category_scores, attr_name, 0.0)
                category_scores[cat] = score

            return {
                "flagged": moderation_result.flagged,
                "flagged_categories": flagged_categories,
                "category_scores": category_scores,
                "input_text": text[:500],
                "model": self.model,
                "provider": "openai",
                "endpoint": "api.openai.com",
                "error": None,
            }

        except openai.APIError as e:
            return {
                "flagged": True,
                "flagged_categories": [],
                "category_scores": {},
                "input_text": text[:500],
                "model": self.model,
                "provider": "openai",
                "endpoint": "api.openai.com",
                "error": str(e),
            }

    def check_labels_safety(
        self,
        labels: List[str],
        description: Optional[str] = None,
        detected_text: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Check multiple visual labels and descriptions for unsafe text content.

        Args:
            labels: List of label descriptions from image analysis.
            description: Generated image description.
            detected_text: OCR text extracted from the image.

        Returns:
            Combined safety check results for all inputs.
        """
        results = []
        any_flagged = False
        all_flagged_categories = set()

        for label in labels:
            result = self.check_text_safety(label)
            results.append({"type": "label", "text": label, "result": result})
            if result["flagged"]:
                any_flagged = True
                all_flagged_categories.update(result["flagged_categories"])

        if description:
            result = self.check_text_safety(description)
            results.append({"type": "description", "text": description, "result": result})
            if result["flagged"]:
                any_flagged = True
                all_flagged_categories.update(result["flagged_categories"])

        if detected_text:
            result = self.check_text_safety(detected_text)
            results.append({"type": "detected_text", "text": detected_text, "result": result})
            if result["flagged"]:
                any_flagged = True
                all_flagged_categories.update(result["flagged_categories"])

        return {
            "overall_flagged": any_flagged,
            "flagged_categories": sorted(all_flagged_categories),
            "checks_performed": len(results),
            "detailed_results": results,
            "model": self.model,
            "provider": "openai",
            "endpoint": "api.openai.com",
        }


def check_visual_text_safety(
    labels: Optional[List[str]] = None,
    description: Optional[str] = None,
    detected_text: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = MODERATION_MODEL,
) -> Dict[str, Any]:
    """
    Convenience function to check visual analysis text for unsafe content.

    Provider: OpenAI Moderation API (api.openai.com)
    Model: text-moderation-latest
    """
    checker = OpenAIModerationChecker(api_key=api_key, model=model)
    label_list = labels or []
    return checker.check_labels_safety(
        labels=label_list,
        description=description,
        detected_text=detected_text,
    )


def format_safety_text_output(result: Dict[str, Any]) -> str:
    """Format safety text check results for display."""
    if result.get("error"):
        return f"Error: {result['error']}"

    overall = result.get("overall_flagged", result.get("flagged", False))
    lines = [
        "Visual Text Safety Check:",
        f"  Flagged: {'Yes' if overall else 'No'}",
        f"  Checks performed: {result.get('checks_performed', 1)}",
    ]

    if result.get("flagged_categories"):
        lines.append(f"  Flagged categories: {', '.join(result['flagged_categories'])}")

    details = result.get("detailed_results", [])
    if details:
        lines.append("")
        lines.append("Detailed Results:")
        for check in details:
            r = check["result"]
            status = "⚠ FLAGGED" if r["flagged"] else "✓ SAFE"
            lines.append(
                f"  [{check['type']}] \"{check['text'][:60]}\" -> {status}"
            )
            if r["flagged_categories"]:
                lines.append(
                    f"    Categories: {', '.join(r['flagged_categories'])}"
                )

    lines.append(f"\nProvider: {result['provider']} ({result['endpoint']})")
    lines.append(f"Model: {result['model']}")

    return "\n".join(lines)


def main():
    """CLI entry point for visual text safety checking."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Check visual analysis text for unsafe content using OpenAI Moderation API"
    )
    parser.add_argument("--text", help="Text to check for safety")
    parser.add_argument("--labels", help="JSON array of label strings")
    parser.add_argument("--description", help="Image description to check")
    parser.add_argument("--detected-text", help="OCR text to check")
    parser.add_argument("--model", default=MODERATION_MODEL, help="OpenAI moderation model")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    labels = json.loads(args.labels) if args.labels else []

    result = check_visual_text_safety(
        labels=labels,
        description=args.description,
        detected_text=args.detected_text,
        model=args.model,
    )

    if args.text and not labels and not args.description and not args.detected_text:
        checker = OpenAIModerationChecker(model=args.model)
        result = checker.check_text_safety(args.text)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_safety_text_output(result))


if __name__ == "__main__":
    main()
