import os

class ObservabilityClient:
    def __init__(self, api_key, service_url):
        self.api_key = api_key
        self.service_url = service_url

    @staticmethod
    def load_config(config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            return config['api_key'], config['service_url']

    def get_metric_data(self, metric_name, start_time, end_time):
        # Placeholder for actual API call
        pass

    # Additional helper methods can be added here

if __name__ == '__main__':
    config_path = 'path_to_config.json'
    api_key, service_url = ObservabilityClient.load_config(config_path)
    client = ObservabilityClient(api_key, service_url)
    # Example usage
    # client.get_metric_data('example_metric', '2021-01-01T00:00:00Z', '2021-01-02T00:00:00Z')