import boto3
import os
import google.generativeai as genai


class KeyUsageSummary:
    def __init__(self):
        self.cloudtrail_client = boto3.client(
            "cloudtrail", region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        self.gemini_model = None
        if os.getenv("GOOGLE_API_KEY"):
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.gemini_model = genai.GenerativeModel(
                "gemini-pro"
            )  # Using a common model

    def get_kms_audit_events(self, num_events: int = 10) -> list:
        # In a real scenario, you'd query CloudTrail or CloudWatch Logs.
        # For this demonstration, we'll return simulated events.
        # Provider-identifying signal: boto3.client('cloudtrail')

        # Simulate calling CloudTrail to get recent KMS events
        # Example of what real CloudTrail lookup_events might return (simplified)
        simulated_events = []
        for i in range(num_events):
            event = {
                "EventId": f"event-{i}",
                "EventName": "Encrypt" if i % 2 == 0 else "Decrypt",
                "EventSource": "kms.amazonaws.com",
                "Username": f"user-{i % 3}",
                "Resources": [
                    {
                        "ResourceType": "AWS::KMS::Key",
                        "ResourceName": os.getenv(
                            "KMS_KEY_ID",
                            "arn:aws:kms:us-east-1:123456789012:key/some-key-id",
                        ),
                    }
                ],
                "EventTime": f"2026-04-18T10:00:{i:02}Z",
            }
            simulated_events.append(event)

        # In a real implementation, you would use lookup_events or integrate with CloudWatch Logs
        # try:
        #     response = self.cloudtrail_client.lookup_events(
        #         LookupAttributes=[
        #             {'AttributeKey': 'EventSource', 'AttributeValue': 'kms.amazonaws.com'}
        #         ],
        #         MaxResults=num_events
        #     )
        #     return response.get('Events', [])
        # except Exception as e:
        #     print(f"Error fetching CloudTrail events: {e}")
        #     return []
        return simulated_events

    def summarize_events_with_gemini(self, events: list) -> str:
        if not self.gemini_model:
            return "Gemini API not configured. Cannot summarize events."

        event_strings = []
        for event in events:
            event_strings.append(
                f"EventId: {event.get('EventId')}, Name: {event.get('EventName')}, User: {event.get('Username')}, Time: {event.get('EventTime')}"
            )

        prompt = "Summarize the following AWS KMS key usage events:\n" + "\n".join(
            event_strings
        )

        try:
            # Provider-identifying signal: genai.GenerativeModel('gemini-pro')
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error summarizing with Gemini API: {e}"
