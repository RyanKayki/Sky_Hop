import pygame
import random

pygame.init()

#CORES
BRANCO, PRETO, VERMELHO = (255, 255, 255), (0, 0, 0), (255, 0, 0)
TERRA, GRAMA, AZUL = (139, 69, 19), (0, 128, 0), (135, 206, 235)
FOSCO = (0, 0, 0, 128)

#TAMANHO DA JANELA
LARGURA, ALTURA = 800, 600
TAMANHO_JANELA = (LARGURA, ALTURA)
estado_jogo = "INICIO"
ajuste_tela_ativo = tela_cheia = False
janela = pygame.display.set_mode(TAMANHO_JANELA)
pygame.display.set_caption("Sky Hop")

#FUNCOES - TELA CHEIA
def alternar_tela_cheia():
    global tela_cheia, janela
    tela_cheia = not tela_cheia
    if tela_cheia:
        info = pygame.display.Info()
        janela = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    else:
        janela = pygame.display.set_mode((LARGURA, ALTURA))

#AJUSTAR TELA
def ajustar_tela():
    global LARGURA, ALTURA, janela, ajuste_tela_ativo
    nova_largura, nova_altura = pygame.display.get_surface().get_size()
    if ajuste_tela_ativo:
        LARGURA, ALTURA = nova_largura, nova_altura
        janela = pygame.display.set_mode((LARGURA, ALTURA))
        ajuste_tela_ativo = False
    else:
        ajuste_tela_ativo = True
        janela = pygame.display.set_mode((nova_largura, nova_altura), pygame.RESIZABLE)

#JOGADOR PROPRIEDADES
largura_jogador, altura_jogador = 50, 50
posicao_jogador_x, posicao_jogador_y = LARGURA // 2 - largura_jogador // 2, ALTURA - altura_jogador
FPS_jogador = 5

#DEFINIÇOES PARA O COMEÇO DO JOGO - RECORD
fim_de_jogo, jogo_ativo = False, False
pausado = False
pontuacao, recorde = 0, 0

try:
    with open("recorde.txt", "r") as arquivo:
        recorde = int(arquivo.read())
except FileNotFoundError:
    pass

#VELOCIDADE
obstaculos = []
FPS_obstaculos = 3

relogio = pygame.time.Clock()

#IMAGEM DO JOGADOR
imagem_jogador = pygame.image.load("documents/2ºSemestre/FPOO/Aula 15/imagens/pou.png")
novo_tamanho = (50, 50)
imagem_jogador = pygame.transform.scale(imagem_jogador, novo_tamanho)

#DESENHO DO JOGADOR
def desenhar_jogador(x, y):
    janela.blit(imagem_jogador, (x, y))

#PONTUAÇÃO
def mostrar_pontuacao(pontuacao, recorde):
    fonte = pygame.font.Font(None, 36)
    texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, PRETO)
    texto_recorde = fonte.render(f"Recorde: {recorde}", True, PRETO)
    janela.blit(texto_pontuacao, (10, 10))
    janela.blit(texto_recorde, (10, 50))

#VERIFICAÇÃO PARA A COLISÃO
def verificar_colisao(posicao_jogador_x, posicao_jogador_y, largura_jogador, altura_jogador, posicao_obstaculo_x, posicao_obstaculo_y, largura_obstaculo, altura_obstaculo):
    return posicao_jogador_y < posicao_obstaculo_y + altura_obstaculo and posicao_jogador_y + altura_jogador > posicao_obstaculo_y and posicao_jogador_x < posicao_obstaculo_x + largura_obstaculo and posicao_jogador_x + largura_jogador > posicao_obstaculo_x

