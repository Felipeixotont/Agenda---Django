from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.http.response import Http404, JsonResponse

#  responsável por criar uma sessão para o usuário autenticar.
def login_user(request):
    return render(request, 'login.html')

#  função para deslogar, apaga os dados da sessão do usuário.
def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)

        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, " Usuário ou senha inválido.") #  envia uma lista de mensagens para o login.html

    return redirect('/')


@login_required(login_url='/login/')  #  esse parametro é para quando não estiver autenticado, encaminhar para pagina de login
def lista_eventos(request):
    #  evento = Evento.objects.get(id=1)       pega só 1

    data_atual = datetime.now()
    usuario = request.user  #  pega o usuario que está logado.
    evento = Evento.objects.filter(usuario=usuario, dataEvento__gt=data_atual) # não podemos usar nas queries do Django operadores de > e < etc, __gt para maior e __lt para menor.
#   evento = Evento.objects.all()   #  Evento.objects.all() ao invés de pegar 1 pega todos.
    response = {'eventos': evento}
    return render(request, 'agenda.html', response)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}

    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)

    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        dataEvento = request.POST.get('data')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')

        if id_evento:
            Evento.objects.filter(id=id_evento).update(titulo=titulo,
                                                       dataEvento=dataEvento,
                                                       descricao=descricao)
        else:
            Evento.objects.create(
                titulo=titulo,
                dataEvento=dataEvento,
                descricao=descricao,
                usuario=usuario
            )

    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user

    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()

    if evento.usuario == usuario:
        evento.delete()
    else:
        raise Http404()

    return redirect('/')


