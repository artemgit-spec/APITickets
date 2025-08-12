import pytest


@pytest.mark.parametrize("auth_token, id, status, answer",[
                         ('admin', 11, 200, {"title": "string","text_ticket": "string","is_active": "active"}),
                         ('admin', 100, 404, {"detail": "Нет такого тикета"}),
                         ('user', 11, 200, {"title": "string","text_ticket": "string","is_active": "active"}),
                         ('user', 100, 404, {"detail": "Нет такого тикета"})],
                         indirect=['auth_token'])
def test_id_user(auth_token, id, status, answer, client):
  resp = client.get(f'/tickets/info-tickte/{id}', headers={"Authorization": auth_token})
  assert resp.status_code == status
  assert resp.json() == answer

@pytest.mark.parametrize('auth_token',[
                          ('admin'),
                          ('user')],
                         indirect=['auth_token'])
def test_create(client, auth_token):
  resp = client.post('/tickets/create', 
                     headers={"Authorization": auth_token},
                     json={"title":"aaa","text_ticket": "aaaaa","creating_ticket":"2025-06-25T10:39:51.113000"}) 
  assert resp.status_code == 201
  assert resp.json() == {'detail':"Тикет создан"}

@pytest.mark.parametrize("auth_token, id, data, status, answer",[
                         ("admin", 1,{"title": "stringaaa","text_ticket": "strinsssg"}, 200, {"status_code": 200,"detail": 'Изменено название и текст тикета'}),
                         ("admin", 100,{"title": "string","text_ticket": "string"}, 404, {"detail":'Нет такого тикета'}),
                         ("admin", 2, {"title": "strina","text_ticket": "string"}, 200, {"status_code": 200,"detail": "Изменено название тикета"}),
                         ("admin", 3, {"title": "string","text_ticket": "strindddg"}, 200, {"status_code": 200,"detail": "Изменено содержание тикета"}),
                         ("admin", 5, {"title": "string","text_ticket": "string"}, 200, {"status_code": 200,"detail": 'Информация не была обновлена'} ),
                         ("user", 1, {"title": "string","text_ticket": "string"}, 200, {"status_code":403,"detail":"Не достаточно прав"})],
                         indirect=['auth_token'])  
def test_update_info(auth_token, id, data, status, answer, client):
  resp = client.patch(f'/tickets/update-info/{id}',
                      json=data,
                      headers={"Authorization": auth_token})
  assert resp.status_code == status
  assert resp.json() == answer


  

@pytest.mark.parametrize("auth_token, id, status_tic, status, answer",[
                          ("admin", 6, "active", 200, {"status_code": 200,"detail": "Тикет обновлен"}),
                          ("admin", 7,"not active", 200,{"status_code": 200,"detail": "Тикет обновлен"}),
                          ("user", 8, "not active", 200, {"status_code": 200,"detail": "Тикет обновлен"}),
                          ("user", 9,"active", 400,{"detail": "Закрытый тикет уже нельзя открыть"})],
                         indirect=['auth_token'])
def test_update_status(auth_token, id, status_tic, status, answer, client):
  resp = client.patch(f"/tickets/update-status/{id}",
                      params = {"new_status": status_tic},
                      headers={"Authorization": auth_token})
  assert resp.status_code == status
  assert resp.json() == answer


@pytest.mark.parametrize('auth_token, id, status, answer',[
                        ("admin", 1, 200, {"status_code": 200,'detail':'Тикет удален'}),
                        ("user", 2, 200, {"status_code": 403,"detail": "Не достаточно прав"})],
                         indirect=["auth_token"])
def test_delete_ticket(auth_token, id, status, answer, client):
  resp = client.delete(f"/tickets/delete/{id}",
                       headers={'Authorization':auth_token})
  assert resp.status_code == status
  assert resp.json() == answer
