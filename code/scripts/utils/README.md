# Utility Scripts

- [`check_litellm_models.py`](check_litellm_models.py): inspect available
  LiteLLM model routes.
- [`runnable_models.py`](runnable_models.py): print the subset of a config's
  models whose credentials are configured, so smoke runs skip the rest instead
  of erroring.
- [`register_model.py`](register_model.py): add a model to
  `benchmark/vibench/models.json` with the metadata the runners and evaluator
  expect.
