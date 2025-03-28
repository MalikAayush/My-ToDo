import pytest
from app import app, db, User, Todo

@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
    app.config['SQLALCHEMY_BINDS'] = {'login': 'sqlite:///test_login.db'}
    app.config['WTF_CSRF_ENABLED'] = False  
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  
        yield client
        with app.app_context():
            db.drop_all()  

def test_home_route(client):
    """Test the home route for unauthorized access."""
    response = client.get('/')
    assert response.status_code == 302  

def test_register_user(client):
    """Test user registration functionality."""
    response = client.post('/register', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Account created successfully!" in response.data

def test_login_user(client):
    """Test user login functionality."""
    
    client.post('/register', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    
    response = client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Todo App" in response.data  

def test_add_todo(client):
    """Test adding a todo item."""
    
    client.post('/register', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    
    response = client.post('/', data={
        'title': 'Test Todo',
        'desc': 'This is a test todo description.'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Todo" in response.data

def test_update_todo(client):
    """Test updating a todo item."""
    
    client.post('/register', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    
    client.post('/', data={
        'title': 'Test Todo',
        'desc': 'This is a test todo description.'
    }, follow_redirects=True)

    
    todo = Todo.query.first()
    response = client.post(f'/update/{todo.SNo}', data={
        'title': 'Updated Todo',
        'desc': 'Updated description.'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Updated Todo" in response.data

def test_delete_todo(client):
    """Test deleting a todo item."""
    
    client.post('/register', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    client.post('/login', data={
        'email': 'testuser@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    
    client.post('/', data={
        'title': 'Test Todo',
        'desc': 'This is a test todo description.'
    }, follow_redirects=True)

    todo = Todo.query.first()
    
    response = client.get(f'/delete/{todo.SNo}', follow_redirects=True)
    
    assert response.status_code == 200
