import os
import json
import google.generativeai as genai
from typing import Dict, Any


def summarize_message_payload(payload: Dict[str, Any], max_length: int = 200) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY environment variable must be set for Google Gemini API"
        )

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    payload_text = json.dumps(payload, indent=2)

    prompt = f"""Please summarize the following JSON payload in a concise way suitable for logging and monitoring.
Focus on the key information and actions. Keep the summary under {max_length} characters.

Payload:
{payload_text}

Summary:"""

    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()

        if len(summary) > max_length:
            summary = summary[: max_length - 3] + "..."

        print(
            f"Generated summary using Google Gemini API (gemini-1.5-flash model): {summary[:50]}..."
        )
        return summary

    except Exception as e:
        print(f"Failed to generate summary with Google Gemini API: {e}")
        fallback = f"Event with {len(payload)} fields"
        if "action" in payload:
            fallback = (
                f"{payload.get('action', 'event')} by {payload.get('user_id', 'user')}"
            )
        return fallback[:max_length]


def summarize_processing_results(results: list[Dict[str, Any]]) -> Dict[str, Any]:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY environment variable must be set for Google Gemini API"
        )

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    results_text = json.dumps(results, indent=2)

    prompt = f"""Analyze these message processing results and provide a brief summary including:
1. Overall success rate
2. Common patterns or issues
3. Any notable trends

Processing Results:
{results_text}

Summary:"""

    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()

        success_count = sum(1 for r in results if r.get("success", False))
        total_count = len(results)
        success_rate = (success_count / total_count * 100) if total_count > 0 else 0

        return {
            "summary": summary,
            "success_rate": f"{success_rate:.1f}%",
            "total_messages": total_count,
            "successful": success_count,
            "failed": total_count - success_count,
            "model_used": "gemini-1.5-flash",
            "provider": "Google Gemini API",
        }

    except Exception as e:
        print(f"Failed to generate processing summary with Google Gemini API: {e}")

        success_count = sum(1 for r in results if r.get("success", False))
        total_count = len(results)

        return {
            "summary": f"Processed {total_count} messages with {success_count} successes",
            "success_rate": f"{(success_count / total_count * 100):.1f}%"
            if total_count > 0
            else "0%",
            "total_messages": total_count,
            "successful": success_count,
            "failed": total_count - success_count,
            "model_used": "fallback",
            "provider": "Google Gemini API",
        }


if __name__ == "__main__":
    sample_payload = {
        "user_id": "user_12345",
        "action": "purchase",
        "items": [
            {"id": "item_001", "name": "Laptop", "price": 999.99, "quantity": 1},
            {"id": "item_002", "name": "Mouse", "price": 29.99, "quantity": 2},
        ],
        "total_amount": 1059.97,
        "payment_method": "credit_card",
        "shipping_address": "123 Main St, City, Country",
    }

    try:
        summary = summarize_message_payload(sample_payload)
        print(f"Payload summary: {summary}")

        sample_results = [
            {
                "message_id": "msg_001",
                "success": True,
                "processing_time_ms": 150,
                "event_type": "purchase",
            },
            {
                "message_id": "msg_002",
                "success": True,
                "processing_time_ms": 120,
                "event_type": "login",
            },
            {
                "message_id": "msg_003",
                "success": False,
                "error": "validation_failed",
                "event_type": "purchase",
            },
            {
                "message_id": "msg_004",
                "success": True,
                "processing_time_ms": 180,
                "event_type": "logout",
            },
        ]

        processing_summary = summarize_processing_results(sample_results)
        print(f"\nProcessing summary: {json.dumps(processing_summary, indent=2)}")

    except Exception as e:
        print(f"Error: {e}")
