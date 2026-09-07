import pytest
from fastapi import status
from .conftest import post_for_testing

#----------TESTING ADD VOTE--------

def test_authorized_add_vote(authorized_client, add_vote_data):

    res = authorized_client.post(f"/vote", json=add_vote_data)

    assert res.status_code == 201

def test_unauthorized_add_vote(client, add_vote_data):

    res = client.post(f"/vote", json=add_vote_data)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED

def test_vote_non_existing_post(authorized_client):
    vote_data = {
    "post_id": 999999,
    "dir": 1
}
    res = authorized_client.post(f"/vote", json=vote_data)

    assert res.status_code == status.HTTP_404_NOT_FOUND

def test_double_vote(authorized_client, vote_for_testing, add_vote_data):

    res =  authorized_client.post("/vote/", json=add_vote_data)

    #the (add_vote_data) uses the same post id with 
    #(vote_for_testing) this is why its double vote


    assert res.status_code == status.HTTP_409_CONFLICT


#----------TESTING DELETE VOTE--------

def test_authorized_delete_vote(authorized_client, vote_for_testing, delete_vote_data):
    res = authorized_client.post("/vote/", json=delete_vote_data)

    assert res.status_code == status.HTTP_201_CREATED

#we dont need test unauthorized delete vote because if u cant
#vote without auth so you cant unvote also bc they are in the
#same HTTP operation

def test_delete_non_exist_vote(authorized_client, delete_vote_data):
    res = authorized_client.post("/vote/", json=delete_vote_data)

    assert res.status_code == status.HTTP_404_NOT_FOUND


