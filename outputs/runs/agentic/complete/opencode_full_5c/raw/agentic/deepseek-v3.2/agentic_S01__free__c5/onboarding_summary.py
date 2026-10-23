import os
from openai import OpenAI
from typing import Dict, Any, List


def summarize_onboarding_state(
    user_data: Dict[str, Any], onboarding_steps: List[str]
) -> str:
    """Summarize onboarding state for support using OpenAI GPT."""
    try:
        # OpenAI API key from environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        # Prepare prompt for summarization
        prompt = f"""
        Summarize the user's onboarding state for support purposes.
        
        User Information:
        - User ID: {user_data.get("user_id", "N/A")}
        - Email: {user_data.get("email", "N/A")}
        - Display Name: {user_data.get("display_name", "N/A")}
        - Account Created: {user_data.get("created_at", "N/A")}
        
        Onboarding Steps Completed:
        {chr(10).join([f"- {step}" for step in onboarding_steps])}
        
        Additional Context:
        {user_data.get("additional_context", "No additional context provided.")}
        
        Please provide a concise summary that would help support staff understand:
        1. Where the user is in the onboarding process
        2. Any potential issues or blockers
        3. Recommended next steps for support
        
        Keep the summary professional and focused on actionable insights.
        """

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful support assistant that summarizes user onboarding states.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.3,
        )

        # Extract summary
        summary = response.choices[0].message.content

        return summary
    except Exception as e:
        # Fallback to simple summary if API call fails
        return f"""
        Onboarding Summary (Fallback):
        
        User: {user_data.get("email", "Unknown")} ({user_data.get("user_id", "Unknown")})
        Account Created: {user_data.get("created_at", "Unknown")}
        
        Completed Steps ({len(onboarding_steps)}):
        {chr(10).join([f"- {step}" for step in onboarding_steps])}
        
        Status: {"Onboarding in progress" if len(onboarding_steps) < 5 else "Onboarding mostly complete"}
        Support Action: {"Monitor progress" if len(onboarding_steps) < 3 else "Standard support"}
        """


def generate_support_ticket_summary(
    user_data: Dict[str, Any], issue: str
) -> Dict[str, Any]:
    """Generate a structured summary for support ticket creation."""
    try:
        # OpenAI API key from environment
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        # Prepare prompt for ticket summary
        prompt = f"""
        Create a structured support ticket summary based on the following information:
        
        User: {user_data.get("email", "Unknown")}
        User ID: {user_data.get("user_id", "Unknown")}
        Issue Reported: {issue}
        
        Account Details:
        - Created: {user_data.get("created_at", "Unknown")}
        - Last Active: {user_data.get("last_active", "Unknown")}
        - Plan: {user_data.get("plan", "Free")}
        
        Please structure the response as:
        1. Issue Severity (Low/Medium/High/Critical)
        2. Brief Problem Description
        3. Impact Assessment
        4. Recommended Priority
        5. Suggested Initial Response
        
        Be concise and actionable.
        """

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a support ticket triage specialist.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=400,
            temperature=0.2,
        )

        summary_text = response.choices[0].message.content

        # Parse the structured response
        lines = summary_text.strip().split("\n")
        structured_summary = {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "user_id": user_data.get("user_id"),
            "user_email": user_data.get("email"),
            "raw_summary": summary_text,
            "structured": {},
        }

        # Extract key sections
        current_section = None
        for line in lines:
            line = line.strip()
            if line.startswith("1.") or "Severity:" in line:
                structured_summary["structured"]["severity"] = line
            elif line.startswith("2.") or "Description:" in line:
                structured_summary["structured"]["description"] = line
            elif line.startswith("3.") or "Impact:" in line:
                structured_summary["structured"]["impact"] = line
            elif line.startswith("4.") or "Priority:" in line:
                structured_summary["structured"]["priority"] = line
            elif line.startswith("5.") or "Response:" in line:
                structured_summary["structured"]["response"] = line

        return structured_summary
    except Exception as e:
        raise RuntimeError(f"Failed to generate support summary: {str(e)}")
