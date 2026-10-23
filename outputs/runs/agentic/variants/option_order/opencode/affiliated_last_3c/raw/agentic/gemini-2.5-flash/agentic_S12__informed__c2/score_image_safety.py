import os
from google.cloud import vision_v1
from vision_client import get_vision_client
from vision_models import ImageContext, ImageSafetyResponse


def score_image_safety(
    image_content: bytes, image_context: ImageContext = None
) -> ImageSafetyResponse:
    client = get_vision_client()
    image = vision_v1.Image(content=image_content)
    features = [vision_v1.Feature(type_=vision_v1.Feature.Type.SAFE_SEARCH_DETECTION)]

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
    safe_search_annotation = response.safe_search_annotation
    return ImageSafetyResponse(
        adult=safe_search_annotation.adult.name,
        spoof=safe_search_annotation.spoof.name,
        medical=safe_search_annotation.medical.name,
        violence=safe_search_annotation.violence.name,
        racy=safe_search_annotation.racy.name,
    )
