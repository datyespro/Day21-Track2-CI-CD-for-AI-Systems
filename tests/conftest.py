"""
conftest.py — cau hinh chung cho pytest.

Set MLFLOW_TRACKING_URI de chi toi mot thu muc tam thoi trong moi test,
tranh xung dot voi MLflow server dang chay va dam bao tests chay duoc
trong GitHub Actions ma khong can MLflow server.
"""
import os
import pytest


@pytest.fixture(autouse=True)
def set_mlflow_tracking(tmp_path):
    """Tro MLflow toi thu muc tam thoi thay vi server HTTP."""
    uri = f"file:///{tmp_path.as_posix()}/mlruns"
    os.environ["MLFLOW_TRACKING_URI"] = uri
    yield
    del os.environ["MLFLOW_TRACKING_URI"]
