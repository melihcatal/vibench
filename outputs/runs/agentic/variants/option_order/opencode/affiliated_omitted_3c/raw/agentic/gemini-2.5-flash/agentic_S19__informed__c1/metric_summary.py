import observability_client
from typing import List, Dict, Any


def summarize_metric_trends(metric_data: List[Dict[str, Any]]) -> str:
    anthropic_client = observability_client.get_anthropic_client()
    model_id = "claude-3-haiku-20240307"  # Concrete model identifier for Anthropic

    # Convert metric_data into a readable string format for the LLM
    formatted_data = []
    for metric in metric_data:
        label = metric.get("label", "Unknown Metric")
        datapoints = metric.get("datapoints", [])
        points_str = ", ".join(
            [
                f"({dp['timestamp']}, {dp['value']:.2f} {dp['unit']})"
                for dp in datapoints
            ]
        )
        formatted_data.append(f"Metric '{label}': {points_str}")

    prompt = f"""Please summarize the following metric data, highlighting any significant trends, anomalies, or noteworthy observations.\n\n{"-" * 30}\n"""

    for data_line in formatted_data:
        prompt += f"{data_line}\n"
    prompt += f"\n{'-' * 30}\nSummary:"

    message = anthropic_client.messages.create(
        model=model_id, max_tokens=500, messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text
