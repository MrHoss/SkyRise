import os
import sys
import math
import random
from random import uniform
import pygame
from pygame import mixer


pygame.init()
# ------------------------ Configurações ------------------------
START_FULLSCREEN = True   # True para fullscreen (tente primeiro), False para janela
FPS = 60
MAX_OBJECTS = 6
COLLISION_RADIUS = 80     # Ajuste conforme o tamanho dos sprites
RESOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    info = pygame.display.Info()
    WIN_X, WIN_Y = info.current_w, info.current_h
except pygame.error:
    WIN_X, WIN_Y = 1280, 720  # fallback

# Utility: safe resource loader
def load_image(rel_path, fallback_color=(255,0,255), scale=None):
    path = os.path.join(RESOURCE_DIR, rel_path)
    if not os.path.isfile(path):
        print(f"[WARN] Imagem não encontrada: {path}")
        # cria surface de fallback
        surf = pygame.Surface((64,64), pygame.SRCALPHA)
        surf.fill(fallback_color+(0,))
        return surf
    img = pygame.image.load(path).convert_alpha()
    if scale is not None:
        img = pygame.transform.scale(img, scale)
    return img

def load_sound(rel_path):
    path = os.path.join(RESOURCE_DIR, rel_path)
    if not os.path.isfile(path):
        print(f"[WARN] Som não encontrado: {path}")
        return None
    return mixer.Sound(path)

# ------------------------ Inicialização ------------------------
pygame.init()
mixer.init()  # inicializa mixer explicitamente

# Configura a janela de forma compatível (evita passar args que alguns backends não aceitam)
window_flags = pygame.FULLSCREEN if START_FULLSCREEN else 0
window = pygame.display.set_mode((WIN_X, WIN_Y), window_flags)
pygame.display.set_caption("SkyRise")

# Ícone (se existir)
try:
    icon = load_image('Icon.png')
    pygame.display.set_icon(icon)
except Exception as e:
    print("Ícone não carregado:", e)

clock = pygame.time.Clock()

# ------------------------ Carregamento de assets ------------------------
background = load_image('gfx/bg/background4_3.png', scale=(WIN_X, WIN_Y))
playerShip1 = load_image('gfx/ships/ship.png')
playerShip2 = load_image('gfx/ships/ship1.png')
HUD = load_image('gfx/HUD.png')
ASTER1 = load_image('gfx/asteroids/Asteroid.png')
ASTER2 = load_image('gfx/asteroids/Asteroid2.png')
ASTER3 = load_image('gfx/asteroids/Asteroid3.png')

# load music & sounds (mixer music uses absolute paths)
bg_music_path = os.path.join(RESOURCE_DIR, 'sfx/background.wav')
if os.path.isfile(bg_music_path):
    mixer.music.load(bg_music_path)
explosionSound = load_sound('sfx/explosion.wav')

# ------------------------ Fonts ------------------------
# Definimos fontes uma vez
FONT = pygame.font.SysFont('comicsans', 40, True)
GO_FONT = pygame.font.SysFont('comicsans', 64, True)
KEY_FONT = pygame.font.SysFont('comicsans', 20, True)

# ------------------------ Objetos (asteroides) ------------------------
objectImg = []
objectX = []
objectY = []
objectY_move = []

for i in range(MAX_OBJECTS):
    objectImg.append(random.choice([ASTER1, ASTER2, ASTER3]))
    objectX.append(random.uniform(0, WIN_X))
    objectY.append(random.uniform(-3000, -300))
    objectY_move.append(15)

# ------------------------ Variáveis de jogo globais (iniciais) ------------------------
playerShip = playerShip1  # seleção padrão
# HUD text placeholders (serão atualizados na tela de jogo)
text_score = FONT.render("", True, (255,255,255))
text_lvl = FONT.render("", True, (255,255,255))
text_life = FONT.render("", True, (255,255,255))

# ------------------------ Funções utilitárias ------------------------
def blit_centered(surf, img, pos):
    """Blita a imagem com seu centro em pos"""
    rect = img.get_rect(center=pos)
    surf.blit(img, rect.topleft)

def player(x, y):
    window.blit(playerShip, (x, y))

def objects(x, y, i):
    window.blit(objectImg[i], (x, y))

def isCollision(enemyX, enemyY, playerX, playerY, radius=COLLISION_RADIUS):
    # Usa distância euclidiana entre centros (ajuste radius conforme sprites)
    dx = (enemyX + objectImg[0].get_width()/2) - (playerX + playerShip.get_width()/2)
    dy = (enemyY + objectImg[0].get_height()/2) - (playerY + playerShip.get_height()/2)
    distance = math.hypot(dx, dy)
    return distance < radius

