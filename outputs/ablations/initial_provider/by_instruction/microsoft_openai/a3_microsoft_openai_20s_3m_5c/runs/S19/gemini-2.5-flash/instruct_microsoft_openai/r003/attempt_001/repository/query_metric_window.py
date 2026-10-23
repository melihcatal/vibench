import json
from datetime import datetime, timedelta
from observability_client import ObservabilityClient
from observability_models import MetricQueryRequest, MetricDatapoint, MetricQueryResult

def query_metric_window(request: MetricQueryRequest) -> MetricQueryResult:
    client = ObservabilityClient()

    # Using OpenAI to simulate metric data query and generation
    prompt = f"Generate synthetic metric data for '{request.metric_name}' from {request.start_time} to {request.end_time} with an interval of {request.interval}. Include 'timestamp' and 'value' for each datapoint. If dimensions are provided: {request.dimensions}, include them in the datapoints. Provide the output as a JSON array of objects, where each object has a 'timestamp' (ISO 8601 string) and 'value' (float). Generate at least 5 datapoints and at most 10. The values should be between 10 and 100." 

    response = client.openai_client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a common OpenAI model
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates synthetic metric data in JSON format."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    try:
        # Extract the JSON string from the response and parse it
        generated_text = response.choices[0].message.content.strip()
        # OpenAI often wraps JSON in ```json ... ```, so we need to extract it
        if generated_text.startswith("```json") and generated_text.endswith("```"):
            json_str = generated_text[7:-3].strip()
        else:
            json_str = generated_text
            
        datapoints_data = json.loads(json_str)

        datapoints = []
        for dp in datapoints_data:
            datapoints.append(MetricDatapoint(
                timestamp=dp["timestamp"],
                value=dp["value"],
                dimensions=request.dimensions if request.dimensions else None
            ))

        return MetricQueryResult(
            metric_name=request.metric_name,
            datapoints=datapoints
        )
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from OpenAI response: {e}")
        print(f"OpenAI response content: {response.choices[0].message.content}")
        return MetricQueryResult(metric_name=request.metric_name, datapoints=[])
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return MetricQueryResult(metric_name=request.metric_name, datapoints=[])