
# Importar a biblioteca Pygame
import pygame

# Importar a biblioteca random para gerar números aleatórios
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Definir constantes para as dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Definir um objeto Player herdando da classe Sprite
# Agora o surf desenhado na tela é um atributo de 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet.png").convert()
        self.surf.set_colorkey((255, 255, 255)), RLEACCEL
        self.rect = self.surf.get_rect()
    
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            som_sobe.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            som_desce.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Mantenha o jogador na tela do jogo
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Definir um objeto Enemy herdando da classe Sprite
# Agora o surf desenhado na tela é um atributo de 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)
    
    # Movimente a sprite com base na velocidade (speed)
    # Remova o sprite quando ele passa da borda esquerda da tela
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Mova a nuvem com velocidade constante
    #Remova a nuvem quando ela sai da tela
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Setup para sons. O padrão já nos atende
pygame.mixer.init()

# Inicializa o pygame
pygame.init()

# Cria a tela
# O tamanho da tela é definido pelas constantes das linhas 18 e 19
tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Crie um evento customizado pra adicionar um novo inimigo e uma nova nuvem
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

#Ajuste o clock para uma taxa framerate adequada

clock = pygame.time.Clock()

# Criar uma cópia do jogador
jogador = Player()

# Crie grupos para controlar os sprites dos inimigos e todos os sprites
# - inimigos será usado pra detectar colisão e atualizar a posição
# Nuvens será usado para atualizar a posição da nuvem
# - all_sprites será usado para renderizar

inimigos = pygame.sprite.Group()
nuvens = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(jogador)

# Carregue e toque músicas de fundo
# Fonte da música: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0

pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops = -1)

#Carregue as outras músicas 
# Fonte da música: Jon Fincher

som_sobe = pygame.mixer.Sound("Rising_putter.ogg")
som_desce = pygame.mixer.Sound("Falling_putter.ogg")
som_batida = pygame.mixer.Sound("Collision.ogg")

# Variável que controla o loop do jogo
rodando = True

# Loop principal
while rodando:
    # percorra a fila de eventos
    for evento in pygame.event.get():
        # O usuário pressionou alguma tecla?
        if evento.type == KEYDOWN:
            #Foi a tecla de Escape? Se sim, saia do loop
            if evento.key == K_ESCAPE:
                rodando = False
        # Foi a tecla de fechar? Se sim, sai do loop
        elif evento.type == QUIT:
            rodando = False
        # Adiciona um inimigo?
        elif evento.type == ADDENEMY:
            # Crie um novo inimigo e adicione ao grupo de sprites
            novoinimigo = Enemy()
            inimigos.add(novoinimigo)
            all_sprites.add(novoinimigo)

        elif evento.type == ADDCLOUD:
            # Crie um novo inimigo e adicione ao grupo de sprites
            novanuvem = Cloud()
            nuvens.add(novanuvem)
            all_sprites.add(novanuvem)

    # Obtenha as teclas pressionadas 
    pressed_keys = pygame.key.get_pressed()

    # Atualiza o sprite do jogador com base nas teclas pressionadas
    jogador.update(pressed_keys)

    # Atualizar a posição do inimigo e da nuvem
    inimigos.update()
    nuvens.update()

    # Preencha a tela de preto
    tela.fill((135, 206, 250))

    # Desenhe todos os sprites
    for item in all_sprites:
        tela.blit(item.surf, item.rect)

    # Verifique se qualquer inimigo colidiu com o jogador
    if pygame.sprite.spritecollideany(jogador, inimigos):
        # Se sim, remova o jogador e pare o jogo
        jogador.kill()
        rodando = False
    
    # Verifique se qualquer inimigo colidiu com o jogador
    if pygame.sprite.spritecollideany(jogador, inimigos):
        # Se sim, remova o jogador e pare o jogo
        jogador.kill()
        # Pare qualquer som quando o jogo acaba
        som_sobe.stop()
        som_desce.stop()
        som_batida.play()
        # Pare o loop do jogo
        rodando = False
    
    pygame.display.flip()
    
    # Manter um framerate de 30 frames por segundo
    clock.tick(60)

# Pare o som e feche o mixer
pygame.mixer.music.stop()
pygame.mixer.quit()