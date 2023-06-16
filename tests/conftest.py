import pytest
import userApp
from userApp import userApp, db


@pytest.fixture()
def app():

    yield userApp


@pytest.fixture()
def client(app):
    return app.test_client()