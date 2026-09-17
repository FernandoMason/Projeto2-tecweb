# tecweb-2026-2-projeto1B

Projeto 1B de Tecnologias Web (Insper, 2026/2) — reimplementação do **Get-it**
usando o framework Django, seguindo o handout da Aula 04 e as tarefas do
Projeto 1B.

## 🚀 Aplicação publicada

**https://getit-1yem.onrender.com**

> Hospedada no Render (plano gratuito). O serviço hiberna depois de um tempo sem
> acesso, então o **primeiro carregamento pode levar cerca de um minuto**.

- Projeto Django: `getit`
- App: `notes`
- Banco de dados: **PostgreSQL** (em container Docker no ambiente local, e
  gerenciado pelo Render em produção)

## Funcionalidades

- **CRUD de anotações** — criar, listar, editar e apagar (Tarefa 01)
- **Sistema de tags** — cada anotação pode ter **várias** tags, e cada tag pode
  estar em várias anotações (relação *many-to-many*, Tarefa 02 + extra)
- **Página de tags** em `/tags/` e as anotações de cada tag em `/tags/<id>/`
- **Django Admin** em `/admin/`

## Como rodar

### 1. Subir o banco de dados

O PostgreSQL roda em um container Docker. Com o Docker Desktop aberto:

```bash
docker compose up -d
```

Para conferir se está no ar:

```bash
docker compose ps
```

Para parar (os dados continuam no volume `pg-docker-data`):

```bash
docker compose down
```

### 2. Rodar a aplicação

```bash
# ativar o ambiente virtual
env\Scripts\activate        # Windows (PowerShell/cmd)
source env/bin/activate     # Linux / macOS

# instalar dependências
python -m pip install -r requirements.txt

# criar as tabelas
python manage.py migrate

# carregar as anotações de exemplo (opcional)
python manage.py loaddata dados-iniciais.json

# subir o servidor
python manage.py runserver
```

- Aplicação: http://localhost:8000
- Django Admin: http://localhost:8000/admin/

## Banco de dados

| | |
|---|---|
| Banco | `getit` |
| Usuário | `getituser` |
| Senha | `getitsenha` |
| Host / porta | `localhost:5432` |

Esses são os valores padrão de desenvolvimento, definidos em
[`docker-compose.yml`](docker-compose.yml). O `settings.py` lê cada um de uma
variável de ambiente (`POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`,
`POSTGRES_HOST`, `POSTGRES_PORT`) e só usa o padrão quando a variável não
existe — é assim que o ambiente de produção aponta para outro banco sem
precisar alterar o código.

> O `db.sqlite3` na raiz é o banco antigo, de antes da Tarefa 03. Não é mais
> usado pela aplicação; ficou no repositório apenas como histórico.

## Superusuário

Um superusuário local já foi criado para testes: `admin` / `admin123`.
**Troque a senha** (`python manage.py changepassword admin`) ou crie o seu:

```bash
python manage.py createsuperuser
```

## Estrutura

```
manage.py
docker-compose.yml         # PostgreSQL em container
dados-iniciais.json        # anotações de exemplo (dumpdata)
getit/                     # configurações do projeto
    settings.py            # INSTALLED_APPS, DATABASES (PostgreSQL)
    urls.py                # rota '' -> notes.urls ; rota 'admin/'
notes/                     # app das anotações
    models.py              # Note (title, content, tags) e Tag (nome)
    views.py               # index, edit, delete, tags, tag_detail
    urls.py                # rotas da aplicação
    admin.py               # registra Note e Tag no Django Admin
    migrations/
        0001_initial.py            # modelo Note
        0002_tag_note_tag.py       # Tag + relação many-to-one
        0003_remove_note_tag_note_tags.py  # migra para many-to-many
    templates/notes/
        base.html          # layout comum (appbar, CSS, JS)
        index.html         # formulário + lista de anotações
        edit.html          # edição de uma anotação
        delete.html        # confirmação de exclusão
        tags.html          # lista de tags
        tag_detail.html    # anotações de uma tag
    static/notes/
        getit.css          # estilo reaproveitado do Projeto 1A
        getit.js
        img/logo-getit.png
```

## Rotas

| Rota | O que faz |
|---|---|
| `/` | lista as anotações e cria novas (POST) |
| `/<id>/edit/` | edita uma anotação |
| `/<id>/delete/` | confirma e apaga uma anotação |
| `/tags/` | lista todas as tags |
| `/tags/<id>/` | anotações de uma tag |
| `/admin/` | Django Admin |
