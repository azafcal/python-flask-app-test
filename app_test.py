"""
Testes unitários e de integração para a aplicação Flask Todo App.

Este arquivo contém testes abrangentes para:
- Modelo Todo
- Rotas da aplicação
- Operações CRUD
- Cenários de erro
"""

import os
import tempfile
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from app import app, db, Todo


# Fixtures
@pytest.fixture
def client():
    """Cria um cliente de teste com banco de dados temporário."""
    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def sample_todo():
    """Cria uma tarefa de exemplo para uso nos testes."""
    return Todo(content="Tarefa de exemplo", date_created=datetime.utcnow())


# Testes do Modelo Todo
class TestTodoModel:
    """Testes unitários para o modelo Todo."""

    @pytest.mark.unit
    def test_todo_creation(self, client):
        """Testa a criação de uma nova tarefa."""
        with app.app_context():
            todo = Todo(content="Nova tarefa")
            assert todo.content == "Nova tarefa"
            assert todo.id is None  # Ainda não foi salva
            assert isinstance(todo.date_created, datetime)

    @pytest.mark.unit
    def test_todo_repr(self, client):
        """Testa a representação string do modelo Todo."""
        with app.app_context():
            todo = Todo(content="Test task")
            db.session.add(todo)
            db.session.commit()
            assert repr(todo) == f'<Task {todo.id}>'

    @pytest.mark.unit
    def test_todo_database_save(self, client):
        """Testa o salvamento de uma tarefa no banco de dados."""
        with app.app_context():
            todo = Todo(content="Tarefa para salvar")
            db.session.add(todo)
            db.session.commit()
            
            # Verifica se foi salva corretamente
            saved_todo = Todo.query.filter_by(content="Tarefa para salvar").first()
            assert saved_todo is not None
            assert saved_todo.content == "Tarefa para salvar"
            assert saved_todo.id is not None


