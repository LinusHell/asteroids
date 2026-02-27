import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}",f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()  #Initialises pygame

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_clock = pygame.time.Clock() 
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable,drawable)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = (updatable,)

    asteroidfield = AsteroidField()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        updatable.update(dt)

        for item in drawable:
            item.draw(screen)

        pygame.display.flip()

        #Let 1/60 th of a second pass, and records the actual time that passed:
        dt = game_clock.tick(60) / 1000 
    



if __name__ == "__main__":
    main()
