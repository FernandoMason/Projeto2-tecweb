from django.shortcuts import get_object_or_404, redirect, render

from .models import Note, Tag

# Mesmos limites declarados nos campos do models.py. O Django só valida
# max_length em formulários; como o formulário é escrito à mão, a checagem
# precisa acontecer aqui — senão o PostgreSQL rejeita o INSERT com erro 500.
MAX_TITULO = 200
MAX_TAG = 200

ERRO_SEM_TITULO = 'A anotação precisa de um título.'
ERRO_TITULO_LONGO = f'O título pode ter no máximo {MAX_TITULO} caracteres.'
ERRO_TAG_LONGA = f'Cada tag pode ter no máximo {MAX_TAG} caracteres.'


def separar_nomes_de_tags(texto):
    """Quebra "tag1, tag2, tag3" na lista de nomes, sem vazios nem repetidos."""
    nomes = []
    for nome in (texto or '').split(','):
        nome = nome.strip()
        if nome and nome not in nomes:
            nomes.append(nome)
    return nomes


def validar(titulo, nomes_de_tags):
    """Devolve a mensagem de erro do formulário, ou None se estiver tudo certo."""
    if not titulo:
        return ERRO_SEM_TITULO
    if len(titulo) > MAX_TITULO:
        return ERRO_TITULO_LONGO
    if any(len(nome) > MAX_TAG for nome in nomes_de_tags):
        return ERRO_TAG_LONGA
    return None


def buscar_ou_criar_tags(nomes):
    """Devolve as Tags com esses nomes, criando as que ainda não existirem.

    O get_or_create garante que não haja tags duplicadas no banco: uma tag já
    usada por outra anotação é reaproveitada em vez de duplicada.
    """
    return [Tag.objects.get_or_create(nome=nome)[0] for nome in nomes]


def index(request):
    """Lista as anotações e cria uma nova quando o formulário é enviado."""
    if request.method == 'POST':
        title = request.POST.get('titulo', '').strip()
        content = request.POST.get('detalhes', '').strip()
        texto_tags = request.POST.get('tags', '')
        nomes = separar_nomes_de_tags(texto_tags)
        erro = validar(title, nomes)
        if erro is None:
            note = Note.objects.create(title=title, content=content)
            # set() aceita lista vazia, então anotação sem tag funciona igual.
            note.tags.set(buscar_ou_criar_tags(nomes))
            return redirect('index')
    else:
        title, content, texto_tags, erro = '', '', '', None

    return render(request, 'notes/index.html', {
        'notes': Note.objects.all(),
        'titulo': title,
        'detalhes': content,
        'tags': texto_tags,
        'erro': erro,
    })


def edit(request, note_id):
    """Mostra o formulário de edição (GET) e salva as alterações (POST)."""
    note = get_object_or_404(Note, pk=note_id)

    if request.method == 'POST':
        title = request.POST.get('titulo', '').strip()
        content = request.POST.get('detalhes', '').strip()
        texto_tags = request.POST.get('tags', '')
        nomes = separar_nomes_de_tags(texto_tags)
        erro = validar(title, nomes)
        if erro is None:
            note.title = title
            note.content = content
            note.save()
            # set() substitui a lista inteira: tags digitadas são adicionadas e
            # as que sumiram do campo são desassociadas da anotação.
            note.tags.set(buscar_ou_criar_tags(nomes))
            return redirect('index')
    else:
        title = note.title
        content = note.content
        texto_tags = note.tags_como_texto()
        erro = None

    return render(request, 'notes/edit.html', {
        'note': note,
        'titulo': title,
        'detalhes': content,
        'tags': texto_tags,
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
