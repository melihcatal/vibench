import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from openai import OpenAI
from query_error_logs import query_errors_with_insights
from observability_models import ErrorSummary


def summarize_incident(
    minutes_ago: int = 60, service: Optional[str] = None, use_ai: bool = True
) -> Dict[str, Any]:
    error_insights = query_errors_with_insights(
        minutes_ago=minutes_ago, service=service
    )

    if use_ai and error_insights["total_errors"] > 0:
        ai_summary = generate_ai_incident_summary(error_insights)
        error_insights["ai_summary"] = ai_summary

    error_summary = ErrorSummary(
        error_count=error_insights["total_errors"],
        unique_errors=error_insights.get("unique_error_types", 0),
        services_affected=error_insights.get("services_affected", []),
        time_range=error_insights.get("time_range", ""),
        most_common_error=error_insights.get("most_common_error", {}).get("pattern"),
    )

    severity = (
        "CRITICAL"
        if error_summary.error_count > 20
        else "HIGH"
        if error_summary.error_count > 10
        else "MEDIUM"
        if error_summary.error_count > 5
        else "LOW"
        if error_summary.error_count > 0
        else "NONE"
    )

    return {
        "summary": error_summary.to_dict(),
        "severity": severity,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "recommended_actions": generate_recommended_actions(error_summary),
        "raw_insights": error_insights,
    }


def generate_ai_incident_summary(error_insights: Dict[str, Any]) -> str:
    try:
        client = OpenAI(api_key="sk-dummy-key-for-example")

        error_context = json.dumps(error_insights, indent=2)

        prompt = f"""
        Analyze these application error logs and provide a concise incident summary:
        
        {error_context}
        
        Please provide:
        1. A brief summary of what's happening
        2. The likely root cause based on error patterns
        3. Recommended immediate actions
        4. Services/components most affected
        
        Keep the response under 300 words.
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced SRE analyzing application error logs.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.3,
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"AI summary unavailable: {str(e)}"


def generate_recommended_actions(error_summary: ErrorSummary) -> List[str]:
    actions = []

    if error_summary.error_count == 0:
        actions.append("No action needed - no errors detected")
        return actions

    if error_summary.error_count > 10:
        actions.append(
            "🚨 High error volume detected - consider scaling or restarting affected services"
        )

    if len(error_summary.services_affected) > 1:
        actions.append(
            "Multiple services affected - check inter-service communication and dependencies"
        )

    if error_summary.most_common_error:
        actions.append(
            f"Focus investigation on most common error: {error_summary.most_common_error[:100]}..."
        )

    if error_summary.error_count > 5:
        actions.append("Review recent deployments or configuration changes")
        actions.append("Check service health metrics and resource utilization")

    actions.append("Correlate errors with user reports or monitoring alerts")
    actions.append("Review error details for stack traces and exception patterns")

    return actions


def create_incident_timeline(
    start_time: datetime, end_time: datetime, interval_minutes: int = 5
) -> List[Dict[str, Any]]:
    timeline = []
    current_time = start_time

    while current_time < end_time:
        interval_end = current_time + timedelta(minutes=interval_minutes)

        errors = query_errors_with_insights(
            minutes_ago=int((datetime.now() - current_time).total_seconds() / 60),
            service=None,
        )

        timeline.append(
            {
                "time_window": f"{current_time.strftime('%H:%M')} - {interval_end.strftime('%H:%M')}",
                "error_count": errors.get("total_errors", 0),
                "peak_errors": errors.get("most_common_error", {}).get("count", 0),
                "services": errors.get("services_affected", []),
            }
        )

        current_time = interval_end

    return timeline


def generate_incident_report(
    incident_id: str, minutes_ago: int = 120, include_timeline: bool = True
) -> Dict[str, Any]:
    summary = summarize_incident(minutes_ago=minutes_ago, use_ai=True)

    report = {
        "incident_id": incident_id,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "time_range": f"Last {minutes_ago} minutes",
        "executive_summary": summary.get("ai_summary", "No AI summary available"),
        "key_metrics": {
            "total_errors": summary["summary"]["error_count"],
            "unique_error_types": summary["summary"]["unique_errors"],
            "services_affected": summary["summary"]["services_affected"],
            "severity_level": summary["severity"],
        },
        "recommended_actions": summary["recommended_actions"],
        "detailed_insights": summary["raw_insights"],
    }

    if include_timeline:
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=minutes_ago)
        report["timeline"] = create_incident_timeline(start_time, end_time)

    return report


if __name__ == "__main__":
    incident_summary = summarize_incident(minutes_ago=30)
    print(f"Incident summary: {json.dumps(incident_summary, indent=2)}")

    report = generate_incident_report(
        incident_id="INC-2023-001", minutes_ago=60, include_timeline=True
    )
    print(f"\nIncident report generated: {report['incident_id']}")
