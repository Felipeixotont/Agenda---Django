from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    dataEvento = models.DateTimeField(verbose_name='Data do Evento')
    dataCriacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) #  se o usuário dono desse evento for excluído da aplicação, exclui também todos os eventos dele.


    class Meta:
        db_table = 'evento'

    def __str__(self):
        return self.titulo

    def get_data_evento(self):
        return self.dataEvento.strftime('%d/%m/%y às %H:%M Hrs')

    def get_data_input_evento(self):
        return self.dataEvento.strftime('%Y-%m-%dT%H:%M')