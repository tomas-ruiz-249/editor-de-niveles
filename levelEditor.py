import pickle
import pygame
import button
import csv

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode(
    (SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('El mejor grupo')

# Variables globales
ROWS = 100
MAX_COLS = 100
TILE_SIZE = 60
TILE_TYPES = 3
TILE_WALLS = 4
level = 0
current_tile = 1
scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
scroll_x = 0
scroll_y = 0
scroll_speed = 1
# player_placed = False
mouse_clicked = False

floating_items = []

# Lista de im�genes
img_list = []
for x in range(1, TILE_TYPES + 1):
    img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

for x in range(1, TILE_WALLS + 1):
    img = pygame.image.load(f'img/walls/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('img/save_btn.png').convert_alpha()
load_img = pygame.image.load('img/load_btn.png').convert_alpha()

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# Fuentes
font = pygame.font.SysFont('arcade', 32)

maps = []
items = []
# Crear un mapa vac�o
world_data = []
for row in range(ROWS):
    r = [0] * MAX_COLS
    world_data.append(r)
maps.append(world_data)
items.append(floating_items)

# Generar suelo
for tile in range(MAX_COLS):
    world_data[ROWS - 1][tile] = 0

# Funci�n para mostrar texto


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Dibujar fondo


def draw_bg():
    screen.fill(BLACK)

# Dibujar cuadr�cula ajustada


def draw_grid():
    for c in range(MAX_COLS + 1):
        x_pos = c * TILE_SIZE - scroll_x
        if x_pos < SCREEN_WIDTH:
            pygame.draw.line(screen, WHITE, (x_pos, 0), (x_pos, SCREEN_HEIGHT))
    for c in range(ROWS + 1):
        y_pos = c * TILE_SIZE - scroll_y
        if y_pos < SCREEN_HEIGHT:
            pygame.draw.line(screen, WHITE, (0, y_pos), (SCREEN_WIDTH, y_pos))

# Dibujar el mapa


def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile > 0:
                screen.blit(
                    img_list[tile - 1], (x * TILE_SIZE - scroll_x, y * TILE_SIZE - scroll_y))


# Ajustar tama�os
save_img = pygame.transform.scale(save_img, (270, 210))
load_img = pygame.transform.scale(load_img, (270, 210))

# Cambiar posiciones
save_button = button.Button(440, 585, save_img, 1)
load_button = button.Button(700, 585, load_img, 1)

# Lista de botones para los tiles
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(
        SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

# Bucle principal
run = True
while run:
    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    draw_text('Presione A o D para cambiar de nivel', font,
              WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 75)
    draw_text(f'Nivel: {level}', font, WHITE, 10,
              SCREEN_HEIGHT + LOWER_MARGIN - 45)

    # Dibujar �tems flotantes
    for item in floating_items:
        item_type, item_x, item_y = item
        screen.blit(img_list[item_type - 1], (item_x - scroll_x -
                    TILE_SIZE / 2, item_y - scroll_y - TILE_SIZE / 2))
    # Guardar y cargar datos
    if save_button.draw(screen):
        with open(f'output/map{level}.txt', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in maps[level]:
                transformed_row = [1 if tile == 4 else 2 if tile ==
                                   5 else 3 if tile == 6 else 4 if tile == 7 else tile for tile in row]
                writer.writerow(transformed_row)

        with open(f'output/items{level}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for item in items[level]:
                item_type = item[0]
                item_x = float(item[1] / TILE_SIZE)
                item_y = float(item[2] / TILE_SIZE)

                writer.writerow([item_type, item_x, item_y])

    if load_button.draw(screen):
        with open(f'output/map{level}.txt', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            world_data = []
            for row in reader:
                transformed_row = [4 if tile == '1' else 5 if tile == '2' else 6 if tile == '3' else 7 if tile == '4' else 0 for tile in row]
                world_data.append([int(tile) for tile in transformed_row])
            maps[level] = world_data
        with open(f'output/items{level}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            floating_items.clear()
            for row in reader:
                print(row)
                item_type = int(row[0])
                item_x = float(row[1]) * TILE_SIZE
                item_y = float(row[2]) * TILE_SIZE

                floating_items.append([item_type, item_x, item_y])
            items[level] = floating_items

    # Botones
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH,
                     0, SIDE_MARGIN, SCREEN_HEIGHT))
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count + 1

    # Resaltar el mosaico seleccionado
    pygame.draw.rect(screen, RED, button_list[current_tile - 1].rect, 3)

    # Desplazamiento del mapa
    if scroll_left and scroll_x > 0:
        scroll_x -= 5 * scroll_speed
    if scroll_right and scroll_x < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll_x += 5 * scroll_speed
    if scroll_up and scroll_y > 0:
        scroll_y -= 5 * scroll_speed
    if scroll_down and scroll_y < (ROWS * TILE_SIZE) - SCREEN_HEIGHT:
        scroll_y += 5 * scroll_speed

    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll_x) // TILE_SIZE
    y = (pos[1] + scroll_y) // TILE_SIZE
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        if pygame.mouse.get_pressed()[0] == 1:
            if current_tile in [1, 2, 3]:
                item_x = (pos[0] + scroll_x)
                item_y = (pos[1] + scroll_y)
                if world_data[y][x] in [0, 1, 2, 3]:
                    if not any(item[0] == current_tile and abs(item[1] - item_x) < TILE_SIZE and abs(item[2] - item_y) < TILE_SIZE for item in floating_items):
                        floating_items.append([current_tile, item_x, item_y])
            # elif current_tile == 1 and not player_placed:
                # if world_data[y][x] == 0:
                    # world_data[y][x] = current_tile
                    # player_placed = True
            elif current_tile in [4, 5, 6, 7]:
                world_data[y][x] = current_tile
                floating_items = [item for item in floating_items if not (
                    abs(item[1] - (x * TILE_SIZE + TILE_SIZE / 2)) <= TILE_SIZE / 2 and
                    abs(item[2] - (y * TILE_SIZE + TILE_SIZE / 2)) <= TILE_SIZE / 2)]
                mouse_clicked = True

        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = 0
            floating_items = [item for item in floating_items if not (
                abs(item[1] - (x * TILE_SIZE + TILE_SIZE / 2)) <= TILE_SIZE / 2 and
                abs(item[2] - (y * TILE_SIZE + TILE_SIZE / 2)) <= TILE_SIZE / 2)]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                scroll_up = True
            if event.key == pygame.K_DOWN:
                scroll_down = True
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                scroll_speed = 5
            if event.key == pygame.K_d:
                level += 1

                #añadir mapa nuevo si no existe
                if level > len(maps) - 1:
                    new_map = []
                    for row in range(ROWS):
                        r = [0] * MAX_COLS
                        new_map.append(r)
                    maps.append(new_map)
                world_data = maps[level]
                
                #añadir items nuevos si no existen
                if level > len(items) - 1:
                    new_items = []
                    items.append(new_items)
                floating_items = items[level]
                    
            if event.key == pygame.K_a and level > 0:
                level -= 1
                world_data = maps[level]
                floating_items = items[level]
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                scroll_up = False
            if event.key == pygame.K_DOWN:
                scroll_down = False
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                scroll_speed = 1
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_clicked = False

    pygame.display.update()
