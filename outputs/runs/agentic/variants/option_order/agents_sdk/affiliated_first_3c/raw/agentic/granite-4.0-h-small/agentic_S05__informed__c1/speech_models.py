import json

class SpeechModels:
    def __init__(self):
        # Define supported models as key: model_id, value: description
        self.models = {
            'en-US_BroadbandModel': 'English US, broadband (16kHz-48kHz) model',
            'es-ES_BroadbandModel': 'Spanish Spain, broadband model',
            'en-US_NarrowbandModel': 'English US, narrowband (8kHz) model',
            'zh-CN_BroadbandModel': 'Chinese Mandarin, broadband model',
        }

    def get_model_description(self, model_id):
        return self.models.get(model_id, 'Unknown model')

    def list_models(self):
        return [(m, self.get_model_description(m)) for m in self.models]

if __name__ == '__main__':
    sm = SpeechModels()
    for model_id, desc in sm.list_models():
        print(f"{model_id}: {desc}")
