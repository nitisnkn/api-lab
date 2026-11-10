import uuid
import pytest

def test_user_already_taken(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    res1 = api.post("/api/users", json=user)
    assert res1.status_code == 201
    
    # Try to create the same user again
    res2 = api.post("/api/users", json=user)
    assert res2.status_code == 400
    assert res2.json() == {"error": "username already taken"}

def test_login_wrong_password(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    api.post("/api/users", json=user)
    
    # Try to log in with wrong password
    wrong_user = {"username": name, "password": "wrong-password"}
    res = api.post("/api/users/token/login", json=wrong_user)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}

def test_user_empty_name(api):
    user = {"username": "", "password": "Pizza-2026"}
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}