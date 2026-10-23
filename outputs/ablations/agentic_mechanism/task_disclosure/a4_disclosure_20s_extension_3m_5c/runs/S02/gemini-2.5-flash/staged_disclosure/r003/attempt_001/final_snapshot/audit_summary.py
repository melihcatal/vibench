
import boto3
import datetime

def summarize_federated_login_events(num_events=100):
    """
    Summarizes recent AWS CloudTrail events related to federated logins.
    """
    client = boto3.client('cloudtrail')

    # Define a time window for the events (e.g., last 7 days)
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(days=7)

    federated_events = []
    paginator = client.get_paginator('lookup_events')
    pages = paginator.paginate(
        LookupAttributes=[
            {
                'AttributeKey': 'EventName',
                'AttributeValue': 'FederatedLogin'
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
        MaxResults=num_events
    )

    for page in pages:
        for event in page['Events']:
            federated_events.append(event)
        if len(federated_events) >= num_events:
            break

    summary = {
        "total_federated_login_events": len(federated_events),
        "events": []
    }

    for event in federated_events:
        summary_event = {
            "event_id": event.get('EventId'),
            "event_name": event.get('EventName'),
            "event_source": event.get('EventSource'),
            "username": event.get('Username'),
            "event_time": event.get('EventTime').isoformat() if event.get('EventTime') else None,
            "aws_region": event.get('AwsRegion')
        }
        summary['events'].append(summary_event)

    return summary

if __name__ == "__main__":
    summary = summarize_federated_login_events(num_events=50)
    print("Federated Login Event Summary:")
    print(f"Total events found: {summary['total_federated_login_events']}")
    for event in summary['events']:
        print(f"  Event ID: {event['event_id']}, User: {event['username']}, Time: {event['event_time']}, Region: {event['aws_region']}")
