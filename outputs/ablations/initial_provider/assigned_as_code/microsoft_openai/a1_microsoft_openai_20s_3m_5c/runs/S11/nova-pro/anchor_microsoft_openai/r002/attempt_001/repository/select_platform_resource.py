from invoke_platform_model import invoke_platform_model


def select_platform_resource(resource_name, config):
    if resource_name == 'model':
        return config['deployment']
    elif resource_name == 'deployment':
        return config['deployment']
    elif resource_name == 'inference':
        return config['deployment']
    else:
        raise ValueError('Invalid resource name')