#CREDITOS
def mostrar_info_criador():
    fonte = pygame.font.Font(None, 24)
    texto_info_criador = fonte.render("Criado por: Ryan Kayki", True, PRETO)
    retangulo_info_criador = texto_info_criador.get_rect(center=(LARGURA // 2, ALTURA - 20))
    janela.blit(texto_info_criador, retangulo_info_criador)

#TELA DE PAUSE
def mostrar_tela_pausa():
    janela.fill(FOSCO)
    fonte = pygame.font.Font(None, 72)
    texto_pausa = fonte.render("Jogo Pausado", True, BRANCO)
    retangulo_pausa = texto_pausa.get_rect(center=(LARGURA // 2, ALTURA // 2 - 50))
    janela.blit(texto_pausa, retangulo_pausa)
    fonte = pygame.font.Font(None, 36)
    botao_continuar = pygame.Rect(LARGURA // 2 - 75, ALTURA // 2 + 10, 150, 50)
    pygame.draw.rect(janela, VERMELHO, botao_continuar)
    texto_continuar = fonte.render("Continuar", True, BRANCO)
    retangulo_continuar = texto_continuar.get_rect(center=botao_continuar.center)
    janela.blit(texto_continuar, retangulo_continuar)
    botao_sair = pygame.Rect(LARGURA // 2 - 75, ALTURA // 2 + 70, 150, 50)
    pygame.draw.rect(janela, VERMELHO, botao_sair)
    texto_sair = fonte.render("Sair", True, BRANCO)
    retangulo_sair = texto_sair.get_rect(center=botao_sair.center)
    janela.blit(texto_sair, retangulo_sair)

#TELA DE CONFIG
def mostrar_tela_configuracao():
    janela.fill(AZUL)
    fonte = pygame.font.Font(None, 36)
    botao_tela_cheia = pygame.Rect(LARGURA // 2 - 75, ALTURA // 2 + 10, 150, 50)
    pygame.draw.rect(janela, VERMELHO, botao_tela_cheia)
    texto_tela_cheia = fonte.render("Tela Cheia", True, BRANCO)
    retangulo_tela_cheia = texto_tela_cheia.get_rect(center=botao_tela_cheia.center)
    janela.blit(texto_tela_cheia, retangulo_tela_cheia)
    botao_ajuste_tela = pygame.Rect(LARGURA // 2 - 75, ALTURA // 2 + 70, 150, 50)
    pygame.draw.rect(janela, VERMELHO, botao_ajuste_tela)
    texto_ajuste_tela = fonte.render("Ajustar Tela", True, BRANCO)
    retangulo_ajuste_tela = texto_ajuste_tela.get_rect(center=botao_ajuste_tela.center)
    janela.blit(texto_ajuste_tela, retangulo_ajuste_tela)

#CRIAR PLATAFORMAS
def criar_obstaculo():
    largura_obstaculo = random.randint(50, 200)
    posicao_obstaculo_x = random.randint(0, LARGURA - largura_obstaculo)
    tipo_obstaculo = 'terra' if random.randint(0, 1) == 0 else 'grama'
    obstaculos.append([posicao_obstaculo_x, 0, largura_obstaculo, 20, tipo_obstaculo])

#GAME OVER - INICIO
while not fim_de_jogo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fim_de_jogo = True
        elif evento.type == pygame.VIDEORESIZE:
            ajustar_tela()

    teclas = pygame.key.get_pressed()

    if estado_jogo == "INICIO":
        janela.fill(AZUL)
        fonte = pygame.font.Font(None, 72)
        texto_inicio = fonte.render("Sky Hop", True, PRETO)
        retangulo_inicio = texto_inicio.get_rect(center=(LARGURA // 2, ALTURA // 2 - 50))
        janela.blit(texto_inicio, retangulo_inicio)
        fonte = pygame.font.Font(None, 36)
        botao_iniciar = pygame.Rect(LARGURA // 2 - 75, ALTURA // 2 + 10, 150, 50)
        pygame.draw.rect(janela, PRETO, botao_iniciar)
        texto_iniciar = fonte.render("Iniciar", True, BRANCO)
        retangulo_iniciar = texto_iniciar.get_rect(center=botao_iniciar.center)
        janela.blit(texto_iniciar, retangulo_iniciar)
        botao_ajuste_tela = pygame.Rect(LARGURA // 2 - 75, ALTURA // 2 + 70, 150, 50)
        pygame.draw.rect(janela, PRETO, botao_ajuste_tela)
        texto_ajuste_tela = fonte.render("Ajustar Tela", True, BRANCO)
        retangulo_ajuste_tela = texto_ajuste_tela.get_rect(center=botao_ajuste_tela.center)
        janela.blit(texto_ajuste_tela, retangulo_ajuste_tela)
        botao_tela_cheia = pygame.Rect(LARGURA // 2 - 75, ALTURA // 2 + 130, 150, 50)
        pygame.draw.rect(janela, PRETO, botao_tela_cheia)
        texto_tela_cheia = fonte.render("Tela Cheia", True, BRANCO)
        retangulo_tela_cheia = texto_tela_cheia.get_rect(center=botao_tela_cheia.center)
        janela.blit(texto_tela_cheia, retangulo_tela_cheia)
        mostrar_info_criador()
        if botao_iniciar.collidepoint(pygame.mouse.get_pos()) and evento.type == pygame.MOUSEBUTTONDOWN:
            estado_jogo, jogo_ativo, pontuacao, obstaculos, posicao_jogador_x, posicao_jogador_y = "JOGO", True, 0, [], LARGURA // 2 - largura_jogador // 2, ALTURA - altura_jogador
        if botao_ajuste_tela.collidepoint(pygame.mouse.get_pos()) and evento.type == pygame.MOUSEBUTTONDOWN:
            ajustar_tela()
        if botao_tela_cheia.collidepoint(pygame.mouse.get_pos()) and evento.type == pygame.MOUSEBUTTONDOWN:
            alternar_tela_cheia()

    elif estado_jogo == "JOGO":
        if not pausado:
            if teclas[pygame.K_LEFT] and posicao_jogador_x > 0:
                posicao_jogador_x -= FPS_jogador
            if teclas[pygame.K_RIGHT] and posicao_jogador_x < LARGURA - largura_jogador:
                posicao_jogador_x += FPS_jogador
            for obstaculo in obstaculos:
                obstaculo[1] += FPS_obstaculos
            for obstaculo in obstaculos:
                if verificar_colisao(posicao_jogador_x, posicao_jogador_y, largura_jogador, altura_jogador, obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]):
                    jogo_ativo = False
            obstaculos = [obstaculo for obstaculo in obstaculos if obstaculo[1] < ALTURA]
            if random.randint(0, 100) < 5:
                criar_obstaculo()
            pontuacao += len(obstaculos)
        janela.fill(AZUL)
        desenhar_jogador(posicao_jogador_x, posicao_jogador_y)
        for obstaculo in obstaculos:
            cor = TERRA if obstaculo[4] == 'terra' else GRAMA
            pygame.draw.rect(janela, cor, (obstaculo[0], obstaculo[1], obstaculo[2], obstaculo[3]))
        mostrar_pontuacao(pontuacao, recorde)
        if not jogo_ativo:
            janela.fill(VERMELHO)
            fonte = pygame.font.Font(None, 72)
            texto = fonte.render("Game Over", True, PRETO)
            retangulo_texto = texto.get_rect(center=(LARGURA // 2, ALTURA // 2 - 50))
            janela.blit(texto, retangulo_texto)
            fonte = pygame.font.Font(None, 36)
            if pontuacao > recorde:
                recorde = pontuacao
                texto_novo_recorde = fonte.render("Novo Recorde!", True, PRETO)
                retangulo_novo_recorde = texto_novo_recorde.get_rect(center=(LARGURA // 2, ALTURA // 2 + 10))
                janela.blit(texto_novo_recorde, retangulo_novo_recorde)
            texto_recorde = fonte.render(f"Recorde Atual: {recorde}", True, PRETO)
            retangulo_recorde = texto_recorde.get_rect(center=(LARGURA // 2, ALTURA // 2 + 50))
            janela.blit(texto_recorde, retangulo_recorde)
            texto_reiniciar = fonte.render("Pressione ESPAÇO para jogar novamente", True, PRETO)
            retangulo_reiniciar = texto_reiniciar.get_rect(center=(LARGURA // 2, ALTURA // 2 + 90))
            janela.blit(texto_reiniciar, retangulo_reiniciar)
            mostrar_info_criador()
            with open("recorde.txt", "w") as arquivo:
                arquivo.write(str(recorde))
            if teclas[pygame.K_SPACE]:
                jogo_ativo, pontuacao, obstaculos, posicao_jogador_x, posicao_jogador_y = True, 0, [], LARGURA // 2 - largura_jogador // 2, ALTURA - altura_jogador

    elif estado_jogo == "PAUSA":
        mostrar_tela_pausa()
        fonte = pygame.font.Font(None, 36)
        botao_continuar = pygame.Rect(LARGURA // 2 - 75, ALTURA // 2 + 10, 150, 50)
        pygame.draw.rect(janela, VERMELHO, botao_continuar)
        texto_continuar = fonte.render("Continuar", True, BRANCO)
        retangulo_continuar = texto_continuar.get_rect(center=botao_continuar.center)
        janela.blit(texto_continuar, retangulo_continuar)
        botao_sair = pygame.Rect(LARGURA // 2 - 75, ALTURA // 2 + 70, 150, 50)
        pygame.draw.rect(janela, VERMELHO, botao_sair)
        texto_sair = fonte.render("Sair", True, BRANCO)
        retangulo_sair = texto_sair.get_rect(center=botao_sair.center)
        janela.blit(texto_sair, retangulo_sair)
        if botao_continuar.collidepoint(pygame.mouse.get_pos()) and evento.type == pygame.MOUSEBUTTONDOWN:
            estado_jogo, pausado = "JOGO", False
        if botao_sair.collidepoint(pygame.mouse.get_pos()) and evento.type == pygame.MOUSEBUTTONDOWN:
            fim_de_jogo = True
        
            

    elif estado_jogo == "CONFIGURACAO":
        mostrar_tela_configuracao()
        fonte = pygame.font.Font(None, 36)
        botao_voltar = pygame.Rect(LARGURA // 2 - 75, ALTURA // 2 + 70, 150, 50)
        pygame.draw.rect(janela, VERMELHO, botao_voltar)
        texto_voltar = fonte.render("Voltar", True, BRANCO)
        retangulo_voltar = texto_voltar.get_rect(center=botao_voltar.center)
        janela.blit(texto_voltar, retangulo_voltar)
        if botao_voltar.collidepoint(pygame.mouse.get_pos()) and evento.type == pygame.MOUSEBUTTONDOWN:
            estado_jogo = "JOGO"

    pygame.display.update()

    if teclas[pygame.K_ESCAPE] and estado_jogo == "JOGO":
        estado_jogo, pausado = "PAUSA", True

    relogio.tick(60)

pygame.quit()
