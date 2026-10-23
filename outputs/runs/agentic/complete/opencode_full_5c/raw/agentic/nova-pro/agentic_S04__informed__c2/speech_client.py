import os


def load_config():
    return {"ASSEMBLYAI_API_KEY": os.getenv("ASSEMBLYAI_API_KEY")}


def create_client():
    from assemblyai import AssemblyAI

    config = load_config()
    return AssemblyAI(api_key=config["ASSEMBLYAI_API_KEY"])
