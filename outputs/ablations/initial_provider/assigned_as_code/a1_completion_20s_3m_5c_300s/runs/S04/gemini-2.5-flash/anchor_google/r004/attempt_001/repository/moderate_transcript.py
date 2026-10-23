import googleapiclient.discovery

def moderate_transcript(text_segment):
    # Using the Perspective API for text moderation
    # https://developers.perspectiveapi.com/s/about-the-api
    client = googleapiclient.discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey="YOUR_API_KEY" # Replace with your actual API key
    )

    analyze_request = {
        'comment': {'text': text_segment},
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = client.comments().analyze(body=analyze_request).execute()
    
    # A score of 0.5 or higher generally indicates a high likelihood of toxicity.
    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']

    return {
        "text": text_segment,
        "toxicity_score": toxicity_score,
        "is_toxic": toxicity_score > 0.5 # Example threshold
    }
