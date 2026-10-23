from google.cloud import vision
import os

def score_image_safety(image_content: bytes) -> dict:
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision Safe Search.
    Returns a dictionary of likelihood scores for various safety attributes.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    # Convert likelihood enum to string for easier interpretation
    likelihood_map = {
        vision.Likelihood.UNKNOWN: 'UNKNOWN',
        vision.Likelihood.VERY_UNLIKELY: 'VERY_UNLIKELY',
        vision.Likelihood.UNLIKELY: 'UNLIKELY',
        vision.Likelihood.POSSIBLE: 'POSSIBLE',
        vision.Likelihood.LIKELY: 'LIKELY',
        vision.Likelihood.VERY_LIKELY: 'VERY_LIKELY',
    }

    safety_scores = {
        'adult': likelihood_map.get(safe_search_annotation.adult, 'UNKNOWN'),
        'spoof': likelihood_map.get(safe_search_annotation.spoof, 'UNKNOWN'),
        'medical': likelihood_map.get(safe_search_annotation.medical, 'UNKNOWN'),
        'violence': likelihood_map.get(safe_search_annotation.violence, 'UNKNOWN'),
        'racy': likelihood_map.get(safe_search_annotation.racy, 'UNKNOWN'),
    }
    return safety_scores

if __name__ == '__main__':
    print("Running score_image_safety.py example...")
    dummy_image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82" # A tiny valid PNG

    safety_results = score_image_safety(dummy_image_content)
    print("Image safety scores:", safety_results)
