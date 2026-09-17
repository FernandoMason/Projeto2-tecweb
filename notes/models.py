from django.db import models


class Tag(models.Model):
    nome = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.nome


class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.id}. {self.title}'
