import os
import json
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from datetime import datetime


def summarize_key_usage(
    usage_data: List[Dict[str, Any]], model_name: str = "gemini-1.5-flash"
) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    genai.configure(api_key=api_key)

    prompt = f"""
    Analyze the following key usage data and provide a concise summary:
    
    Key Usage Data:
    {json.dumps(usage_data, indent=2)}
    
    Please provide a summary that includes:
    1. Total number of operations
    2. Breakdown by operation type (encrypt, decrypt, sign, verify, etc.)
    3. Most frequently used keys
    4. Any patterns or anomalies in usage
    5. Security recommendations based on the usage patterns
    
    Format the response as a clear, structured summary.
    """

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini API call failed: {e}")


def analyze_encryption_patterns(
    encryption_events: List[Dict[str, Any]], model_name: str = "gemini-1.5-flash"
) -> Dict[str, Any]:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    genai.configure(api_key=api_key)

    prompt = f"""
    Analyze these encryption events for patterns and security insights:
    
    Encryption Events:
    {json.dumps(encryption_events, indent=2)}
    
    Provide analysis in JSON format with these keys:
    - "total_encryptions": number
    - "key_rotation_frequency": analysis text
    - "encryption_context_usage": analysis text  
    - "potential_risks": list of strings
    - "recommendations": list of strings
    """

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)

        try:
            analysis = json.loads(response.text)
        except json.JSONDecodeError:
            analysis = {"analysis_text": response.text}

        return analysis
    except Exception as e:
        raise RuntimeError(f"Gemini API analysis failed: {e}")


def generate_compliance_report(
    audit_logs: List[Dict[str, Any]], model_name: str = "gemini-1.5-flash"
) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    genai.configure(api_key=api_key)

    prompt = f"""
    Generate a compliance report based on these key management audit logs:
    
    Audit Logs:
    {json.dumps(audit_logs, indent=2)}
    
    Create a formal compliance report that includes:
    1. Executive Summary
    2. Key Usage Statistics
    3. Access Control Analysis
    4. Policy Compliance Assessment
    5. Findings and Recommendations
    6. Risk Assessment
    
    Format as a professional report with sections and bullet points where appropriate.
    """

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise RuntimeError(f"Gemini API report generation failed: {e}")


def detect_anomalies(
    usage_history: List[Dict[str, Any]], model_name: str = "gemini-1.5-flash"
) -> List[str]:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")

    genai.configure(api_key=api_key)

    prompt = f"""
    Analyze this key usage history for anomalies or suspicious patterns:
    
    Usage History:
    {json.dumps(usage_history, indent=2)}
    
    Identify any anomalies such as:
    - Unusual access patterns
    - Unexpected operation volumes
    - Irregular timing
    - Suspicious key usage
    
    Return a list of detected anomalies, one per line. If no anomalies found, return "No anomalies detected."
    """

    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        anomalies = [line.strip() for line in response.text.split("\n") if line.strip()]
        return anomalies
    except Exception as e:
        raise RuntimeError(f"Gemini API anomaly detection failed: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        try:
            with open(input_file, "r") as f:
                usage_data = json.load(f)

            summary = summarize_key_usage(usage_data)
            print("Key Usage Summary:")
            print(summary)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
