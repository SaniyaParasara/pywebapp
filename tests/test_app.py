from app import app

def test_healthz_ok():
    client = app.test_client()
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.get_json().get("status") == "ok"

def test_home_ok():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    assert "Python WebApp" in res.get_data(as_text=True)
