import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

# Create a Service Bus client using the connection string
client = ServiceBusClient.from_connection_string(
    conn_str=os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
)

with client:
    # Get the dead letter queue sender
    sender = client.get_queue_sender(queue_name="your-dead-letter-queue")
    with sender:
        # Create a message
        message = ServiceBusMessage("Failed message 1")
        # Send the message
        sender.send_messages(message)
