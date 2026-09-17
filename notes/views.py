from django.shortcuts import get_object_or_404, redirect, render

from .models import Note, Tag

# Mesmos limites declarados nos campos do models.py. O Django só valida
# max_length em formulários; como o formulário é escrito à mão, a checagem
# precisa acontecer aqui — senão o PostgreSQL rejeita o INSERT com erro 500.
MAX_TITULO = 200
MAX_TAG = 200

ERRO_SEM_TITULO = 'A anotação precisa de um título.'
ERRO_TITULO_LONGO = f'O título pode ter no máximo {MAX_TITULO} caracteres.'
ERRO_TAG_LONGA = f'A tag pode ter no máximo {MAX_TAG} caracteres.'


def validar(titulo, tag_nome):
    """Devolve a mensagem de erro do formulário, ou None se estiver tudo certo."""
    if not titulo:
        return ERRO_SEM_TITULO
    if len(titulo) > MAX_TITULO:
        return ERRO_TITULO_LONGO
    if len(tag_nome.strip()) > MAX_TAG:
        return ERRO_TAG_LONGA
    return None


def buscar_ou_criar_tag(nome):
    """Devolve a Tag com esse nome, criando-a se ainda não existir.

    Campo vazio significa "anotação sem tag", então devolve None.
    O get_or_create garante que não haja tags duplicadas no banco.
    """
    nome = (nome or '').strip()
    if not nome:
        return None
    tag, _ = Tag.objects.get_or_create(nome=nome)
    return tag


def index(request):
    """Lista as anotações e cria uma nova quando o formulário é enviado."""
    if request.method == 'POST':
        title = request.POST.get('titulo', '').strip()
        content = request.POST.get('detalhes', '').strip()
        tag_nome = request.POST.get('tag', '')
        erro = validar(title, tag_nome)
        if erro is None:
            Note.objects.create(
                title=title,
                content=content,
                tag=buscar_ou_criar_tag(tag_nome),
            )
            return redirect('index')
    else:
        title, content, tag_nome, erro = '', '', '', None

    return render(request, 'notes/index.html', {
        'notes': Note.objects.all(),
        'titulo': title,
        'detalhes': content,
        'tag': tag_nome,
        'erro': erro,
    })


def edit(request, note_id):
    """Mostra o formulário de edição (GET) e salva as alterações (POST)."""
    note = get_object_or_404(Note, pk=note_id)

    if request.method == 'POST':
        title = request.POST.get('titulo', '').strip()
        content = request.POST.get('detalhes', '').strip()
        tag_nome = request.POST.get('tag', '')
        erro = validar(title, tag_nome)
        if erro is None:
            note.title = title
            note.content = content
            # Campo de tag em branco remove a tag da anotação.
            note.tag = buscar_ou_criar_tag(tag_nome)
            note.save()
            return redirect('index')
    else:
        title = note.title
        content = note.content
        tag_nome = note.tag.nome if note.tag else ''
        erro = None

    return render(request, 'notes/edit.html', {
        'note': note,
        'titulo': title,
        'detalhes': content,
        'tag': tag_nome,
        'erro': erro,
    })


def delete(request, note_id):
    """Pede confirmação (GET) e apaga a anotação (POST)."""
    note = get_object_or_404(Note, pk=note_id)

    if request.method == 'POST':
        note.delete()
        return redirect('index')

    return render(request, 'notes/delete.html', {'note': note})


def tags(request):
    """Lista os nomes de todas as tags cadastradas."""
    return render(request, 'notes/tags.html', {'tags': Tag.objects.all()})


def tag_detail(request, tag_id):
    """Mostra todas as anotações associadas a uma tag."""
    tag = get_object_or_404(Tag, pk=tag_id)
    return render(request, 'notes/tag_detail.html', {
        'tag': tag,
        'notes': tag.note_set.all(),
    })
