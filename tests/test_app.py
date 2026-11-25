from src.app import activities


def test_root_redirects_to_static_page(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_participant(client):
    response = client.post(
        "/activities/Basketball%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Signed up student@mergington.edu for Basketball Club"
    )
    assert "student@mergington.edu" in activities["Basketball Club"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Student is already signed up for this activity"
    )


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant(client):
    response = client.request(
        "DELETE",
        "/activities/Chess%20Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Unregistered michael@mergington.edu from Chess Club"
    )
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_rejects_unknown_participant(client):
    response = client.request(
        "DELETE",
        "/activities/Chess%20Club/signup",
        params={"email": "missing@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_unregister_rejects_unknown_activity(client):
    response = client.request(
        "DELETE",
        "/activities/Unknown%20Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_static_assets_are_available(client):
    app_js = client.get("/static/app.js")
    styles = client.get("/static/styles.css")

    assert app_js.status_code == 200
    assert styles.status_code == 200
