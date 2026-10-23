def normalize_request(instances):
    return [{'content': instance} for instance in instances]

def normalize_response(response):
    return [prediction['content'] for prediction in response.predictions]