import os
import json
from openai import OpenAI
from observability_models import SummaryRequest


def metric_summary(request: SummaryRequest) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Summarize the following metric data. Identify any notable trends, anomalies, or patterns.
    The data is in JSON format.
    
    Metric Data:
    {json.dumps([ts.dict() for ts in request.metric_data], indent=2)}
    
    Provide a concise summary of your findings.
    """

    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful monitoring and observability assistant.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=250,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {e}"
