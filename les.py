import sys

import pygame
from pygame.image import load as load_image

FPS = 50
WIDTH, HEIGHT = SIZE = 500, 500
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    screen.fill((0, 0, 200))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    kk = []
    for y in range(len(level)):
        kk.append([])
        for x in range(len(level[y])):
            if level[y][x] == '.':
                kk[-1].append(Tile('empty', x, y))
            elif level[y][x] == '#':
                kk[-1].append(Tile('wall', x, y))
            elif level[y][x] == '@':
                kk[-1].append(Tile('empty', x, y))
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, kk


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.x = pos_x
        self.y = pos_y
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)



def move(x, y, delta_x, delta_y):
    global tttmtmt

    if tttmtmt[y + delta_y][x + delta_x] == '#':
        return x, y

    return x + delta_x, y + delta_y


if __name__ == '__main__':
    pygame.init()
    size = width, height = SIZE
    screen = pygame.display.set_mode(size)

    while True:
        n = input('Введите номер уровня (число от 0 до 4)\n\t-> ')
        try:
            player, level_x, level_y, mmm = generate_level(load_level(n))
            with open(n, 'r') as f:
                tttmtmt = f.read().split()
            break
        except Exception:
            print('Введено неверное число или не число вообще!\nПопробуйте снова\n')

    bg = pygame.Surface((500, 500))

    for i in enumerate(mmm):
        for j in enumerate(i[1]):
            bg.blit(j[1].image, j[1].rect)

    print(mmm)

    running = True
    start_screen()
    while running:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player = Player(*move(player.x, player.y, 0, -1))
                if event.key == pygame.K_DOWN:
                    player = Player(*move(player.x, player.y, 0, 1))
                if event.key == pygame.K_LEFT:
                    player = Player(*move(player.x, player.y, -1, 0))
                if event.key == pygame.K_RIGHT:
                    player = Player(*move(player.x, player.y, 1, 0))

        # отрисовка и изменение свойств объектов
        # ...

        screen.blit(bg, (0, 0))

        screen.blit(player.image, player.rect)

        # обновление экрана
        pygame.display.flip()
    pygame.quit()
