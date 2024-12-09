import pytest
from unittest.mock import MagicMock
from app import create_app
from types import SimpleNamespace
import uuid

@pytest.fixture
def mock_cassandra_session(monkeypatch):
    # Mock cluster and session
    mock_cluster = MagicMock()
    mock_session = MagicMock()
    monkeypatch.setattr('app.connect_to_cassandra', lambda: (mock_cluster, mock_session))
    return mock_session

@pytest.fixture
def app(mock_cassandra_session):
    """Test application fixture."""

    def test_create_app():
        application = create_app()
        application.testing = True
        application.config['CACHE_TYPE'] = 'SimpleCache'
        # Reinitialize cache with SimpleCache
        from flask_caching import Cache
        application.cache = Cache(application, config={'CACHE_TYPE': 'SimpleCache'})
        return application

    application = test_create_app()
    return application

@pytest.fixture
def mock_cache(monkeypatch, app):
    monkeypatch.setattr(app.cache, 'get', lambda key: None)
    monkeypatch.setattr(app.cache, 'delete', lambda key: True)
    monkeypatch.setattr(app.cache, 'clear', lambda: True)
    return app.cache

@pytest.fixture
def client(app):
    return app.test_client()

### Tests

def test_get_categories(client, mock_cassandra_session, mock_cache):
    """Test fetching all categories."""
    mock_cassandra_session.execute.return_value = [
        SimpleNamespace(id="1234", name="Men"),
        SimpleNamespace(id="5678", name="Women")
    ]
    response = client.get('/api/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['name'] == "Men"

def test_add_category_missing_name(client, mock_cache):
    """Test adding a category without a name."""
    response = client.post('/api/categories', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Category name is required"

def test_get_clothes(client, mock_cassandra_session, mock_cache):
    """Test fetching clothes with filters."""
    mock_result = MagicMock()
    mock_result.current_rows = [
        SimpleNamespace(
            id="1234",
            name="T-Shirt",
            size="M",            # Add the missing attribute
            price=20.0,
            stock=50,
            color="Red",
            brand="Brand A",
            material="Cotton",
            description="Casual T-Shirt",
            is_available=True,
            category_id="5678",
            rating=4.5
        )
    ]
    mock_cassandra_session.execute.return_value = mock_result

    response = client.get('/api/clothes')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["clothes"]) == 1
    assert data["clothes"][0]["name"] == "T-Shirt"