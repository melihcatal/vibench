import os
from datetime import datetime
from security_client import get_openai_client
from security_models import KeyUsageSummary


def summarize_key_usage(key_id: str, operation_logs: list) -> KeyUsageSummary:
    """Summarize key usage and crypto events using OpenAI."""
    client = get_openai_client()

    try:
        # Create a summary of operations
        operation_count = len(operation_logs)

        # Find the most recent operation
        last_used = None
        if operation_logs:
            timestamps = [
                op.get("timestamp") for op in operation_logs if op.get("timestamp")
            ]
            if timestamps:
                last_used = max(timestamps)

        # Use OpenAI to generate a natural language summary
        operations_text = "\n".join(
            [
                f"- {op.get('operation', 'unknown')} at {op.get('timestamp', 'unknown')}"
                for op in operation_logs[:10]
            ]
        )  # Limit to 10 for context

        prompt = f"""
        Summarize the key usage for key ID: {key_id}
        
        Total operations: {operation_count}
        Recent operations:
        {operations_text}
        
        Provide a concise summary of the key usage pattern.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a security analyst summarizing key usage patterns.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
        )

        summary_text = response.choices[0].message.content

        return KeyUsageSummary(
            key_id=key_id,
            operation_count=operation_count,
            last_used=last_used,
            provider="openai",
        )
    except Exception as e:
        # Fallback to basic summary if OpenAI fails
        return KeyUsageSummary(
            key_id=key_id,
            operation_count=len(operation_logs),
            last_used=None,
            provider="openai",
            error=str(e) if str(e) else None,
        )
