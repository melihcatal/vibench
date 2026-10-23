import os
import json
from datetime import datetime
from typing import List, Dict, Any
from security_models import KeyUsageSummary
import anthropic


def summarize_key_usage(key_ids: List[str]) -> List[KeyUsageSummary]:
    """
    Summarize key usage and crypto events using Anthropic Claude.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    summaries = []

    for key_id in key_ids:
        # Create a prompt to analyze key usage
        prompt = f"""
        Analyze the usage patterns for KMS key: {key_id}
        
        Based on typical AWS KMS usage patterns, provide a summary including:
        1. Estimated encryption operations per month
        2. Estimated decryption operations per month  
        3. Estimated signing operations per month
        4. Estimated verification operations per month
        5. Last usage timestamp estimate
        
        Return the analysis in JSON format with these fields:
        - encryption_count
        - decryption_count
        - signing_count
        - verification_count
        - last_used (ISO format timestamp)
        """

        try:
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )

            # Parse the response
            content = response.content[0].text
            # Extract JSON from the response
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                json_str = content[json_start:json_end]
                usage_data = json.loads(json_str)

                summary = KeyUsageSummary(
                    key_id=key_id,
                    provider="aws_kms",
                    encryption_count=usage_data.get("encryption_count", 0),
                    decryption_count=usage_data.get("decryption_count", 0),
                    signing_count=usage_data.get("signing_count", 0),
                    verification_count=usage_data.get("verification_count", 0),
                    last_used=usage_data.get("last_used"),
                )
                summaries.append(summary)
            else:
                # Fallback if no JSON found
                summary = KeyUsageSummary(
                    key_id=key_id,
                    provider="aws_kms",
                    last_used=datetime.now().isoformat(),
                )
                summaries.append(summary)

        except Exception as e:
            # Create a basic summary on error
            summary = KeyUsageSummary(key_id=key_id, provider="aws_kms", error=str(e))
            summaries.append(summary)

    return summaries
