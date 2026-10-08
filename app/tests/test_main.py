from datetime import datetime
from unittest.mock import ANY

from httpx import AsyncClient
from schema import TodoResponse

data = {"name":"joshua", "completed": True}


async def test_empyt_read_todos(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == []


async def test_read_todos(client: AsyncClient):
    for i in range(5):
        response = await client.post('/', json={"name":f"todo_{i}", "completed": True})
        assert response.status_code == 201
        assert response.json() == {"msg": f"Todo todo_{i} added successfully"} 
    
    response = await client.get("/")
    assert response.status_code == 200
    
    data_ = response.json()
    validate_todo = [TodoResponse.model_validate(item) for item in data_]
    
    assert len(validate_todo) == 5
    assert validate_todo[0].name == "todo_0"


async def test_add_todo(client):
    response = await client.post('/', json=data)
    assert response.status_code == 201
    assert response.json() == {"msg": "Todo joshua added successfully"} 


async def test_get_todo_by_id(client: AsyncClient):
    await client.post('/', json=data)
    response = await client.get('/1' )
    assert response.status_code == 200
    
    data_ = response.json()
    TodoResponse.model_validate(data_) # allowing pydantic to validate all fields and return 422 if any gose wrong

async def test_get_todo_by_id_1(client: AsyncClient):
    await client.post("/", json={"name": "joshua", "completed": True})
    response = await client.get("/1")
    assert response.status_code == 200

    # Parsing response JSON into your Pydantic model
    todo = TodoResponse.model_validate(response.json())

    # Assert values for fixed fields
    assert todo.id == 1
    assert todo.name == "joshua"
    assert todo.completed is True

    # Assert using type checker on the timestamp
    assert isinstance(todo.created_at, datetime)
    

async def test_get_todo_by_id_2(client: AsyncClient):
    await client.post("/", json={"name": "joshua", "completed": True})
    response = await client.get("/1")
    assert response.status_code == 200

    # Validate response structure with Pydantic
    todo = TodoResponse.model_validate(response.json())

    # Dump to dict and compare whole payload using ANY for created_at
    assert todo.model_dump() == {
        "id": 1,
        "name": "joshua",
        "completed": True,
        "created_at": ANY
        }        
    
async def test_update_todo(client: AsyncClient):
    await client.post('/', json=data)
    response = await client.put('/1', json= {"name": "ifeanyi", "completed": False})
    assert response.status_code == 200
    assert response.json() == {"msg": "Todo for id: 1 updated successfully"} 

async def test_delete_todo(client: AsyncClient):
    post_rqt = await client.post('/', json=data)
    assert post_rqt.status_code == 201
    response = await client.delete('/1')
    assert response.status_code == 204
    
    
    
    
    
    

# # # tests/test_models.py
# # import pytest
# # from app.model import User

# # @pytest.mark.asyncio
# # async def test_create_user_in_db(db_session):
# #     """Uses the isolated db_session fixture for async direct database queries."""
# #     new_user = User(username="joshua", email="joshua@example.com")
# #     db_session.add(new_user)
# #     await db_session.commit()

# #     # Query the user back from the database
# #     result = await db_session.get(User, new_user.id)
# #     assert result is not None
# #     assert result.username == "joshua"