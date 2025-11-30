# livros/views.py
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.http import HttpResponse, Http404 
from django.contrib.auth.decorators import login_required

# 💡 CORREÇÃO: Certifique-se de que ComentarioLeitura esteja aqui
from .models import (
    Livro, Avaliacao, ComentarioLeitura, ProgressoLeitura,
    Conversa, Mensagem, Perfil, GENERO_CHOICES,
)
# ...


# -----------------------------------------------------------------
# 1. FUNÇÃO HOME: Lida com a página inicial (Seguindo e Pra Você)
# -----------------------------------------------------------------
def home(request):
    # 'seguindo' é o padrão se nenhum parâmetro 'tab' for passado na URL
    active_tab = request.GET.get('tab', 'seguindo') 

    # --- LISTAS PARA A ABA "SEGUINDO" (Filtros por Gênero) ---
    livros_em_alta = Livro.objects.filter(em_alta=True).order_by('?')[:4]
    livros_romance = Livro.objects.filter(genero__iexact='Romance').order_by('?')[:4]
    livros_fantasia = Livro.objects.filter(genero__iexact='Fantasia').order_by('?')[:4]
    livros_acao = Livro.objects.filter(genero__iexact='Ação').order_by('?')[:4]
    livros_ficcao = Livro.objects.filter(genero__iexact='Ficção Adolescente').order_by('?')[:4]
    livros_contos = Livro.objects.filter(genero__iexact='Contos').order_by('?')[:4]
    livros_drama = Livro.objects.filter(genero__iexact='Drama').order_by('?')[:4]
    livros_gastronomia = Livro.objects.filter(genero__iexact='Gastronomia').order_by('?')[:4]
    livros_espiritualidade = Livro.objects.filter(genero__iexact='Espiritualidade').order_by('?')[:4]

    # --- LISTAS PARA A ABA "PRA VOCÊ" (Conteúdo Sugerido/Geral) ---
    livros_voce_1 = Livro.objects.all().order_by('?')[:4]
    livros_voce_2 = Livro.objects.all().order_by('?')[:4]
    livros_voce_3 = Livro.objects.all().order_by('?')[:4]

    context = {
        'active_tab': active_tab, 
        
        # Dados da aba "Seguindo"
        'livros_em_alta': livros_em_alta,
        'livros_romance': livros_romance,
        'livros_fantasia': livros_fantasia,
        'livros_acao': livros_acao,
        'livros_ficcao': livros_ficcao,
        'livros_contos': livros_contos,
        'livros_drama': livros_drama,
        'livros_gastronomia': livros_gastronomia,
        'livros_espiritualidade': livros_espiritualidade,

        # Dados da aba "Pra Você"
        'livros_voce_1': livros_voce_1,
        'livros_voce_2': livros_voce_2,
        'livros_voce_3': livros_voce_3,
    }

    return render(request, 'home.html', context)


# -----------------------------------------------------------------------
# 2. NOVA FUNÇÃO: DETALHE DO LIVRO (Carrega o conteúdo do livro específico)
# -----------------------------------------------------------------------
def detalhe_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    
    # ... (Seu código existente para calcular a média e buscar avaliações) ...
    media_estrelas = livro.avaliacoes.aggregate(Avg('estrelas'))['estrelas__avg']
    media_estrelas_arredondada = round(media_estrelas) if media_estrelas is not None else 0
    
    # Buscando as avaliações reais
    avaliacoes = Avaliacao.objects.filter(livro=livro)
    
    context = {
        'livro': livro,
        'avaliacoes': avaliacoes, # Garanta que você está usando 'avaliacoes' aqui
        'media_estrelas': media_estrelas_arredondada,
    }
    return render(request, 'livros/detalhe_livro.html', context)


# 💡 NOVA FUNÇÃO PARA PROCESSAR O FORMULÁRIO POST
def adicionar_avaliacao(request, pk):
    if request.method == 'POST':
        livro = get_object_or_404(Livro, pk=pk)

        nome = request.POST.get('nome')
        estrelas = request.POST.get('estrelas')
        texto = request.POST.get('texto')

        try:
            estrelas = int(estrelas)
            if not 1 <= estrelas <= 5:
                return HttpResponse("Erro: O número de estrelas deve ser entre 1 e 5.", status=400)
            if not nome or not texto:
                return HttpResponse("Erro: Nome e texto da avaliação são obrigatórios.", status=400)

        except (ValueError, TypeError):
            return HttpResponse("Erro: Valor de estrela inválido.", status=400)

        Avaliacao.objects.create(
            livro=livro,
            nome=nome,
            estrelas=estrelas,
            texto=texto,
        )

        return redirect('livros:detalhe_livro', pk=livro.pk)

    return redirect('livros:detalhe_livro', pk=pk)