# Testes das Rotas
class TestRoutes:
    """Testes para as rotas da aplicação."""

    @pytest.mark.integration
    def test_index_get_empty(self, client):
        """Testa a rota GET / sem tarefas."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'<html' in response.data.lower()

    @pytest.mark.integration
    def test_index_get_with_tasks(self, client):
        """Testa a rota GET / com tarefas existentes."""
        # Adiciona uma tarefa primeiro
        with app.app_context():
            todo = Todo(content="Tarefa existente")
            db.session.add(todo)
            db.session.commit()
        
        response = client.get('/')
        assert response.status_code == 200
        assert b'Tarefa existente' in response.data

    @pytest.mark.integration
    def test_index_post_valid_data(self, client):
        """Testa a criação de tarefa via POST com dados válidos."""
        response = client.post('/', data={'content': 'Nova tarefa via POST'}, follow_redirects=True)
        assert response.status_code == 200
        
        # Verifica se a tarefa foi criada no banco
        with app.app_context():
            task = Todo.query.filter_by(content='Nova tarefa via POST').first()
            assert task is not None

    @pytest.mark.integration
    def test_index_post_empty_content(self, client):
        """Testa POST com conteúdo vazio."""
        response = client.post('/', data={'content': ''}, follow_redirects=True)
        assert response.status_code == 200
        
        # Verifica se a tarefa vazia foi criada (comportamento atual da app)
        with app.app_context():
            task = Todo.query.filter_by(content='').first()
            assert task is not None

    @pytest.mark.integration
    def test_delete_existing_task(self, client):
        """Testa a exclusão de uma tarefa existente."""
        # Cria uma tarefa primeiro
        with app.app_context():
            todo = Todo(content="Tarefa para deletar")
            db.session.add(todo)
            db.session.commit()
            task_id = todo.id
        
        # Deleta a tarefa
        response = client.get(f'/delete/{task_id}', follow_redirects=True)
        assert response.status_code == 200
        
        # Verifica se foi deletada
        with app.app_context():
            deleted_task = Todo.query.get(task_id)
            assert deleted_task is None

    @pytest.mark.integration
    def test_delete_nonexistent_task(self, client):
        """Testa a exclusão de uma tarefa que não existe."""
        response = client.get('/delete/9999')
        assert response.status_code == 404

    @pytest.mark.integration
    def test_update_get_existing_task(self, client):
        """Testa a rota GET /update/<id> para tarefa existente."""
        # Cria uma tarefa primeiro
        with app.app_context():
            todo = Todo(content="Tarefa original")
            db.session.add(todo)
            db.session.commit()
            task_id = todo.id
        
        response = client.get(f'/update/{task_id}')
        assert response.status_code == 200
        assert b'Tarefa original' in response.data

    @pytest.mark.integration
    def test_update_get_nonexistent_task(self, client):
        """Testa a rota GET /update/<id> para tarefa inexistente."""
        response = client.get('/update/9999')
        assert response.status_code == 404

    @pytest.mark.integration
    def test_update_post_existing_task(self, client):
        """Testa a atualização de uma tarefa via POST."""
        # Cria uma tarefa primeiro
        with app.app_context():
            todo = Todo(content="Tarefa original")
            db.session.add(todo)
            db.session.commit()
            task_id = todo.id
        
        # Atualiza a tarefa
        response = client.post(f'/update/{task_id}', 
                             data={'content': 'Tarefa atualizada'}, 
                             follow_redirects=True)
        assert response.status_code == 200
        
        # Verifica se foi atualizada
        with app.app_context():
            updated_task = Todo.query.get(task_id)
            assert updated_task.content == 'Tarefa atualizada'

    @pytest.mark.integration
    def test_update_post_nonexistent_task(self, client):
        """Testa a atualização de uma tarefa inexistente."""
        response = client.post('/update/9999', data={'content': 'Nova tarefa'})
        assert response.status_code == 404


# Testes de Cenários de Erro
class TestErrorScenarios:
    """Testes para cenários de erro e situações excepcionais."""

    @pytest.mark.integration
    @patch('app.db.session.add')
    @patch('app.db.session.commit')
    def test_index_post_database_error(self, mock_commit, mock_add, client):
        """Testa erro de banco de dados ao criar tarefa."""
        mock_commit.side_effect = Exception("Database error")
        
        response = client.post('/', data={'content': 'Test task'})
        assert response.status_code == 200
        assert b'There was an issue adding your task' in response.data

    @pytest.mark.integration
    @patch('app.db.session.delete')
    @patch('app.db.session.commit')
    def test_delete_database_error(self, mock_commit, mock_delete, client):
        """Testa erro de banco de dados ao deletar tarefa."""
        # Cria uma tarefa primeiro
        with app.app_context():
            todo = Todo(content="Tarefa para erro")
            db.session.add(todo)
            db.session.commit()
            task_id = todo.id
        
        mock_commit.side_effect = Exception("Database error")
        
        response = client.get(f'/delete/{task_id}')
        assert response.status_code == 200
        assert b'There was a problem deleting that task' in response.data

    @pytest.mark.integration
    @patch('app.db.session.commit')
    def test_update_database_error(self, mock_commit, client):
        """Testa erro de banco de dados ao atualizar tarefa."""
        # Cria uma tarefa primeiro
        with app.app_context():
            todo = Todo(content="Tarefa para erro")
            db.session.add(todo)
            db.session.commit()
            task_id = todo.id
        
        mock_commit.side_effect = Exception("Database error")
        
        response = client.post(f'/update/{task_id}', data={'content': 'Conteúdo atualizado'})
        assert response.status_code == 200
        assert b'There was an issue updating your task' in response.data


# Testes de Performance e Carga
class TestPerformance:
    """Testes de performance básicos."""

    @pytest.mark.slow
    def test_multiple_tasks_creation(self, client):
        """Testa a criação de múltiplas tarefas."""
        num_tasks = 100
        
        for i in range(num_tasks):
            response = client.post('/', data={'content': f'Tarefa {i}'}, follow_redirects=True)
            assert response.status_code == 200
        
        # Verifica se todas foram criadas
        with app.app_context():
            count = Todo.query.count()
            assert count == num_tasks

    @pytest.mark.integration
    def test_task_ordering(self, client):
        """Testa se as tarefas são ordenadas por data de criação."""
        tasks_content = ['Primeira', 'Segunda', 'Terceira']
        
        # Cria tarefas em sequência
        for content in tasks_content:
            client.post('/', data={'content': content}, follow_redirects=True)
        
        # Verifica a ordem na página
        response = client.get('/')
        response_text = response.data.decode('utf-8')
        
        # Verifica se aparecem na ordem correta
        primeira_pos = response_text.find('Primeira')
        segunda_pos = response_text.find('Segunda')
        terceira_pos = response_text.find('Terceira')
        
        assert primeira_pos < segunda_pos < terceira_pos

