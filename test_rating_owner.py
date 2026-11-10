def test_other_user_read(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.get(path, headers=other_auth)
    print(f"\nRead attempt status: {res.status_code}")
    assert 400 <= res.status_code <= 499

def test_other_user_update(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 4}, headers=other_auth)
    print(f"Update attempt status: {res.status_code}")
    assert 400 <= res.status_code <= 499
    
    check = api.get(path, headers=auth)
    assert check.json()["stars"] == rating["stars"]

def test_other_user_delete(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.delete(path, headers=other_auth)
    print(f"Delete attempt status: {res.status_code}")
    assert 400 <= res.status_code <= 499
    
    check = api.get(path, headers=auth)
    assert check.status_code == 200