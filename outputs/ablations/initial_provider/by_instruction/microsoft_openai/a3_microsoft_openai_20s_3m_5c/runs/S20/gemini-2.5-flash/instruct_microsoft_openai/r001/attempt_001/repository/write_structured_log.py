import os
import datetime
import json
from observability_client import observability_client
from observability_models import StructuredLogEvent

def write_structured_log(event_name: str, properties: dict):
    try:
        # Use Azure OpenAI to generate a structured log message
        # This simulates a service generating a log entry with AI assistance
        response = observability_client.azure_openai_client.chat.completions.create(
            model=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo"), # Example model
            messages=[
                {"role": "system", "content": "You are a logging assistant. Generate a structured JSON log message based on the user's input. Include a timestamp, eventName, and properties. Ensure the output is a valid JSON object only."},
                {"role": "user", "content": f"Generate a log for event: {event_name} with properties: {json.dumps(properties)}"}
            ],
            response_format={ "type": "json_object" }
        )

        generated_log_str = response.choices[0].message.content
        generated_log = json.loads(generated_log_str)

        # Assuming the generated log has 'message', 'level', 'timestamp' and other properties
        message = generated_log.get("message", f"Event {event_name} occurred.")
        level = generated_log.get("level", "info")
        timestamp = generated_log.get("timestamp", datetime.datetime.utcnow().isoformat() + "Z")
        
        # Create a StructuredLogEvent object
        structured_event = StructuredLogEvent(
            message=message,
            level=level,
            timestamp=timestamp,
            eventName=event_name,
            **properties
        )

        # In a real scenario, this would send to Azure Monitor via the OpenTelemetry handler
        # For this simulation, we'll print the generated structured log JSON
        print(f"Generated Structured Log: {structured_event.to_json()}")

    except Exception as e:
        print(f"Error writing structured log: {e}")

# Example usage (for testing purposes, not part of the final script output)
# if __name__ == "__main__":
#     write_structured_log(
#         event_name="UserLogin",
#         properties={
#             "userId": "user123",
#             "ipAddress": "192.168.1.1",
#             "status": "success"
#         }
#     )
