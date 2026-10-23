def collect_platform_metadata(response):
    return {
        'output': response['body']['results'][0]['outputText'],
        'metadata': response['modelMetadata']
    }