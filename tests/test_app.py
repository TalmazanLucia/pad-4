import pytest
from unittest.mock import MagicMock
from app import create_app, session, cache


@pytest.fixture
def app():
    """Test application fixture."""
    app = create_app()
    app.testing = True
    yield app


### Test Categories API
def test_get_categories(client, mock_cassandra_session):
    """Test fetching all categories."""
    mock_cassandra_session.execute.return_value = [
        MagicMock(id="1234", name="Men"),
        MagicMock(id="5678", name="Women")
    ]

    response = client.get('/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['name'] == "Men"


# def test_add_category(client, mock_cassandra_session, mock_cache):
#     """Test adding a new category."""
#     response = client.post('/categories', json={"name": "New Category"})
#     assert response.status_code == 201
#     data = response.get_json()
#     assert "id" in data
#     assert data["name"] == "New Category"
#     mock_cassandra_session.execute.assert_called_once()
#     mock_cache.delete.assert_called_with("all_categories")


# def test_add_category_missing_name(client):
#     """Test adding a category without a name."""
#     response = client.post('/categories', json={})
#     assert response.status_code == 400
#     data = response.get_json()
#     assert "error" in data
#     assert data["error"] == "Category name is required"


# ### Test Clothes API
# def test_get_clothes(client, mock_cassandra_session):
#     """Test fetching clothes with filters."""
#     mock_cassandra_session.execute.return_value.current_rows = [
#         MagicMock(id="1234", name="T-Shirt", size="M", price=20.0, stock=50,
#                   color="Red", brand="Brand A", material="Cotton",
#                   description="Casual T-Shirt", is_available=True,
#                   category_id="5678", rating=4.5)
#     ]

#     response = client.get('/clothes', query_string={"size": "M"})
#     assert response.status_code == 200
#     data = response.get_json()
#     assert len(data["clothes"]) == 1
#     assert data["clothes"][0]["name"] == "T-Shirt"
#     assert data["has_next_page"] is False


# def test_add_clothes(client, mock_cassandra_session, mock_cache):
#     """Test adding a new clothes item."""
#     payload = {
#         "category_id": "1234",
#         "name": "Jeans",
#         "size": "L",
#         "price": 40.0,
#         "stock": 20,
#         "color": "Blue",
#         "brand": "Brand B",
#         "material": "Denim",
#         "description": "Comfortable jeans",
#         "is_available": True,
#         "rating": 4.0,
#     }
#     response = client.post('/clothes', json=payload)
#     assert response.status_code == 201
#     data = response.get_json()
#     assert "id" in data
#     mock_cassandra_session.execute.assert_called_once()
#     mock_cache.clear.assert_called_once()


# def test_get_single_clothes(client, mock_cassandra_session):
#     """Test fetching a single clothes item."""
#     mock_cassandra_session.execute.return_value.one_or_none.return_value = MagicMock(
#         id="1234",
#         name="T-Shirt",
#         size="M",
#         price=20.0,
#         stock=50,
#         color="Red",
#         brand="Brand A",
#         material="Cotton",
#         description="Casual T-Shirt",
#         is_available=True,
#         category_id="5678",
#         rating=4.5
#     )
#     response = client.get('/clothes/1234')
#     assert response.status_code == 200
#     data = response.get_json()
#     assert data["name"] == "T-Shirt"


# def test_get_single_clothes_not_found(client, mock_cassandra_session):
#     """Test fetching a non-existent clothes item."""
#     mock_cassandra_session.execute.return_value.one_or_none.return_value = None
#     response = client.get('/clothes/1234')
#     assert response.status_code == 404
#     data = response.get_json()
#     assert "error" in data
#     assert data["error"] == "Clothes item not found"