# -------------------------------------------
# 4. FUNÇÃO LEITURA LIVRO (Carrega a página de leitura)
# -------------------------------------------

def ler_livro(request, pk):
    livro = get_object_or_404(Livro, pk=pk)
    pagina = int(request.GET.get("pag", 1))
    texto = livro.conteudo or ""

    # --- TAMANHO MÁXIMO POR PÁGINA ---
    TAM_PAGINA = 1200

    blocos = []
    inicio = 0
    total = len(texto)

    while inicio < total:
        blocos.append(texto[inicio:inicio + TAM_PAGINA])
        inicio += TAM_PAGINA

    # total = capa + título + blocos
    total_paginas = len(blocos) + 2

    # --- PÁGINA 1 / CAPA ---
    if pagina == 1:
        return render(request, "livros/leitura.html", {
            "livro": livro,
            "pagina": pagina,
            "paginas": list(range(1, total_paginas + 1)),
            "linhas": [],
            "comentarios_agrupados": {},
        })

    # --- PÁGINA 2 / TÍTULO ---
    if pagina == 2:
        return render(request, "livros/leitura.html", {
            "livro": livro,
            "pagina": pagina,
            "paginas": list(range(1, total_paginas + 1)),
            "linhas": [],
            "comentarios_agrupados": {},
        })

    if request.user.is_authenticated:
        # Nível 2 (8 espaços)
        progresso, created = ProgressoLeitura.objects.get_or_create(
            # Nível 3 (12 espaços)
            usuario=request.user,
            livro=livro
        )
        # Nível 2 (8 espaços)
        progresso.pagina_atual = pagina
        progresso.total_paginas = total_paginas
        progresso.save()

    # --- PÁGINAS DE CONTEÚDO ---
    index = pagina - 3
    bloco = blocos[index] if 0 <= index < len(blocos) else ""

    # divide o texto do bloco em parágrafos reais
    linhas = [p.strip() for p in bloco.split("\n") if p.strip()]

    comentarios = ComentarioLeitura.objects.filter(livro=livro)

    comentarios_agrupados = {}
    for c in comentarios:
        comentarios_agrupados.setdefault(c.posicao_paragrafo, []).append(c)

    return render(request, "livros/leitura.html", {
        "livro": livro,
        "pagina": pagina,
        "paginas": list(range(1, total_paginas + 1)),
        "linhas": linhas,
        "comentarios_agrupados": comentarios_agrupados,
    })

# -------------------------------------------
# 5. FUNÇÃO ADICIONAR COMENTÁRIO EM LINHA (Salva o formulário)
# -------------------------------------------
def publicar_comentario(request, pk):
    livro = get_object_or_404(Livro, pk=pk)

    if request.method != "POST":
        return HttpResponse("Método inválido", status=405)

    pos = request.POST.get("posicao_paragrafo")
    if not pos or not pos.isdigit():
        return HttpResponse("Erro: posição inválida", status=400)

    ComentarioLeitura.objects.create(
        livro=livro,
        nome=request.user.first_name or request.user.username,
        texto=request.POST.get("texto"),
        posicao_paragrafo=int(pos)
    )

    # redireciona para a mesma página
    return redirect(f"/livro/{pk}/leitura/?pag={int(pos)+2}")


# -------------------------------------------
# 6. MINHA BIBLIOTECA
# -------------------------------------------

@login_required
def biblioteca(request):
    
    tab = request.GET.get('tab', 'leitura')

    em_leitura = []
    estante = []

    if request.user.is_authenticated:
        progresso = (
            ProgressoLeitura.objects
            .filter(usuario=request.user)
            .select_related('livro')
        )

        # CRIAR OBJETOS COMPUTADOS
        for p in progresso:
            try:
                percent = int((p.pagina_atual / p.total_paginas) * 100)
            except ZeroDivisionError:
                percent = 0

            media = (
                p.livro.avaliacoes.aggregate(Avg("estrelas"))["estrelas__avg"]
            )
            if media is None:
                media = 0

            em_leitura.append({
                "livro": p.livro,
                "pagina_atual": p.pagina_atual,
                "total_paginas": p.total_paginas,
                "percent": percent,
                "media": round(media, 1),  # 👈 bonitinho para exibir 4.3
            })


    context = {
        "tab": tab,
        "em_leitura": em_leitura,
        "estante": estante,
    }
    
    return render(request, "livros/biblioteca.html", context)

