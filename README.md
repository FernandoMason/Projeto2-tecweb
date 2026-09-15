# tecweb-2026-2-projeto1B

Projeto 1B de Tecnologias Web (Insper, 2026/2) — reimplementação do **Get-it**
usando o framework Django, seguindo o handout da Aula 04.

- Projeto Django: `getit`
- App: `notes`

## Como rodar

```bash
# 1. ativar o ambiente virtual
env\Scripts\activate        # Windows (PowerShell/cmd)
source env/bin/activate     # Linux / macOS

# 2. instalar dependências (se o env for novo)
python -m pip install -r requirements.txt

# 3. aplicar as migrações
python manage.py migrate

# 4. subir o servidor
python manage.py runserver
```

- Aplicação: http://localhost:8000
- Django Admin: http://localhost:8000/admin/

## Superusuário

Um superusuário local já foi criado para testes: `admin` / `admin123`.
**Troque a senha** (`python manage.py changepassword admin`) ou crie o seu:

```bash
python manage.py createsuperuser
```

## Estrutura

```
manage.py
getit/                     # configurações do projeto
    settings.py            # INSTALLED_APPS inclui notes.apps.NotesConfig
    urls.py                # rota '' -> notes.urls ; rota 'admin/'
notes/                     # app das anotações
    models.py              # modelo Note (title, content, __str__)
    views.py               # view index: GET lista, POST cria
    urls.py                # rota '' -> views.index (name='index')
    admin.py               # registra Note no Django Admin
    migrations/
    templates/notes/
        base.html          # layout comum (appbar, CSS, JS)
        index.html         # formulário + lista de anotações
    static/notes/
        getit.css          # estilo reaproveitado do Projeto 1A
        getit.js
        img/logo-getit.png
```

## Próximos passos

Implementar as funcionalidades de **editar** e **deletar** anotações.
