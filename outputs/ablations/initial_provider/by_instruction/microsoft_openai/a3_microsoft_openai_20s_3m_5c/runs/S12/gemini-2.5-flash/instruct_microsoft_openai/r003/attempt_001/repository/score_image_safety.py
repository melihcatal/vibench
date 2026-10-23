import os
from google.cloud import videointelligence_v1 as videointelligence

def score_image_safety(image_uri: str) -> dict:
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.SHOT_CHANGE_DETECTION, videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]

    # The Video Intelligence API is designed for video, but we can use it for static images
    # by treating the image as a single frame video. This is a common workaround.
    video_context = videointelligence.VideoContext(explicit_content_detection=videointelligence.ExplicitContentDetectionConfig(model='builtin/stable'))

    operation = client.annotate_video(
        request={
            "input_uri": image_uri,
            "features": features,
            "video_context": video_context
        }
    )

    print("Processing video for explicit content annotations.")
    result = operation.result(timeout=300) # Increased timeout for potential processing time

    # Explicit content detection results
    if result.annotation_results and result.annotation_results[0].explicit_content_annotation:
        explicit_content_likelihoods = []
        for frame in result.annotation_results[0].explicit_content_annotation.frames:
            explicit_content_likelihoods.append(frame.pornography_likelihood)
        
        # Take the maximum likelihood across all frames (for a single image, there's usually one frame)
        max_likelihood = max(explicit_content_likelihoods) if explicit_content_likelihoods else videointelligence.Likelihood.UNKNOWN

        return {"explicit_content_likelihood": videointelligence.Likelihood(max_likelihood).name}
    else:
        return {"explicit_content_likelihood": videointelligence.Likelihood.UNKNOWN.name}
