"""
[LATER-STEP] payload_safety.py - Check decrypted text payloads for unsafe content.

Provider: Azure AI Content Safety
SDK: requests (REST API)
Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
"""

from __future__ import annotations

import argparse
import logging
import os
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s")

AZURE_CONTENT_SAFETY_API_VERSION = "2024-02-15-preview"


def check_payload_safety(
    text: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    categories: Optional[List[str]] = None,
    output_type: str = "EightSeverityLevels",
) -> Dict[str, Any]:
    """
    Check a text payload for unsafe content using Azure AI Content Safety.

    Provider: Azure AI Content Safety
    REST API: POST {endpoint}/contentsafety/text:analyze
    Auth: AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY
    """
    azure_endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    azure_api_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

    if not azure_endpoint or not azure_api_key:
        raise ValueError(
            "Azure Content Safety endpoint and API key are required. "
            "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY env vars."
        )

    url = f"{azure_endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": azure_api_key,
    }

    default_categories = ["Hate", "SelfHarm", "Sexual", "Violence"]
    selected_categories = categories or default_categories

    payload = {
        "text": text,
        "categories": selected_categories,
        "outputType": output_type,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    result = response.json()
    logger.info(
        "Azure Content Safety analysis completed for text of length %d",
        len(text),
    )
    return result


def check_payload_safety_with_image(
    text: str,
    image_url: Optional[str] = None,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Check text and optionally an image for unsafe content using Azure AI Content Safety.

    Provider: Azure AI Content Safety
    """
    azure_endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT", "")
    azure_api_key = api_key or os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

    if not azure_endpoint or not azure_api_key:
        raise ValueError(
            "Azure Content Safety endpoint and API key are required."
        )

    url = f"{azure_endpoint}/contentsafety/text:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": azure_api_key,
    }

    payload: Dict[str, Any] = {
        "text": text,
        "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
        "outputType": "EightSeverityLevels",
    }

    if image_url:
        payload["image"] = {"url": image_url}
        # For image analysis, use the image endpoint
        image_url_endpoint = f"{azure_endpoint}/contentsafety/image:analyze?api-version={AZURE_CONTENT_SAFETY_API_VERSION}"
        image_headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": azure_api_key,
        }
        image_payload = {
            "image": {"url": image_url},
            "categories": ["Hate", "SelfHarm", "Sexual", "Violence"],
            "outputType": "EightSeverityLevels",
        }
        image_response = requests.post(
            image_url_endpoint, headers=image_headers, json=image_payload, timeout=30
        )
        image_response.raise_for_status()
        image_result = image_response.json()
    else:
        image_result = None

    text_response = requests.post(url, headers=headers, json=payload, timeout=30)
    text_response.raise_for_status()
    text_result = text_response.json()

    combined_result = {
        "text_analysis": text_result,
        "image_analysis": image_result,
    }

    logger.info(
        "Azure Content Safety analysis completed (text + image) for text length %d",
        len(text),
    )
    return combined_result


def summarize_safety_results(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and summarize the Azure AI Content Safety analysis results.
    Returns a structured summary with severity levels and recommendations.
    """
    text_analysis = analysis_result.get("text_analysis", analysis_result)
    categories_results = text_analysis.get("categoriesAnalysis", [])

    summary = {
        "overall_safe": True,
        "flags": [],
        "categories": {},
    }

    for category_result in categories_results:
        category = category_result.get("category", "Unknown")
        severity = category_result.get("severity", 0)

        summary["categories"][category] = severity

        if severity > 0:
            summary["overall_safe"] = False
            if severity >= 4:
                level = "HIGH"
            elif severity >= 2:
                level = "MEDIUM"
            else:
                level = "LOW"

            summary["flags"].append(
                {
                    "category": category,
                    "severity": severity,
                    "level": level,
                }
            )

    return summary


def check_decrypted_payload_safety(
    plaintext: str,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience function: check a decrypted plaintext payload for unsafe content.

    Provider: Azure AI Content Safety
    """
    result = check_payload_safety(
        text=plaintext,
        endpoint=endpoint,
        api_key=api_key,
    )
    summary = summarize_safety_results(result)
    summary["raw_result"] = result
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check decrypted text payload for unsafe content"
    )
    parser.add_argument(
        "--text",
        help="Text payload to analyze",
    )
    parser.add_argument(
        "--text-file",
        help="Path to file containing text payload",
    )
    parser.add_argument(
        "--endpoint",
        help="Azure Content Safety endpoint (or set AZURE_CONTENT_SAFETY_ENDPOINT)",
    )
    parser.add_argument(
        "--api-key",
        help="Azure Content Safety API key (or set AZURE_CONTENT_SAFETY_KEY)",
    )
    parser.add_argument(
        "--categories",
        nargs="*",
        default=["Hate", "SelfHarm", "Sexual", "Violence"],
        help="Categories to check",
    )
    parser.add_argument(
        "--output-file",
        help="Path to write analysis results",
    )
    args = parser.parse_args()

    if args.text_file:
        with open(args.text_file, "r") as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        parser.error("--text or --text-file is required")

    result = check_payload_safety(
        text=text,
        endpoint=args.endpoint,
        api_key=args.api_key,
        categories=args.categories,
    )

    summary = summarize_safety_results(result)

    if args.output_file:
        output = {
            "summary": summary,
            "raw_result": result,
        }
        import json
        with open(args.output_file, "w") as f:
            json.dump(output, f, indent=2, default=str)
        print(f"Analysis written to {args.output_file}")
    else:
        print(f"Overall Safe: {summary['overall_safe']}")
        for flag in summary.get("flags", []):
            print(f"  [{flag['level']}] {flag['category']}: severity {flag['severity']}")
        if not summary.get("flags"):
            print("  No safety flags detected.")


if __name__ == "__main__":
    main()
