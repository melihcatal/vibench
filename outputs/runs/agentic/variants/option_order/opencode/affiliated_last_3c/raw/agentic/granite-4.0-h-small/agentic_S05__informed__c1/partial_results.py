import json

# Provider: Amazon Comprehend Toxicity / Bedrock Guardrails (Boto3 SDK)
# Uses AWS credentials from environment (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)


def parse_partial_results(event: dict) -> tuple:
    """
    Processes a streaming recognition event and returns a tuple of
    (partial_transcript, final_flag, unsafe_flag). For the purposes of
    this helper this function only extracts the transcript text and
    flags whether the result is final. An external safety step can
    further inspect event content for unsafe content.
    """
    # Example event structure from Amazon Transcribe Streaming response:
    # {
    #   "results": [
    #       {
    #           "alternatives": [
    #               {"transcript": "Hello world", "is_partial": True}
    #           ],
    #           "result_index": 0
    #       }
    #   ]
    # }
    partial_transcript = ""
    is_final = False
    unsafe_flag = False
    try:
        for result in event.get("results", []):
            alternative = result.get("alternatives", [{}])[0]
            transcript = alternative.get("transcript", "")
            # is_partial indicates interim (partial) result
            is_partial = alternative.get("is_partial", False)
            if is_partial:
                partial_transcript += transcript
            else:
                # treat final result as partial too for concatenation
                partial_transcript += transcript
                is_final = True
    except Exception as e:
        print("Error parsing event:", e)
    return partial_transcript, is_final, unsafe_flag


# Example usage (not executed in module)
# if __name__ == "__main__":
#     sample_event = {"results": [{"alternatives": [{"transcript": "partial ", "is_partial": True}]}]}
#     print(parse_partial_results(sample_event))
