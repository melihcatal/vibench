def stream_platform_generation(response):
    for event in response['body']['choices']:
        yield event['text']