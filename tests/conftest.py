import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from db_management.db import Base, User, Ticket, session_db
from core.security import get_hash_pass


TEST_BASE = 'sqlite:///test.db'


@pytest.fixture(scope='session')
def test_db():
    engine = create_engine(TEST_BASE, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    
@pytest.fixture
def test_session(test_db):
    TestSession = sessionmaker(bind=test_db)
    session = TestSession()
    
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    
    admin = User(name='admin', password=get_hash_pass('admin'), mail_users="user@example.com", is_admin='admin')
    user = User(name='user', password=get_hash_pass('user'), mail_users='user@example.com', is_admin='user')
    session.add_all([admin, user])
    session.commit()
    
    ticket1 = Ticket(title='string', text_ticket='string', id_user=admin.id)
    ticket2 = Ticket(title='string', text_ticket='string', id_user=admin.id)
    ticket3 = Ticket(title='string', text_ticket='string', id_user=admin.id)
    ticket4 = Ticket(title='string', text_ticket='string', id_user=admin.id)
    ticket5 = Ticket(title='string', text_ticket='string', id_user=admin.id)
    ticket6 = Ticket(title='string', text_ticket='string', id_user=admin.id)
    ticket7 = Ticket(title='string', text_ticket='string', id_user=admin.id)
    ticket8 = Ticket(title='string', text_ticket='string', id_user=admin.id)
    ticket9 = Ticket(title='string', text_ticket='string', is_active = "not active", id_user=admin.id)
    ticket10 = Ticket(title='string', text_ticket='string', id_user=admin.id)
    ticket11 = Ticket(title='string', text_ticket='string', id_user=admin.id)
    session.add_all([ticket1,ticket2,ticket3,ticket4,ticket5,ticket6,ticket7,ticket8,ticket9,ticket10,ticket11])
    session.commit()
    
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def client(test_session):
    def override_get_db():
        try:
            yield test_session
        finally:
            test_session.close()
    app.dependency_overrides[session_db] = override_get_db
    with TestClient(app) as c:
        yield c


users = {
    'admin':{'username':"admin", 'password':'admin'},
    'user':{'username':"user", 'password':'user'}
}

@pytest.fixture
def auth_token(client, request):
    creds = users[request.param]
    response = client.post(f'/token', data=creds)
    assert response.status_code == 200
    token = response.json().get('access_token')
    return f'Bearer {token}'

"""@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_db(scope='module'):
    engine = create_engine('sqlite:///test.db')
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    
@pytest.fixture
def test_session(test_db):
    Session = sessionmaker(bind=test_db)
    session = Session()
    yield session
    session.rollback()
    session.close()
"""