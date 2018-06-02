Build container for model:
```bash
gcloud container builds submit --gcs-source-staging-dir=gs://djr-data/cloudbuild \
    --async --timeout 4h0m0s --config cloudbuild.yaml .
```

Test running container locally:
```bash
export PROJECT_ID=$(gcloud config get-value project -q)
export IMAGE_ID=gcr.io/${PROJECT_ID}/code-names:latest
gcloud docker -- pull ${IMAGE_ID}
docker run -p 8050:8050 ${IMAGE_ID}
```