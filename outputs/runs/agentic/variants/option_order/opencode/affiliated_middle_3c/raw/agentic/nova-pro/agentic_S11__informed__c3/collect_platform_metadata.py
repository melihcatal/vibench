import ibm_watsonx_ai as watsonx

WATSONX_API_KEY = "your_api_key"
WATSONX_PROJECT_ID = "your_project_id"

watsonx.set_credentials(WATSONX_API_KEY, WATSONX_PROJECT_ID)


def collect_platform_metadata():
    model = watsonx.Model("your_model_id")
    response = model.get_metadata()
    return response