# ------------------------ Telas do jogo ------------------------
def paused():
    pause_text = GO_FONT.render("GAME PAUSED - Press ESC to resume", True, (255,255,255))
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
        window.blit(background, (0,0))
        window.blit(pause_text, (WIN_X//2 - pause_text.get_width()//2, WIN_Y//2 - 32))
        pygame.display.update()
        clock.tick(10)

def Startscreen():
    StartLogo = load_image('Logo.png')
    # tenta escalar pra metade da tela, mas se faltar logo, não quebrar
    try:
        StartLogo = pygame.transform.scale(StartLogo, (int(WIN_X/2), int(WIN_Y/2)))
    except Exception:
        pass
    Continue = FONT.render("Press <SPACEBAR> to continue", True, (255,255,255))
    Start = True
    while Start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ShipSelection()
                    Start = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        window.fill((0,0,0))
        window.blit(background, (0,0))
        if StartLogo:
            window.blit(StartLogo, (WIN_X//2 - StartLogo.get_width()//2, WIN_Y//2 - StartLogo.get_height()//2 - 100))
        window.blit(Continue, (WIN_X//2 - Continue.get_width()//2, WIN_Y//2 + 150))
        pygame.display.update()
        clock.tick(30)

def ShipSelection():
    global playerShip
    selected1 = False
    selected2 = False
    bposX = 100
    bposY = 100
    bsizeX = 144
    bsizeY = 144
    select = True
    while select:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Startscreen()
                    select = False
                if event.key == pygame.K_SPACE and (playerShip == playerShip1 or playerShip == playerShip2):
                    GamingScreen()
                    select = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if bposX <= mx <= bposX + bsizeX and bposY <= my <= bposY + bsizeY:
                    playerShip = playerShip1
                    selected1 = True; selected2 = False
                if bposX + 160 <= mx <= bposX + 160 + bsizeX and bposY <= my <= bposY + bsizeY:
                    playerShip = playerShip2
                    selected2 = True; selected1 = False

        mouse = pygame.mouse.get_pos()
        window.fill((0,0,0))
        window.blit(background, (0,0))
        keytext = KEY_FONT.render("<SPACEBAR>:Confirm   <ESC>:Return   <Alt+F4>:Close game", True, (255,255,255))
        window.blit(keytext, (20, WIN_Y-30))

        mouse_over = (170, 170, 170)
        mouse_out = (100, 100, 100)
        selectedc = (110, 110, 110)

        # botão 1
        rect1 = pygame.Rect(bposX, bposY, bsizeX, bsizeY)
        rect2 = pygame.Rect(bposX+160, bposY, bsizeX, bsizeY)

        if selected1:
            pygame.draw.rect(window, selectedc, rect1)
        elif rect1.collidepoint(mouse):
            pygame.draw.rect(window, mouse_over, rect1)
        else:
            pygame.draw.rect(window, mouse_out, rect1)

        if selected2:
            pygame.draw.rect(window, selectedc, rect2)
        elif rect2.collidepoint(mouse):
            pygame.draw.rect(window, mouse_over, rect2)
        else:
            pygame.draw.rect(window, mouse_out, rect2)

        # desenha as naves
        window.blit(playerShip1, (bposX, bposY))
        window.blit(playerShip2, (bposX+180, bposY))
        pygame.display.update()
        clock.tick(30)

def GameoverScreen(score_text, level_text):
    GOtext = GO_FONT.render("GAME OVER", True, (255,255,255))
    keytext = KEY_FONT.render("<SPACEBAR>:Ship Selection   <ESC>:Exit game", True, (255,255,255))
    credittext = KEY_FONT.render("Game made By MrHoss", True, (255,255,255))
    GOscreen = True
    # animação simples dos objetos ainda caindo
    while GOscreen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_SPACE:
                    ShipSelection()
                    GOscreen = False

        dt = clock.tick(FPS) / 1000.0  # segundos desde o último frame

        # atualiza posições dos objetos para dar vida à tela de game over
        for i in range(MAX_OBJECTS):
            if objectY[i] >= WIN_Y + 200:
                objectY[i] = uniform(-800, -1000)
                objectX[i] = uniform(0, WIN_X)
            objectY[i] += objectY_move[i] * dt * 60  # mantém velocidade consistente
        
        window.fill((0,0,0))
        window.blit(background, (0,0))
        window.blit(keytext, (20, WIN_Y - 30))
        window.blit(credittext, (WIN_X-250, WIN_Y-30))
        window.blit(score_text, (WIN_X//2 - score_text.get_width()//2, WIN_Y//2 - 100))
        window.blit(level_text, (WIN_X//2 - level_text.get_width()//2, WIN_Y//2 - 140))
        window.blit(GOtext, (WIN_X // 2 - GOtext.get_width()//2, WIN_Y // 2 - 250))

        for i in range(MAX_OBJECTS):
            objects(objectX[i], objectY[i], i)

        pygame.display.update()
        clock.tick(FPS)

def GamingScreen():
    global text_score, text_lvl, text_life

    # Inicia música de fundo (se disponível)
    try:
        if os.path.isfile(bg_music_path):
            mixer.music.play(-1)
    except Exception as e:
        print("Erro ao tocar música:", e)

    playerX = WIN_X / 2 - 50
    playerY = WIN_Y / 2 + 150
    speed = 10
    lvl = 0
    lvlCount = 1
    timer = 0
    life = 3
    clockSec = 0

    # atualiza textos HUD
    def update_texts():
        nonlocal clockSec, lvlCount, life
        text_score = FONT.render("Score: " + str(clockSec), True, (255, 255, 255))
        text_lvl = FONT.render("Level: " + str(lvlCount), True, (255, 255, 255))
        text_life = FONT.render("Life: " + str(life), True, (255, 255, 255))
        return text_score, text_lvl, text_life

    text_score, text_lvl, text_life = update_texts()

    Run = True
    while Run:
        window.fill((0,0,0))
        window.blit(background, (0,0))
        dt = clock.tick(FPS) / 1000.0  # segundos desde o último frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameoverScreen(text_score, text_lvl)
                Run = False

        keybind = pygame.key.get_pressed()
        if (keybind[pygame.K_UP] or keybind[pygame.K_w]) and playerY >= 0:
            playerY -= speed * dt * 60
        if (keybind[pygame.K_DOWN] or keybind[pygame.K_s]) and playerY <= WIN_Y - playerShip.get_height():
            playerY += speed * dt * 60
        if (keybind[pygame.K_RIGHT] or keybind[pygame.K_d]) and playerX <= WIN_X - playerShip.get_width():
            playerX += speed * dt * 60
        if (keybind[pygame.K_LEFT] or keybind[pygame.K_a]) and playerX >= 0:
            playerX -= speed * dt * 60
        if keybind[pygame.K_ESCAPE]:
            paused()

        # aumenta a quantidade de asteroides ativos com o nível
        active_objects = min(MAX_OBJECTS, 5 + lvlCount * 2)

        for i in range(active_objects):
            if objectY[i] >= WIN_Y + 200:
                objectY[i] = uniform(-800, -1000)
                objectX[i] = uniform(0, WIN_X)
            objectY[i] += (objectY_move[i] + lvlCount) * dt * 60  # aumenta velocidade com o nível
            print(objectY[i])

            if isCollision(objectX[i], objectY[i], playerX, playerY):
                if explosionSound:
                    explosionSound.play()
                objectX[i] = random.uniform(0, WIN_X)
                objectY[i] = random.uniform(-2200, -3000)
                life -= 1
                playerX = WIN_X/2-50
                playerY = WIN_Y/2+150
                text_score, text_lvl, text_life = update_texts()
                if life <= 0:
                    final_score_txt = FONT.render("Score: " + str(clockSec), True, (255,255,255))
                    final_level_txt = FONT.render("Level: " + str(lvlCount), True, (255,255,255))
                    GameoverScreen(final_score_txt, final_level_txt)
                    Run = False
                    break
            objects(objectX[i], objectY[i], i)

        if timer < 20:
            timer += 1
        else:
            clockSec += 10
            timer = 0
            text_score, text_lvl, text_life = update_texts()

        if lvl < 200:
            lvl += 1
        else:
            lvlCount += 1
            lvl = 0
            text_score, text_lvl, text_life = update_texts()

        
        player(playerX, playerY)
        if HUD:
            window.blit(HUD, (0,0))
        window.blit(text_score, (50, 40))
        window.blit(text_lvl, (50, 75))
        window.blit(text_life, (50, 110))

        pygame.display.update()
        clock.tick(FPS)


# ------------------------ Loop principal ------------------------
def main():
    try:
        # Coloca as fontes já definidas (poderia ser refeito aqui se quiser)
        Startscreen()
    except Exception as e:
        print("Erro fatal no jogo:", e)
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
