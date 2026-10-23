import os


DEFAULT_MODEL = "gemini-2.5-flash"


def build_model_config(config=None):
    config = dict(config or {})
    config["model"] = config.get("model") or os.environ.get("GOOGLE_MODEL", DEFAULT_MODEL)
    return config


def get_api_key(config, env_name):
    return config.get("api_key") or os.environ[env_name]


def build_prompt(instruction, text):
    return instruction.strip() + "\n\n" + text
