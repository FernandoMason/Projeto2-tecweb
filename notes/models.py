from django.db import models


class TagManager(models.Manager):
    """Permite localizar uma Tag pelo nome em vez da chave primária."""

    def get_by_natural_key(self, nome):
        return self.get(nome=nome)


class Tag(models.Model):
    nome = models.CharField(max_length=200, unique=True)

    objects = TagManager()

    def __str__(self):
        return self.nome

    def natural_key(self):
        """Identifica a tag pelo nome nos fixtures.

        Sem isso o dumpdata grava a chave primária, que não é a mesma em
        bancos diferentes: carregar o fixture em um banco onde a tag já
        existe com outro id quebra a restrição de nome único.
        """
        return (self.nome,)


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'{self.id}. {self.title}'

    def tags_como_texto(self):
        """Tags da anotação no mesmo formato aceito pelo formulário."""
        return ', '.join(tag.nome for tag in self.tags.all())
