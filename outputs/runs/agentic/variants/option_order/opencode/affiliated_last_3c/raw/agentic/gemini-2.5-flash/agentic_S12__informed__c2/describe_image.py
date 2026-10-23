import os
from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import ImageContext, DescribedImageResponse


def describe_image(
    image_content: bytes, image_context: ImageContext = None
) -> DescribedImageResponse:
    client = get_vision_client()
    image = vision_v1.Image(content=image_content)
    features = [vision_v1.Feature(type_=vision_v1.Feature.Type.WEB_DETECTION)]

    request = vision_v1.AnnotateImageRequest(
        image=image,
        features=features,
    )
    if image_context:
        request.image_context = vision_v1.ImageContext(
            language_hints=image_context.language_hints,
            lat_long_rect=vision_v1.LatLongRect(
                lat_lngs=[
                    vision_v1.LatLng(
                        latitude=image_context.lat_long_rect.latitude_north,
                        longitude=image_context.lat_long_rect.longitude_west,
                    ),
                    vision_v1.LatLng(
                        latitude=image_context.lat_long_rect.latitude_south,
                        longitude=image_context.lat_long_rect.longitude_east,
                    ),
                ]
            )
            if image_context.lat_long_rect
            else None,
        )

    response = client.annotate_image(request=request)
    best_guess_labels = (
        [label.label for label in response.web_detection.best_guess_labels]
        if response.web_detection
        else []
    )
    full_matching_images = (
        [image.url for image in response.web_detection.full_matching_images]
        if response.web_detection
        else []
    )
    return DescribedImageResponse(
        best_guess_labels=best_guess_labels, full_matching_images=full_matching_images
    )
