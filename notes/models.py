from django.db import models


class Tag(models.Model):
    nome = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nome


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'{self.id}. {self.title}'

    def tags_como_texto(self):
        """Tags da anotação no mesmo formato aceito pelo formulário."""
        return ', '.join(tag.nome for tag in self.tags.all())
