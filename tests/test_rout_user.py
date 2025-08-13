import pytest


def test_create_user(client):
    resp = client.post(
        "/users/reg-user",
        json={
            "name": "user2",
            "password": "user2",
            "mail_user": "user2@example.com",
            "is_admin": "user",
        },
    )
    assert resp.status_code == 200
    assert resp.json() == {"status_code": 201, "detail": "Пользователь создан"}


@pytest.mark.parametrize(
    "auth_token, id, status, answer",
    [
        (
            "admin",
            1,
            200,
            {
                "id": 1,
                "name": "admin",
                "is_admin": "admin",
                "mail_users": "user@example.com",
            },
        ),
        ("admin", 100, 404, {"detail": "Нет такого пользователя"}),
        (
            "user",
            2,
            200,
            {
                "id": 2,
                "name": "user",
                "is_admin": "user",
                "mail_users": "user@example.com",
            },
        ),
        ("user", 100, 401, {"detail": "Не достаточно прав"}),
    ],
    indirect=["auth_token"],
)
def test_info_user(auth_token, id, status, answer, client):
    resp = client.get(f"/users/info-user/{id}", headers={"Authorization": auth_token})
    assert resp.status_code == status
    assert resp.json() == answer


@pytest.mark.parametrize(
    "auth_token, id, new_status, status, answer",
    [
        ("admin", 2, "admin", 200, {"status_code": 200, "detail": "Статус изменен"}),
        ("admin", 100, "admin", 404, {"detail": "Нет такого пользователя"}),
    ],
    indirect=["auth_token"],
)
def test_update_status(auth_token, id, new_status, status, answer, client):
    resp = client.patch(
        f"/users/update-status-user/{id}",
        params={"new_status": new_status},
        headers={"Authorization": auth_token},
    )
    assert resp.status_code == status
    assert resp.json() == answer
