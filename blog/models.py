from django.db import models
from django.utils import timezone

class Post(models.Model):
    author=models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date=timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author=models.CharField(max_length=200)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now)
    approved_comment=models.BooleanField(default=False)

    def approve(self):
        self.approved_comment=True
        self.save()

    def __str__(self):
        return self.text

''' Mi opcion antes al crear el model Comment era buscar desde el post en el que estes recoger la pk (xq te la pasa la view al llegar) y asociarlo asi desde el model. No funcionaba x demas fallos
seguramente mala sintaxis tambn si es q se podria hacer asi. Pero a lo mejor es un poco complicado si implicas que hay una pk en la definicion que solo se muestra cuando se ha creado el comment
En verdad vendria mas o menos a ser lo mismo ya q en la view lo asgnas asi de todas formas¿? Sería como una forma manual (aun asi una no muy buena opcion)'''
