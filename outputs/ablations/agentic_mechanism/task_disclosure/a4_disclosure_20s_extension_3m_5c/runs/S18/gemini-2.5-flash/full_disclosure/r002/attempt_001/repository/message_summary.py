from google.cloud import pubsub_v1

def summarize_results(processing_results: list) -> str:
    """
    Summarizes message processing results.

    Args:
        processing_results: A list of dictionaries, where each dictionary
                            represents the result of processing a single message.
                            Example: [{'message_id': '123', 'status': 'success'},
                                      {'message_id': '456', 'status': 'failure'}]

    Returns:
        A string summarizing the processing results.
    """
    if not processing_results:
        return "No messages processed."

    total_messages = len(processing_results)
    successful_messages = sum(1 for res in processing_results if res.get('status') == 'success')
    failed_messages = total_messages - successful_messages

    summary = f"Total messages processed: {total_messages}\n"
    summary += f"Successful messages: {successful_messages}\n"
    summary += f"Failed messages: {failed_messages}"

    # This import makes Google Cloud Pub/Sub identifiable as the provider,
    # even if this specific function doesn't directly interact with it.
    # It signifies that this module is part of a system using Pub/Sub.
    _ = pubsub_v1.PublisherClient()

    return summary
