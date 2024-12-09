import pytest
from unittest.mock import MagicMock
from app import create_app
from types import SimpleNamespace
import uuid


@pytest.fixture
def mock_cassandra_session(monkeypatch):
    # Mock cluster and session objects
    mock_cluster = MagicMock()
    mock_session = MagicMock()

    # Mock the connect_to_cassandra function to return the mock objects
    monkeypatch.setattr('app.connect_to_cassandra', lambda: (mock_cluster, mock_session))
    return mock_session


@pytest.fixture
def mock_cache(monkeypatch):
    # Create a mock cache object that doesn't hit Redis
    mock_cache = MagicMock()
    # Ensure cache methods return simple values and don't attempt real connections
    mock_cache.get.return_value = None
    mock_cache.delete.return_value = True
    mock_cache.clear.return_value = True

    # Replace 'app.cache' with this mock
    monkeypatch.setattr('app.cache', mock_cache)
    return mock_cache


@pytest.fixture
def app(mock_cassandra_session, mock_cache):
    """Test application fixture."""
    application = create_app()
    application.testing = True

    # If needed, you could switch the cache backend here for testing:
    # application.config['CACHE_TYPE'] = 'SimpleCache'

    return application


@pytest.fixture
def client(app):
    return app.test_client()


### Tests

def test_get_categories(client, mock_cassandra_session):
    """Test fetching all categories."""
    # Return objects that have attributes, not MagicMocks
    mock_cassandra_session.execute.return_value = [
        SimpleNamespace(id="1234", name="Men"),
        SimpleNamespace(id="5678", name="Women")
    ]

    response = client.get('/api/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['name'] == "Men"


def test_add_category(client, mock_cassandra_session, mock_cache):
    """Test adding a new category."""
    # Just ensure this doesn't fail due to Redis or JSON issues
    response = client.post('/api/categories', json={"name": "New Category"})
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["name"] == "New Category"
    mock_cassandra_session.execute.assert_called_once()
    mock_cache.delete.assert_called_with("all_categories")


def test_add_category_missing_name(client):
    """Test adding a category without a name."""
    response = client.post('/api/categories', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Category name is required"


def test_get_clothes(client, mock_cassandra_session):
    """Test fetching clothes with filters."""
    mock_result = MagicMock()
    mock_result.current_rows = [
        SimpleNamespace(
            id="1234", name="T-Shirt", size="M", price=20.0, stock=50,
            color="Red", brand="Brand A", material="Cotton",
            description="Casual T-Shirt", is_available=True,
            category_id="5678", rating=4.5
        )
    ]
    mock_cassandra_session.execute.return_value = mock_result

    response = client.get('/api/clothes', query_string={"size": "M"})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["clothes"]) == 1
    assert data["clothes"][0]["name"] == "T-Shirt"


def test_add_clothes(client, mock_cassandra_session, mock_cache):
    """Test adding a new clothes item."""
    valid_uuid = str(uuid.uuid4())
    payload = {
        "category_id": valid_uuid,
        "name": "Jeans",
        "size": "L",
        "price": 40.0,
        "stock": 20,
        "color": "Blue",
        "brand": "Brand B",
        "material": "Denim",
        "description": "Comfortable jeans",
        "is_available": True,
        "rating": 4.0,
    }
    response = client.post('/api/clothes', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    mock_cassandra_session.execute.assert_called_once()
    mock_cache.clear.assert_called_once()


def test_get_single_clothes(client, mock_cassandra_session):
    """Test fetching a single clothes item."""
    mock_result = MagicMock()
    mock_result.one_or_none.return_value = SimpleNamespace(
        id="1234",
        name="T-Shirt",
        size="M",
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
    mock_cassandra_session.execute.return_value = mock_result

    response = client.get('/api/clothes/1234')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "T-Shirt"


def test_get_single_clothes_not_found(client, mock_cassandra_session):
    """Test fetching a non-existent clothes item."""
    mock_result = MagicMock()
    mock_result.one_or_none.return_value = None
    mock_cassandra_session.execute.return_value = mock_result

    response = client.get('/api/clothes/1234')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Clothes item not found"
