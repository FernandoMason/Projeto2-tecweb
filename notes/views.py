from django.shortcuts import get_object_or_404, redirect, render

from .models import Note

ERRO_SEM_TITULO = 'A anotação precisa de um título.'


def index(request):
    """Lista as anotações e cria uma nova quando o formulário é enviado."""
    if request.method == 'POST':
        title = request.POST.get('titulo', '').strip()
        content = request.POST.get('detalhes', '').strip()
        if title:
            Note.objects.create(title=title, content=content)
            return redirect('index')
        erro = ERRO_SEM_TITULO
    else:
        title, content, erro = '', '', None

    return render(request, 'notes/index.html', {
        'notes': Note.objects.all(),
        'titulo': title,
        'detalhes': content,
        'erro': erro,
    })


def edit(request, note_id):
    """Mostra o formulário de edição (GET) e salva as alterações (POST)."""
    note = get_object_or_404(Note, pk=note_id)

    if request.method == 'POST':
        title = request.POST.get('titulo', '').strip()
        content = request.POST.get('detalhes', '').strip()
        if title:
            note.title = title
            note.content = content
            note.save()
            return redirect('index')
        erro = ERRO_SEM_TITULO
    else:
        title, content, erro = note.title, note.content, None

    return render(request, 'notes/edit.html', {
        'note': note,
        'titulo': title,
        'detalhes': content,
        'erro': erro,
    })


def delete(request, note_id):
    """Pede confirmação (GET) e apaga a anotação (POST)."""
    note = get_object_or_404(Note, pk=note_id)

    if request.method == 'POST':
        note.delete()
        return redirect('index')

    return render(request, 'notes/delete.html', {'note': note})
