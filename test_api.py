import requests

def test_my_pizza():
    response = requests.get('https://quickpizza.grafana.com/api/names')
    assert response.status_code == 200

    names = response.json().get('names')
    assert len(names) == 18

    assert "Margherita" in names