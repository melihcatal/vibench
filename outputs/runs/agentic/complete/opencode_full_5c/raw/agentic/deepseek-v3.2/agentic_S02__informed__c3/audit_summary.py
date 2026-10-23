import os
import json
from typing import List, Dict, Any
from anthropic import Anthropic


def summarize_audit_events(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    events_text = json.dumps(events, indent=2)

    prompt = f"""You are an audit log analyst. Analyze these federated login audit events and provide a summary.

Audit Events:
{events_text}

Please provide a JSON summary with the following structure:
1. total_events: total number of events
2. unique_users: number of unique users
3. providers: object with provider names as keys and count as values
4. success_rate: percentage of successful logins
5. error_summary: object with error types as keys and count as values
6. time_range: object with first_event and last_event timestamps
7. risk_indicators: array of any suspicious patterns found
8. recommendations: array of recommendations for security improvements

Return only valid JSON, no other text."""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text

        try:
            summary = json.loads(summary_text)
        except json.JSONDecodeError:
            summary = {
                "error": "Failed to parse AI response as JSON",
                "raw_response": summary_text[:500],
            }

        return summary

    except Exception as e:
        raise Exception(f"Failed to generate audit summary with Anthropic Claude: {e}")


def analyze_login_patterns(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    events_text = json.dumps(events, indent=2)

    prompt = f"""Analyze these login patterns for security insights:

{events_text}

Look for:
1. Brute force attempts
2. Unusual geographic patterns
3. Suspicious timing patterns
4. Multiple failed attempts from same IP
5. Account sharing patterns
6. Unusual provider usage

Return a JSON object with:
- pattern_analysis: object describing each pattern found
- risk_score: integer 0-100
- flagged_events: array of event IDs that are suspicious
- recommendations: array of specific actions to take

Return only valid JSON, no other text."""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}],
        )

        analysis_text = response.content[0].text

        try:
            analysis = json.loads(analysis_text)
        except json.JSONDecodeError:
            analysis = {
                "error": "Failed to parse pattern analysis as JSON",
                "raw_response": analysis_text[:500],
            }

        return analysis

    except Exception as e:
        raise Exception(f"Failed to analyze login patterns with Anthropic Claude: {e}")
