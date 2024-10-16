import pygame
import time
import random

pygame.init()
largura = 1000
altura = 600
configTela = (largura, altura)
gameDisplay = pygame.display.set_mode(configTela)
clock = pygame.time.Clock()
white = (255, 255, 255)
black = (0, 0, 0)
pygame.display.set_caption("Superman 2D")
icone = pygame.image.load("assets/icone.jpg")
pygame.display.set_icon(icone)

# Carregar as imagens do Superman para os diferentes estados
superman_normal = pygame.image.load("assets/superman_1.png")
#superman_normal = pygame.transform.rotate(superman_normal, 90)
superman_direita = pygame.image.load("assets/superman_2.png")  # Nova imagem para movimento para direita
#superman_direita = pygame.transform.rotate(superman_direita, 90)
superman_esquerda = pygame.image.load("assets/superman_3.png")  # Nova imagem para movimento para esquerda
#superman_esquerda = pygame.transform.rotate(superman_esquerda, 90)

alturaSuperman = 200
larguraSuperman = 50
fundo = pygame.image.load("assets/fundo.jpg")
fundo = pygame.transform.scale(fundo, (1000, 600))
missile = pygame.image.load("assets/missel.png")
missile = pygame.transform.rotate(missile, 90)
missileAltura = 200
missileLargura = 20

somDeMorte = pygame.mixer.Sound("assets/somDeMorte.wav")
somDeMorte.set_volume(0.1)

# Variável global para controlar o som do jogo
som_ativo = True

def mostraMissile(x, y):
    gameDisplay.blit(missile, (x, y))

def mostraPersonagem(x, y, imagem):
    gameDisplay.blit(imagem, (x, y))

def text_objects(texto, font):
    textSurface = font.render(texto, True, white)
    return textSurface, textSurface.get_rect()

def escreveNaTela(texto):
    fonte = pygame.font.Font("freesansbold.ttf", 100)
    TextSurf, textRect = text_objects(texto, fonte)
    textRect.center = ((largura / 2, altura / 2))
    gameDisplay.blit(TextSurf, textRect)
    pygame.display.update()
    time.sleep(2)
    menu()  # Volta para o menu principal após a morte

def mostraPontuacao(contador):
    fonte = pygame.font.SysFont("Verdana", 30)
    texto = fonte.render("Pontuação: " + str(contador), True, black)
    gameDisplay.blit(texto, (10, 5))

def morte():
    if som_ativo:  # Só toca o som se o som estiver ativado
        pygame.mixer.Sound.play(somDeMorte)
    escreveNaTela("Lex Luthor venceu!")

def menu():
    global som_ativo  # Declarando que vamos usar a variável global som_ativo
    pygame.mixer.music.stop()
    gameDisplay.fill(black)  # Preenche o fundo com a cor preta (caso a imagem não seja carregada)

    # Carregar a imagem de fundo do menu
    fundo_menu = pygame.image.load("assets/fundo_menu.jpg")  # Substitua pelo caminho da sua imagem
    fundo_menu = pygame.transform.scale(fundo_menu, (largura, altura))  # Redimensiona a imagem para o tamanho da tela
    gameDisplay.blit(fundo_menu, (0, 0))  # Desenha a imagem do fundo

    fonte = pygame.font.SysFont("Verdana", 60)
    titulo = fonte.render("Superman 2D", True, white)
    tituloRect = titulo.get_rect(center=(largura // 2, altura // 4))
    gameDisplay.blit(titulo, tituloRect)

    # Botão Start
    fonte_botao = pygame.font.SysFont("Verdana", 40)
    start_text = fonte_botao.render("Iniciar Jogo", True, white)
    start_rect = start_text.get_rect(center=(largura // 2, altura // 2))
    gameDisplay.blit(start_text, start_rect)

    # Botão de som
    som_texto = "Som: " + ("Ativado" if som_ativo else "Desativado")
    som_botao = fonte_botao.render(som_texto, True, white)
    som_rect = som_botao.get_rect(center=(largura // 2, altura // 1.5))
    gameDisplay.blit(som_botao, som_rect)

    # Botão Sair
    sair_texto = fonte_botao.render("Sair", True, white)
    sair_rect = sair_texto.get_rect(center=(largura // 2, altura // 1.25))
    gameDisplay.blit(sair_texto, sair_rect)

    pygame.display.update()

    while True:
        for acao in pygame.event.get():
            if acao.type == pygame.QUIT:
                pygame.quit()
                quit()

            if acao.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(acao.pos):
                    jogo()  # Inicia o jogo ao clicar em Start Game
                elif som_rect.collidepoint(acao.pos):
                    som_ativo = not som_ativo  # Alterna o estado do som
                    print(f"Som ativado: {som_ativo}")  # Debug para verificar se o som está mudando
                    menu()  # Atualiza o menu após a mudança no som
                elif sair_rect.collidepoint(acao.pos):
                    pygame.quit()  # Fecha o jogo
                    quit()


def jogo():
    global som_ativo
    if som_ativo:
        pygame.mixer.music.load("assets/SupermanTheme.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)
    
    supermanPosicaoX = largura * 0.38
    supermanPosicaoY = altura * 0.68
    movimentoX = 0
    velocidade = 7

    missileVelocidade = 5
    missileX = random.randrange(0, largura)
    missileY = -200
    pontuacao = 0

    superman_imagem = superman_normal  # Imagem inicial do personagem

    while True:
        # qualquer ação realizada pelo usuário
        acoes = pygame.event.get()
        for acao in acoes:
            if acao.type == pygame.QUIT:
                pygame.quit()
                quit()
            if acao.type == pygame.KEYDOWN:
                if acao.key == pygame.K_LEFT:
                    movimentoX = -5
                    superman_imagem = superman_esquerda  # Muda para a imagem de movimento para esquerda
                elif acao.key == pygame.K_RIGHT:
                    movimentoX = 5
                    superman_imagem = superman_direita  # Muda para a imagem de movimento para direita
            if acao.type == pygame.KEYUP:
                if acao.key == pygame.K_LEFT or acao.key == pygame.K_RIGHT:
                    movimentoX = 0
                    superman_imagem = superman_normal  # Volta para a imagem padrão quando não houver movimento

        supermanPosicaoX += movimentoX

        if supermanPosicaoX < 0:
            supermanPosicaoX = 0
        elif supermanPosicaoX > largura - alturaSuperman:
            supermanPosicaoX = largura - alturaSuperman

        # Análise de colisão do míssil com o personagem
        if supermanPosicaoY < missileY + missileAltura:
            if supermanPosicaoX < missileX and supermanPosicaoX + larguraSuperman > missileX or missileX + missileLargura > supermanPosicaoX and missileX + missileLargura < supermanPosicaoX + larguraSuperman:
                morte()
            else:
                print("")

        gameDisplay.blit(fundo, (0, 0))
        mostraPersonagem(supermanPosicaoX, supermanPosicaoY, superman_imagem)
        missileY = missileY + missileVelocidade

        if missileY > altura:
            missileY = -200
            missileX = random.randrange(0, largura)
            pontuacao += 1  
            missileVelocidade += 0.5

        mostraMissile(missileX, missileY)
        mostraPontuacao(pontuacao)
        pygame.display.update()
        clock.tick(60)  # Atualiza a tela x vezes por segundo

menu()
