from dataclasses import dataclass


@dataclass
class PlatformRequest:
    prompt: str
    model_id: str
    system: str | None = None

    def to_messages(self):
        return [{"role": "user", "content": [{"text": self.prompt}]}]

    def to_system(self):
        return [] if self.system is None else [{"text": self.system}]


def normalize_text(text: str):
    return text.strip()


def to_platform_response(response, resource):
    return {"response": response, "resource": resource}


def stream_platform_chunks(response, resource):
    return {"stream": response, "resource": resource}


def collect_metadata(response, resource):
    return {
        "output": response,
        "metadata": {
            "resource": resource,
            "usage": response.get("usage", {}) if isinstance(response, dict) else {},
        },
    }
