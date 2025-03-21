import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

#config tela
width = 666
height = 666
tela = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pointergeist')


#config loop
black = (0,0,0)
running = True
clock = pygame.time.Clock()

fonte = pygame.font.SysFont("Times New Roman", 30, bold=True, italic=True)
evento = randint(5, 15)
contador = 0

#config o sprite do fanstama
class Ghost(pygame.sprite.Sprite):
    
    def __init__(self, px, py):

        #chama os sprites, configura, aumenta, espelha
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('assets/Scary_Ghost.png'))
        self.sprites.append(pygame.image.load('assets/Scary_Ghost_2.png'))
        self.pointer = 0
        self.image = self.sprites[self.pointer]
        self.image = pygame.transform.scale(self.image, (14*5, 11*5))
        self.image = pygame.transform.flip(self.image, 1, 0)

        #define as coordenadas
        self.px = px
        self.py = py
        self.last_dx = 0

        #desenha o fantasma
        self.rect = self.image.get_rect()
        self.rect.topright = (self.px, self.py)


    #atualiza o fantasma (posicao e sprite)
    def update(self):
        self.rect.topright = pygame.mouse.get_pos()

        self.pointer += 0.05
        if self.pointer >= len(self.sprites):
            self.pointer = 0
        self.image = self.sprites[int(self.pointer)]
        self.image = pygame.transform.scale(self.image, (14*5, 11*5))
        self.image = pygame.transform.flip(self.image, True, False)

class Egg(pygame.sprite.Sprite):
    def __init__(self, px, py):
        #chama os sprites, configura, aumenta, espelha
        super().__init__()  # Inicializa a superclasse
        self.sprites = [pygame.image.load('assets/Egg.png')]
        self.sound = pygame.mixer.Sound('assets/Echo.wav')
        self.image = pygame.transform.scale(self.sprites[0], (14*3, 11*3))


        #define as coordenadas
        self.px = px
        self.py = py

        # Define a posição inicial do ovo
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.px, self.py)

        
    def update(self):
        # Acessa todos os fantasmas do grupo e verifica colisão
        # Agora update() não precisa de argumentos, pois percorre all_sprites para encontrar o Ghost, 
        # evitando erro de chamada incorreta de update() pelo grupo de sprites.
        global contador
        for sprite in all_sprites:
            if isinstance(sprite, Ghost) and pygame.sprite.collide_rect(self, sprite):
                self.sound.play()
                self.rect.topleft = (randint(0, width - self.rect.width), randint(0, height - self.rect.height))
                contador += 1


class Boo(pygame.sprite.Sprite):
    def __init__(self, px, py):
        #chama os sprites, configura, aumenta, espelha
        super().__init__()  # Inicializa a superclasse
        self.sprites = [pygame.image.load('assets/Jumpscare.png')]
        self.sound = pygame.mixer.Sound('assets/Laugh3.wav')
        self.image = pygame.transform.scale(self.sprites[0], (512*1.3, 512*1.3))

        #define as coordenadas
        self.px = px
        self.py = py

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.px, self.py)

    def update(self):
        global evento
        global contador

        if contador == evento:
            self.sound.play()
            self.rect.topleft = (0, 0)  # mostra

  
#adiciona o fantasma e o ovo ao grupo sprite
all_sprites= pygame.sprite.Group()
ghost = Ghost(*pygame.mouse.get_pos())
egg = Egg(width / 2, height /2)
boo = Boo(-1000, -1000)
all_sprites.add(egg)
all_sprites.add(ghost)
all_sprites.add(boo)


while running:
    tela.fill(black)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
    mensagem = f'{contador}'
    texto_formatado = fonte.render(mensagem, True, (255,255,255))
    tela.blit(texto_formatado, (width / 2 ,40))

    all_sprites.update()
    all_sprites.draw(tela)
    

    pygame.display.flip()
    clock.tick(60)
