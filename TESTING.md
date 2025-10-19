# Guia de Testes - Flask Todo App

Este documento explica como executar e entender os testes unitários e de integração da aplicação Flask Todo.

## 📋 Índice

- [Instalação das Dependências](#instalação-das-dependências)
- [Estrutura dos Testes](#estrutura-dos-testes)
- [Como Executar os Testes](#como-executar-os-testes)
- [Tipos de Teste](#tipos-de-teste)
- [Cobertura de Código](#cobertura-de-código)
- [Interpretando os Resultados](#interpretando-os-resultados)

## 🚀 Instalação das Dependências

Primeiro, instale todas as dependências necessárias:

```bash
pip install -r requirements.txt
```

## 📁 Estrutura dos Testes

```
python-flask-app-test/
├── app.py              # Aplicação principal
├── app_test.py         # Arquivo principal de testes
├── run_tests.py        # Script para executar testes
├── pytest.ini         # Configuração do pytest
├── requirements.txt    # Dependências (incluindo pytest)
└── TESTING.md         # Este documento
```

## 🧪 Como Executar os Testes

### Opção 1: Usando o script personalizado (Recomendado)

```bash
# Executar todos os testes
python run_tests.py --all

# Executar apenas testes unitários
python run_tests.py --unit

# Executar apenas testes de integração
python run_tests.py --integration

# Executar com relatório de cobertura
python run_tests.py --coverage

# Executar com saída detalhada
python run_tests.py --verbose

# Incluir testes lentos
python run_tests.py --slow
```

### Opção 2: Usando pytest diretamente

```bash
# Todos os testes
pytest app_test.py

# Testes com verbose
pytest -v app_test.py

# Apenas testes unitários
pytest -m unit app_test.py

# Apenas testes de integração
pytest -m integration app_test.py

# Testes com cobertura
pytest --cov=app --cov-report=html app_test.py
```

## 🎯 Tipos de Teste

### 1. Testes Unitários (`@pytest.mark.unit`)

Testam componentes individuais isoladamente:

- **TestTodoModel**: Testa o modelo Todo
  - `test_todo_creation()`: Criação de instâncias
  - `test_todo_repr()`: Representação string
  - `test_todo_database_save()`: Salvamento no banco

### 2. Testes de Integração (`@pytest.mark.integration`)

Testam a interação entre componentes:

- **TestRoutes**: Testa as rotas da aplicação
  - `test_index_get_empty()`: Página inicial vazia
  - `test_index_get_with_tasks()`: Página com tarefas
  - `test_index_post_valid_data()`: Criação via POST
  - `test_delete_existing_task()`: Exclusão de tarefa
  - `test_update_post_existing_task()`: Atualização de tarefa

### 3. Testes de Erro (`TestErrorScenarios`)

Testam cenários de falha:

- `test_index_post_database_error()`: Erro ao criar tarefa
- `test_delete_database_error()`: Erro ao deletar tarefa
- `test_update_database_error()`: Erro ao atualizar tarefa

### 4. Testes de Performance (`@pytest.mark.slow`)

Testam performance e comportamento em larga escala:

- `test_multiple_tasks_creation()`: Criação de 100 tarefas
- `test_task_ordering()`: Verificação de ordenação

## 📊 Cobertura de Código

Para gerar relatório de cobertura:

```bash
python run_tests.py --coverage
```

Isso gerará:
- Relatório no terminal mostrando linhas não cobertas
- Arquivo HTML em `htmlcov/index.html` para visualização detalhada

### Interpretando a Cobertura

- **Verde**: Linhas cobertas pelos testes
- **Vermelho**: Linhas não cobertas
- **Amarelo**: Linhas parcialmente cobertas

## 🔍 Interpretando os Resultados

### Exemplo de Saída Bem-Sucedida

```
=================== test session starts ===================
collected 15 items

app_test.py::TestTodoModel::test_todo_creation PASSED     [ 6%]
app_test.py::TestTodoModel::test_todo_repr PASSED         [13%]
app_test.py::TestRoutes::test_index_get_empty PASSED      [20%]
...
=================== 15 passed in 2.34s ===================
```

### Exemplo de Falha

```
=================== FAILURES ===================
____ TestTodoModel.test_todo_creation ____

    def test_todo_creation(self, client):
>       assert todo.content == "Nova tarefa"
E       AssertionError: assert None == "Nova tarefa"

app_test.py:52: AssertionError
```

## 🎛️ Fixtures Utilizadas

### `client`
- Cria um cliente de teste com banco de dados temporário
- Limpa automaticamente após cada teste
- Usado em praticamente todos os testes

### `sample_todo`
- Cria uma tarefa de exemplo para reutilização
- Útil para testes que precisam de dados pré-definidos

## 🚨 Mocks e Simulações

Os testes usam `unittest.mock` para simular:

- **Falhas de banco de dados**: Simulando exceções nas operações
- **Isolamento**: Testando componentes sem dependências externas

Exemplo:
```python
@patch('app.db.session.commit')
def test_database_error(self, mock_commit, client):
    mock_commit.side_effect = Exception("Database error")
    # Teste continua...
```

## 🔧 Configuração Personalizada

### pytest.ini

Configurações globais do pytest:

```ini
[tool:pytest]
testpaths = .
python_files = *_test.py test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
```

## 📈 Melhores Práticas Implementadas

1. **Isolamento**: Cada teste usa um banco de dados limpo
2. **Nomenclatura clara**: Nomes de teste descritivos
3. **Documentação**: Docstrings explicando o propósito
4. **Organização**: Testes agrupados em classes por funcionalidade
5. **Marcadores**: Separação entre unit, integration e slow tests
6. **Cleanup**: Limpeza automática de recursos

## 🆘 Troubleshooting

### Erro: "No module named 'app'"

```bash
# Certifique-se de estar no diretório correto
cd /home/azaf/testing/python/python-flask-app-test
python -m pytest app_test.py
```

### Erro: "Database locked"

```bash
# Remova arquivos de banco temporários
rm -f test.db*
rm -f *.db*
```

### Erro: Dependências não encontradas

```bash
# Reinstale as dependências
pip install -r requirements.txt
```

## 🎯 Próximos Passos

Para melhorar ainda mais os testes:

1. **Testes de API**: Testar endpoints JSON se existirem
2. **Testes de Segurança**: Verificar proteções CSRF, XSS
3. **Testes de Carga**: Usar ferramentas como locust
4. **Testes E2E**: Selenium para testes de interface
5. **CI/CD**: Integração com GitHub Actions

---

**💡 Dica**: Execute `python run_tests.py --coverage` regularmente para manter boa cobertura de testes!