@login_required
def busca(request):

    # 1️⃣ Categorias dos livros que o usuário está lendo
    generos_user = (
        Livro.objects
        .filter(leituras__usuario=request.user)
        .values_list("genero", flat=True)
        .distinct()
    )

    # Se o usuário nunca leu nada → recomendar tudo
    if not generos_user:
        livros_qs = Livro.objects.all()
    else:
        livros_qs = Livro.objects.filter(genero__in=generos_user)

    # 2️⃣ Filtro de UI (pill)
    filtro = request.GET.get("filtro")
    if filtro:
        livros_qs = livros_qs.filter(genero=filtro)

    # 3️⃣ Enrich (avaliacao média)
    livros = []
    for lv in livros_qs:
        media = lv.avaliacoes.aggregate(Avg("estrelas"))["estrelas__avg"]
        lv.media_avaliacao = round(media or 0, 1)
        livros.append(lv)

    context = {
        "categorias": list(generos_user),  # só o que o user lê
        "filtro": filtro,
        "livros": livros,
    }

    return render(request, "livros/busca.html", context)

@login_required
def chat(request):
    conversas = Conversa.objects.filter(participantes=request.user)

    lista = []
    for conv in conversas:
        ultima = conv.mensagens.order_by("-criado_em").first()

        if ultima:
            perfil = Perfil.objects.filter(user=ultima.autor).first()
            avatar = perfil.foto.url if perfil and perfil.foto else "/static/livros/img/default_profile.png"
        else:
            avatar = "/static/livros/img/default_profile.png"

        lista.append({
            "id": conv.id,
            "nome": conv.nome or ultima.autor.username if ultima else "Nova conversa",
            "msg": ultima.texto if ultima else "",
            "avatar": avatar,
        })

    return render(request, "livros/chat.html", {"conversas": lista})

@login_required
def chat_conversa(request, pk):
    conversa = get_object_or_404(Conversa, id=pk, participantes=request.user)

    if request.method == "POST":
        texto = request.POST.get("msg")
        if texto:
            Mensagem.objects.create(
                conversa=conversa,
                autor=request.user,
                texto=texto
            )
        return redirect("livros:chat_conversa", pk=pk)

    msgs = conversa.mensagens.select_related("autor").order_by("criado_em")

    return render(request, "livros/chat_conversa.html", {
        "conversa": conversa,
        "msgs": msgs
    })

@login_required
def perfil(request):
    perfil, created = Perfil.objects.get_or_create(user=request.user)

    if request.method == "POST":
        if request.FILES.get("foto"):
            perfil.foto = request.FILES["foto"]
            perfil.save()

        return redirect("livros:perfil")

    return render(request, "livros/perfil.html", {"perfil": perfil})

@login_required
def comando_voz(request):
    texto = request.GET.get("texto", "").lower().strip()

    if "áudio" in texto or "audio" in texto or "reproduzir" in texto or "ouvir" in texto:
        return JsonResponse({
            "redirect": "/livro/4/leitura/?pag=3&audio=1"
        })

    return JsonResponse({"msg": "Não entendi o que você disse."})

    # EXEMPLO 1 — Retomar último livro
    if "último" in texto or "continuar" in texto:
        return JsonResponse({
            "redirect": "/livro/4/leitura/?pag=3"
        })

    # EXEMPLO 2 — Começar leitura
    if "começar" in texto or "ler" in texto:
        return JsonResponse({
            "redirect": "/livro/4/leitura/?pag=1"
        })

    # EXEMPLO 3 — Abrir pelo título
    # (atenção: busca simples)
    for livro in Livro.objects.all():
        if livro.titulo.lower() in texto:
            return JsonResponse({
                "redirect": f"/livro/{livro.pk}/"
            })

    # Nenhuma regra encontrada →
    return JsonResponse({
        "msg": "Não consegui entender. Tente novamente."
    })