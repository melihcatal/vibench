# Utility Scripts

- [`check_litellm_models.py`](check_litellm_models.py): inspect available LiteLLM model routes.
- [`prepare_hf_upload.py`](prepare_hf_upload.py): stage the `vibench-emnlp26/vibench` and `vibench-emnlp26/vibench-results` Hugging Face dataset uploads from the current benchmark, configs, raw outputs, labeled outputs, reports, and compact Space/viewer indices.

Prepare upload folders:

```bash
make hf-stage
```

Upload the benchmark with normal `hf upload`; upload the full result bundle with
the resumable large-folder path:

```bash
make hf-upload
```
