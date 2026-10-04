import os

import pytest

from src import tracking


def test_configure_sets_dagshub_tracking_uri_and_credentials(monkeypatch):
    monkeypatch.setenv("DAGSHUB_OWNER", "example-owner")
    monkeypatch.setenv("DAGSHUB_TOKEN", "example-token")
    tracking_uris = []
    monkeypatch.setattr(tracking.mlflow, "set_tracking_uri", tracking_uris.append)

    tracking.configure()

    assert tracking_uris == ["https://dagshub.com/example-owner/mlops-bank-marketing.mlflow"]
    assert os.environ["MLFLOW_TRACKING_USERNAME"] == "example-owner"
    assert os.environ["MLFLOW_TRACKING_PASSWORD"] == "example-token"


@pytest.mark.parametrize("missing_variable", ["DAGSHUB_OWNER", "DAGSHUB_TOKEN"])
def test_configure_requires_dagshub_secrets(monkeypatch, missing_variable):
    monkeypatch.setenv("DAGSHUB_OWNER", "example-owner")
    monkeypatch.setenv("DAGSHUB_TOKEN", "example-token")
    monkeypatch.delenv(missing_variable)
    tracking_uris = []
    monkeypatch.setattr(tracking.mlflow, "set_tracking_uri", tracking_uris.append)

    with pytest.raises(RuntimeError, match=missing_variable):
        tracking.configure()

    assert tracking_uris == []
