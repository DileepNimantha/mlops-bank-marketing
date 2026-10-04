"""Configure MLflow to use the project's DagsHub tracking server."""

import os

import mlflow

REPOSITORY = "mlops-bank-marketing"


def configure() -> None:
    """Set the DagsHub MLflow URI and credentials from Codespaces secrets."""
    owner = os.environ.get("DAGSHUB_OWNER")
    token = os.environ.get("DAGSHUB_TOKEN")
    if not owner or not token:
        missing = [
            name
            for name, value in (("DAGSHUB_OWNER", owner), ("DAGSHUB_TOKEN", token))
            if not value
        ]
        raise RuntimeError(f"Required environment variable(s) not set: {', '.join(missing)}")

    os.environ["MLFLOW_TRACKING_USERNAME"] = owner
    os.environ["MLFLOW_TRACKING_PASSWORD"] = token
    mlflow.set_tracking_uri(f"https://dagshub.com/{owner}/{REPOSITORY}.mlflow")
