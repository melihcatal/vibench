import os
import openai

def metric_summary(metric_data: str, summary_length: str = "concise") -> str:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    prompt = f"Summarize the following metric data. Focus on trends, anomalies, and key observations. Make the summary {summary_length}.\n\nMetric Data: {metric_data}\n\nSummary:"

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Using a recent and capable model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes metric data."}, 
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to summarize metric data using OpenAI: {e}")

if __name__ == "__main__":
    # Example Usage
    sample_metric_data = """
    Timestamp,Value
    2023-10-26T10:00:00Z,10.5
    2023-10-26T10:05:00Z,11.2
    2023-10-26T10:10:00Z,10.8
    2023-10-26T10:15:00Z,55.1  # Anomaly
    2023-10-26T10:20:00Z,12.3
    2023-10-26T10:25:00Z,12.0
    """
    try:
        summary = metric_summary(sample_metric_data, summary_length="brief")
        print("Metric Summary:")
        print(summary)
    except Exception as e:
        print(f"Error: {e}")
