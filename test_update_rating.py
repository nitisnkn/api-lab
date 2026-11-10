import pytest

@pytest.mark.parametrize("stars, expected_status", [
    (0, 400),
    (1, 200),
    (5, 200),
    (6, 400)
])
def test_update_boundaries(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected_status
    
    # อ่านเรตติ้งกลับมาตรวจสอบว่าถูกอัปเดต หรือคงค่าเดิมไว้
    res_get = api.get(path, headers=auth)
    assert res_get.status_code == 200
    
    if expected_status == 200:
        assert res_get.json()["stars"] == stars
    else:
        # ถ้า Update ถูกปฏิเสธ (400) ค่าดาวต้องเท่ากับค่าเริ่มต้น (3 ดาว)
        assert res_get.json()["stars"] == rating["stars"]