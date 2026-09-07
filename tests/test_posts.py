from app import schemas
import pytest
from fastapi import status


#------TESTING GET ALL POSTS---------

def test_get_all_posts(authorized_client, post_for_testing):
    res = authorized_client.get("/posts/")

    assert len(res.json()) == len(post_for_testing)
    assert res.status_code == 200

def test_unauthorized_get_all_posts(client, post_for_testing):
    res = client.get("/posts/")

    assert res.status_code == 401


#------TESTING GET ONE POST---------

def test_get_one_post(authorized_client, post_for_testing):
    id = post_for_testing[0].id

    res = authorized_client.get(f"/posts/{id}")

    post = schemas.PostVote(**res.json())

    assert post.Post.id == post_for_testing[0].id
    assert post.Post.content == post_for_testing[0].content
    assert post.Post.title == post_for_testing[0].title

def test_unauthorized_get_one_post(client, post_for_testing):
    id = post_for_testing[0].id

    res = client.get(f"/posts/{id}")

    assert res.status_code == 401


def test_get_one_NonExist_post(authorized_client):
    res = authorized_client.get("/posts/999999")

    assert res.status_code == 404


#------TESTING CREATE POST-----------

@pytest.mark.parametrize("title, content, published", [
    ("cool title!", "coolest title ever", True),
    ("EATING!", "potato", False),
    ("orca", "fishing", True)
])
def test_create_post(authorized_client, test_user, title, content, published): 
    res = authorized_client.post("/posts/", json={"title": title, 
                                                  "content": content, 
                                                  "published": published})

    new_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.published == published
    assert new_post.owner_id == test_user["id"]


def test_unauthorized_create_post(client):
    res = client.post("/posts/", 
    json={"title": "unauthorized", 
          "content": "trying to create a post unauthorized"})

    assert res.status_code == 401


def test_create_post_default_published(authorized_client, test_user): 
    res = authorized_client.post("/posts/", 
                        json={"title": "published is default", 
                        "content": "trying published default"})

    new_post = schemas.PostResponse(**res.json())

    assert res.status_code == 201
    assert new_post.title == "published is default"
    assert new_post.content == "trying published default"
    assert new_post.published == True
    assert new_post.owner_id == test_user["id"]


#------------TESTING DELETE POST------------

def test_authorized_delete_post(authorized_client, post_for_testing):
    id = post_for_testing[0].id

    res = authorized_client.delete(
        f"/posts/{id}")

    assert res.status_code == status.HTTP_204_NO_CONTENT

def test_unauthorized_delete_post(client, post_for_testing):
    id = post_for_testing[0].id

    res = client.delete(f"/posts/{id}")

    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_non_exist_post(authorized_client):
    res = authorized_client.delete("/posts/99999999")

    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_delete_other_user_post(authorized_client, post_for_testing,
                                test_user2):
    id = post_for_testing[3].id

    res = authorized_client.delete(f"/posts/{id}")

    assert res.status_code == status.HTTP_403_FORBIDDEN


#-------TESTING UPDATE POST---------

data = {"title": "updated title",
    "content": "updated content",
    "published": False}


def test_authorized_update_post(authorized_client,
                                post_for_testing):
    
    id = post_for_testing[0].id

    res = authorized_client.put(
        f"/posts/{id}", json=data)

    updated_post = schemas.PostResponse(**res.json())

    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert updated_post.published == data["published"]

def test_unauthorized_update_post(client, post_for_testing):
    id = post_for_testing[0].id

    res = client.put(f"/posts/{id}", 
                     json=data)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_other_user_post(authorized_client, 
                                post_for_testing):

    id = post_for_testing[3].id

    res = authorized_client.put(f"/posts/{id}", json=data)

    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_update_non_exist_post(authorized_client):
    res = authorized_client.put("/posts/99999", json=data)

    assert res.status_code == status.HTTP_404_NOT_FOUND

