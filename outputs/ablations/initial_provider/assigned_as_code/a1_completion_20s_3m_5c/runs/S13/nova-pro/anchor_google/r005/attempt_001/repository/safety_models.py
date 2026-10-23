def normalize_response(response):
    return {
        'toxicity': response['attributeScores']['TOXICITY']['summaryScore']['value']
    }