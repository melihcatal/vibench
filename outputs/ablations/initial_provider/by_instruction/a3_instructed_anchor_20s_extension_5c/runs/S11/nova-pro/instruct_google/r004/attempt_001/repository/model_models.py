def normalize_request(instances):
    return [{"content": instance} for instance in instances]

def normalize_response(predictions):
    return [prediction.prediction for prediction in predictions]