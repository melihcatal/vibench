"""[SAME-SCENARIO] checks an image for unsafe or policy-sensitive visual content"""
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from vision_client import image_to_b64, get_api_key
from vision_models import SafetyResponse

def score_image_safety(image_path: str) -> SafetyResponse:
    # Clarifai Image Recognition Moderation
    pat = get_api_key('CLARIFAI_PAT')
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)
    image_b64 = image_to_b64(image_path)
    request = service_pb2.PostModelOutputsRequest(
        model_id='c0cbee9ca1db480791b0d2b11ed3b5f7',
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(base64=image_b64)
                )
            )
        ]
    )
    metadata = (('authorization', f'Key {pat}'),)
    response = stub.PostModelOutputs(request, metadata=metadata)
    if response.status.status_code != status_code_pb2.SUCCESS:
        raise RuntimeError(f'Clarifai API error: {response.status.description}')
    concepts = response.outputs[0].data.concepts
    risks = [concept.name for concept in concepts if concept.value > 0.5]
    is_safe = len(risks) == 0
    return {'is_safe': is_safe, 'risks': risks}
