import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from messaging_models import Event

def summarize_message_processing(event: Event) -> str:
    key = os.environ.get("AZURE_TEXT_ANALYTICS_KEY")
    endpoint = os.environ.get("AZURE_TEXT_ANALYTICS_ENDPOINT")

    if not key or not endpoint:
        print("Azure Text Analytics credentials not set. Providing basic summary.")
        return f"Processed event ID: {event.id}, Type: {event.type}, Data: {event.data}"

    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    document = [str(event.data)]
    response = text_analytics_client.analyze_sentiment(documents=document)[0]
    sentiment = response.sentiment.value
    
    summary = f"Event ID: {event.id}\nEvent Type: {event.type}\nEvent Data: {event.data}\nSentiment: {sentiment}"
    return summary

if __name__ == "__main__":
    from pydantic import BaseModel
    class SampleData(BaseModel):
        message: str

    example_event_positive = Event(id="123", type="feedback", data=SampleData(message="I love this product!").dict())
    print("\n--- Positive Event Summary ---")
    print(summarize_message_processing(example_event_positive))

    example_event_negative = Event(id="456", type="feedback", data=SampleData(message="This product is terrible.").dict())
    print("\n--- Negative Event Summary ---")
    print(summarize_message_processing(example_event_negative))

    example_event_neutral = Event(id="789", type="information", data=SampleData(message="This is a factual statement.").dict())
    print("\n--- Neutral Event Summary ---")
    print(summarize_message_processing(example_event_neutral))
