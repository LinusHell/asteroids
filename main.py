import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_DEATH_DELAY
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from logger import log_event

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}",f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()  #Initialises pygame
    

    
    

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.toggle_fullscreen()
    #TODO find a way to hide the mouse
    #screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #alternative for fullscreen?

    font = pygame.font.Font(None, 30)
    font_big = font = pygame.font.Font(None, 50)

    game_clock = pygame.time.Clock() 
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable,drawable)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = (updatable,)

    shots = pygame.sprite.Group()
    Shot.containers = (updatable,drawable,shots)

    asteroidfield = AsteroidField()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    player_alive = True
    score = 0
    score_change = True
    while player_alive:
        

        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        updatable.update(dt)

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    score += 1
                    score_change = True
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                player.death_animation()
                player.kill()
                asteroid.kill()
                player_alive = False
                # score -= 20 #alternative for developer mode
                
        
        

        for item in drawable:
            item.draw(screen)

        if score_change == True:
            score_surface = font.render(f"{score}",True, (255,255,255))
            score_change = False

        screen.blit(score_surface, (10, 10))

        pygame.display.flip()

        #Let 1/60 th of a second pass, and records the actual time that passed:
        dt = game_clock.tick(60) / 1000 

    end_text_surface = font_big.render(f"GAME OVER!",True, (255,255,255))
    escape_continue_surface = font_big.render(f"Press 'Enter' to exit.",True, (255,255,255))
    player_death_delay = 3
    
    while True:
        

        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        updatable.update(dt)

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.kill()
                    shot.kill()
                    score += 1
                    score_change = True
                
        
        

        for item in drawable:
            item.draw(screen)

        if score_change == True:
            score_surface = font.render(f"{score}",True, (255,255,255))
            endscore_surface = font_big.render(f"Your score is: {score}",True, (255,255,255))
            score_change = False


        if player_death_delay > 0:
            player_death_delay -= dt
            screen.blit(score_surface, (10, 10))
        else: 
            screen.blit(end_text_surface, (SCREEN_WIDTH / 2 -100, SCREEN_HEIGHT / 2-30))
            screen.blit(endscore_surface, (SCREEN_WIDTH / 2  -115, SCREEN_HEIGHT /2 + 20))
            screen.blit(escape_continue_surface, (SCREEN_WIDTH / 2 - 145, SCREEN_HEIGHT / 2  + 100))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                sys.exit()

        pygame.display.flip()

        #Let 1/60 th of a second pass, and records the actual time that passed:
        dt = game_clock.tick(60) / 1000 
        






    
    


if __name__ == "__main__":
    main()
