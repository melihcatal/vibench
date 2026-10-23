from google.cloud import vision

from vision_client import get_vision_client, make_image


def score_image_safety(image_path=None, image_uri=None):
    client = get_vision_client()
    image = make_image(image_path=image_path, image_uri=image_uri)
    response = client.safe_search_detection(image=image)
    likelihoods = response.safe_search_annotation
    return {
        "adult": vision.Likelihood(likelihoods.adult).name,
        "spoof": vision.Likelihood(likelihoods.spoof).name,
        "medical": vision.Likelihood(likelihoods.medical).name,
        "violence": vision.Likelihood(likelihoods.violence).name,
        "racy": vision.Likelihood(likelihoods.racy).name,
    }
