#i want to add a lot more to this game like buying moreland and a crop shop that you have to walk to on the left to open ui and sell crops at a vender on the right and im sure more ideas will come to me as i build and whatnot

import pygame
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TILE_SIZE = 64
FARM_COLUMNS = 8
FARM_ROWS = 5
MAX_GROWTH_STAGE = 3
SECONDS_PER_STAGE = 5


farm_width = FARM_COLUMNS * TILE_SIZE
farm_height = FARM_ROWS * TILE_SIZE

farm_x = (SCREEN_WIDTH - farm_width) // 2
farm_y = (SCREEN_HEIGHT - farm_height) // 2

farm_tiles = []
watered_tiles = []
fertilized_tiles = []
planted_tiles = []
growth_stages = []
growth_timers = []


for row in range(FARM_ROWS):
    for column in range(FARM_COLUMNS):
        tile_x = farm_x + column * TILE_SIZE
        tile_y = farm_y + row * TILE_SIZE

        tile = pygame.Rect(tile_x, tile_y, TILE_SIZE, TILE_SIZE)
        farm_tiles.append(tile)
        watered_tiles.append(False)
        planted_tiles.append(False)
        growth_stages.append(0)
        growth_timers.append(0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Farming With Bobo")

clock = pygame.time.Clock()

player = pygame.Rect(450, 250, 40, 40)
player_speed = 250
crops_collected = 0


running = True

while running:
    delta_time = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = event.pos

            for index, tile in enumerate(farm_tiles):
                if tile.collidepoint(mouse_position):

                    if event.button == 1:
                        watered_tiles[index] = True

                    if event.button == 3:
                        if (
                            planted_tiles[index]
                            and growth_stages[index] == MAX_GROWTH_STAGE
                        ):
                            planted_tiles[index] = False
                            growth_stages[index] = 0
                            growth_timers[index] = 0
                            crops_collected += 1

                            print("Crops collected:", crops_collected)

                        elif (
                            watered_tiles[index]
                            and not planted_tiles[index]
                        ):
                            planted_tiles[index] = True
                            growth_stages[index] = 0
                            growth_timers[index] = 0

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player.y -= player_speed * delta_time
    if keys[pygame.K_s]:
        player.y += player_speed * delta_time
    if keys[pygame.K_a]:
        player.x -= player_speed * delta_time
    if keys[pygame.K_d]:
        player.x += player_speed * delta_time
        
    player.clamp_ip(screen.get_rect())
    for index in range(len(farm_tiles)):
        if (
            planted_tiles[index]
            and watered_tiles[index]
            and growth_stages[index] < MAX_GROWTH_STAGE
        ):
            growth_timers[index] += delta_time

            if growth_timers[index] >= SECONDS_PER_STAGE:
                growth_timers[index] -= SECONDS_PER_STAGE
                growth_stages[index] += 1
    screen.fill((110, 180, 90))

    for index, tile in enumerate(farm_tiles):
        if watered_tiles[index]:
            tile_color = (75, 65, 50)
        else:
            tile_color = (125, 75, 40)

        pygame.draw.rect(screen, tile_color, tile)
        pygame.draw.rect(screen, (90, 50, 25), tile, 2)
        if planted_tiles[index]:
            stage = growth_stages[index]

            if stage == 0:
                pygame.draw.circle(
                    screen,
                    (235, 205, 90),
                    tile.center,
                    5
                )

            elif stage == 1:
                pygame.draw.line(
                    screen,
                    (50, 150, 60),
                    (tile.centerx, tile.centery + 8),
                    (tile.centerx, tile.centery - 8),
                    4
                )

                pygame.draw.circle(
                    screen,
                    (70, 185, 75),
                    (tile.centerx - 6, tile.centery - 5),
                    5
                )

            elif stage == 2:
                pygame.draw.circle(
                    screen,
                    (70, 180, 75),
                    tile.center,
                    13
                )

                pygame.draw.line(
                    screen,
                    (40, 120, 45),
                    (tile.centerx, tile.centery + 15),
                    (tile.centerx, tile.centery - 10),
                    5
                )

            elif stage == 3:
                pygame.draw.circle(
                    screen,
                    (235, 145, 45),
                    tile.center,
                    18
                )

                pygame.draw.circle(
                    screen,
                    (55, 165, 65),
                    (tile.centerx, tile.centery - 16),
                    7
                )

    pygame.draw.rect(screen, (70, 100, 220), player)

    pygame.display.update()

pygame.quit()
