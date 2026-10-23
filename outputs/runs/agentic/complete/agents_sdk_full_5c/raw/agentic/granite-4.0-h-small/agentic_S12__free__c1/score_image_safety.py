import vision_client

def score_image_safety(image_path):
    # Use Google Cloud Vision's safe search detection to check for unsafe content
    # The `safe_search_detection` method returns categories like adult, violence, medical, etc.
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as f:
        content = f.read()
    image = vision.Image(content=content)
    response = client.safe_search_detection(image=image)
    # Return a simple risk rating based on annotation likelihood
    likelihood = response.safe_search_annotation.adult
    rating = {
        vision.Likelihood.VERY_UNLIKELY: 'Very Low',
        vision.Likelihood.UNLIKELY: 'Low',
        vision.Likelihood.POSSIBLE: 'Medium',
        vision.Likelihood.LIKELY: 'High',
        vision.Likelihood.VERY_LIKELY: 'Very High'
    }.get(likelihood, 'Unknown')
    return rating
