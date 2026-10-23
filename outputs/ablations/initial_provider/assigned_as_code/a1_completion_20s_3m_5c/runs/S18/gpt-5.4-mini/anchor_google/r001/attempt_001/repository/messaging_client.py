import os


def _config_value(config, key, env_key, default=None):
    if key in config and config[key] is not None:
        return config[key]
    value = os.getenv(env_key)
    if value is not None:
        return value
    return default


def get_publisher_config(config=None):
    config = config or {}
    return {
        "project_id": _config_value(config, "project_id", "GOOGLE_CLOUD_PROJECT"),
        "topic_id": _config_value(config, "topic_id", "PUBSUB_TOPIC_ID"),
        "dead_letter_topic_id": _config_value(config, "dead_letter_topic_id", "PUBSUB_DEAD_LETTER_TOPIC_ID", _config_value(config, "topic_id", "PUBSUB_TOPIC_ID")),
    }


def get_subscriber_config(config=None):
    config = config or {}
    return {
        "project_id": _config_value(config, "project_id", "GOOGLE_CLOUD_PROJECT"),
        "subscription_id": _config_value(config, "subscription_id", "PUBSUB_SUBSCRIPTION_ID"),
        "timeout": int(_config_value(config, "timeout", "PUBSUB_TIMEOUT_SECONDS", 30)),
    }
