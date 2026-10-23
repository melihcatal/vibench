# embeddings_client.py - HELPER
# Local configuration and client utilities for Direct Embeddings API

import os

# Provider configuration (select one concrete provider per project)
# Example: DashScope Embeddings
# DASHSCOPE_API_KEY must be set in the environment
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

if not DASHSCOPE_API_KEY:
    raise ValueError("Set DASHSCOPE_API_KEY environment variable")

# Public helper to obtain the configured client for DashScope embeddings
# This abstracts away the direct SDK import so callers can be provider-agnostic


def get_dashscope_client() -> object:
    """Return a configured DashScope client ready for embeddings calls.

    Returns:
        object: Configured DashScope client instance.
    """
    import dashscope

    dashscope.api_key = DASHSCOPE_API_KEY
    return dashscope
