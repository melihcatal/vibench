def summarize_message_processing_results(results):
    total_messages = len(results)
    successful_messages = 0
    failed_messages = 0
    errors = []
    processed_message_ids = []

    for result in results:
        if "error" in result:
            failed_messages += 1
            errors.append(result["error"])
        elif "message_id" in result:
            successful_messages += 1
            processed_message_ids.append(result["message_id"])
        elif "dead_letter_message_id" in result:
            failed_messages += 1 # Consider dead-lettered as a form of failure for summary
            processed_message_ids.append(result["dead_letter_message_id"])

    summary = {
        "total_messages": total_messages,
        "successful_messages": successful_messages,
        "failed_messages": failed_messages,
        "processed_message_ids": processed_message_ids,
        "errors": errors if errors else None
    }
    return summary
