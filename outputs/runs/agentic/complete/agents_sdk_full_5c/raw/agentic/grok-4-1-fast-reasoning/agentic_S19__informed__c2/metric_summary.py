import os
import anthropic
from typing import List
from observability_models import DataPoint

def metric_summary(datapoints: List[DataPoint], metric_name: str) -> str:
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    recent_data = datapoints[-20:]
    data_str = '\\n'.join(f"{dp.timestamp.isoformat()}: {dp.value}" for dp in recent_data)
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        temperature=0.3,
        messages=[
            {
                "role": "user",
                "content": f"Summarize recent trends, averages, peaks, and potential anomalies for metric '{metric_name}'. Recent datapoints (timestamp: value):\\n{data_str}"
            }
        ]
    )
    return message.content[0].text
