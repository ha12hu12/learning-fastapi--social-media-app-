import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.database import get_db, Base
from app.config import settings
from app.oauth2 import create_access_token
from app import models

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

print

SQL_DATABASE_URL = f'''postgresql://{settings.database_username}:{settings.
database_password}@{settings.database_hostname}:{settings.
database_port}/{settings.database_name}_test'''

engine = create_engine(SQL_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "ha12hu12@gmail.com",
                "password": "ha12hu12345password"}
    
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "huss12@gmail.com",
                "password": "huss123456x2password"}
    
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def post_for_testing(test_user, test_user2, session):
    posts_data = [
        {
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, 
            {
        "title": "4rd title",
        "content": "4rd content",
        "owner_id": test_user2['id']
    }
]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts_list = list(post_map)

    session.add_all(posts_list)

    session.commit()
    
    posts = session.query(models.Post).all()

    return posts

@pytest.fixture
def add_vote_data(post_for_testing):
    data = {
    "post_id": post_for_testing[3].id, #so i dont vote on MY post
    "dir": 1
    }

    return data

@pytest.fixture
def delete_vote_data(post_for_testing):
    data = {
    "post_id": post_for_testing[3].id, 
    "dir": 0
    }

    return data

@pytest.fixture
def vote_for_testing(session, test_user, post_for_testing):

    data = {
        "post_id": post_for_testing[3].id,
        "user_id": test_user["id"]
    }

    new_vote = models.Vote(post_id=data["post_id"], 
                           user_id=data["user_id"])

    session.add(new_vote)
    session.commit()
