from azure.ai.vision.imageanalysis.models import VisualFeatures

class VisionModels:
    @staticmethod
    def get_visual_features():
        return [VisualFeatures.OBJECTS, VisualFeatures.CAPTION, VisualFeatures.TEXT, VisualFeatures.ADULT]