import os
from typing import List, Dict, Any
from openai import OpenAI
import json


def summarize_message_processing(results: List[Dict[str, Any]]) -> str:
    """Summarize message processing results using OpenAI GPT."""
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=openai_api_key)

    summary_data = {
        "total_messages": len(results),
        "successful": sum(1 for r in results if r.get("status") == "success"),
        "failed": sum(1 for r in results if r.get("status") == "failed"),
        "processing_time_avg": sum(r.get("processing_time", 0) for r in results)
        / max(len(results), 1),
        "message_types": {},
    }

    for result in results:
        msg_type = result.get("message_type", "unknown")
        summary_data["message_types"][msg_type] = (
            summary_data["message_types"].get(msg_type, 0) + 1
        )

    prompt = f"""
    Analyze this message processing batch and provide a concise summary:
    
    {json.dumps(summary_data, indent=2)}
    
    Provide a 2-3 sentence summary highlighting key metrics and any issues.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes message processing results.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    sample_results = [
        {"status": "success", "message_type": "order_created", "processing_time": 0.5},
        {
            "status": "success",
            "message_type": "payment_processed",
            "processing_time": 0.7,
        },
        {
            "status": "failed",
            "message_type": "inventory_check",
            "processing_time": 2.1,
            "error": "Timeout",
        },
        {"status": "success", "message_type": "order_created", "processing_time": 0.6},
        {
            "status": "success",
            "message_type": "customer_update",
            "processing_time": 0.4,
        },
    ]

    try:
        summary = summarize_message_processing(sample_results)
        print("Message Processing Summary:")
        print(summary)
    except Exception as e:
        print(f"Failed to generate summary: {e}")
