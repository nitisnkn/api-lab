import pytest

@pytest.mark.parametrize("excluded", [
    [],                            # 0 tools
    ["Knife"],                     # 1 tool
    ["Scissors"],                  # 1 tool
    ["Knife", "Scissors"]          # 2 tools
])
def test_excluded_tool_is_not_used(api, auth, excluded):
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded

@pytest.mark.xfail(reason="Defect 1: API returns 500 when all tools are excluded instead of 400", strict=True)
def test_exclude_all_tools(api, auth):
    excluded = ["Knife", "Pizza cutter", "Scissors"]
    body = {"excludedTools": excluded}
    res = api.post("/api/pizza", json=body, headers=auth)
    assert res.status_code == 400
    assert "error" in res.json()