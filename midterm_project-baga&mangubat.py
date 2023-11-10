import pygame
import sys
import random
import math
pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 60
#colors
green = (255, 255, 255)
red = (255, 0, 0)
#player
player_size = 10
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 10
#bullet
bullet_size = 5
bullet_speed = 20
bullets = []
#alien
alien_size = 15
alien_speed = 20  #adjusted alien speed
alien_change_direction_prob = 0.10  #probability of changing direction towards player
aliens = []
#initialize Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Shooting Game")
clock = pygame.time.Clock()
#score
score = 0
#constants
FIRE_RATE = 0.5  #number of seconds between shots
last_shot_time = 0  #time of the last shot
#game state
running = False
game_over = False
def spawn_aliens(pattern, count):
    aliens.clear()
    if pattern == "triangle":
        for i in range(count):
            x = i * (alien_size + 20) + 50
            y = random.randint(0, 100)  #random Y-coordinate within a certain range at the top of the screen
            aliens.append([x, y, 1, random.uniform(-alien_speed, alien_speed),
                           random.uniform(-alien_speed, alien_speed)])  #1 is the initial health of the alien
    elif pattern == "circle":
        for i in range(count):
            angle = i * (360 / count)
            x = WIDTH // 2 + int(150 * (1.5 * 3.1415 * angle / 180))
            y = random.randint(0, 100)  #random Y-coordinate within a certain range at the top of the screen
            aliens.append([x, y, 1, random.uniform(-alien_speed, alien_speed),
                           random.uniform(-alien_speed, alien_speed)])  #1 is the initial health of the alien
    #add more patterns as needed
def spawn_new_batch():
    #spawn a new batch of aliens with a random pattern and count
    patterns = ["triangle", "circle", "new_pattern"]  #add more patterns as needed
    pattern = random.choice(patterns)
    count = random.randint(5, 10)  #adjust the count as needed
    spawn_aliens(pattern, count)
def draw_aliens():
    for alien in aliens:
        pygame.draw.circle(screen, red, (int(alien[0]), int(alien[1])), alien_size)
def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, green, (int(bullet[0]), int(bullet[1]), bullet_size, bullet_size))
def game_over_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, green)
    screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(2000)
def update_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, green)
    screen.blit(score_text, (10, 10))
def move_towards_player(alien, player_pos):
    angle = math.atan2(player_pos[1] - alien[1], player_pos[0] - alien[0])
    alien[0] += alien[3]  #alien[3] is the x-speed
    alien[1] += alien[4]  #alien[4] is the y-speed
def bounce_alien(alien):
    #Reverse the direction of the alien
    alien[3] *= -1  #Reverse x-speed
    alien[4] *= -1  #Reverse y-speed
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Check if Enter key is pressed
                if not running and not game_over:
                    running = True
                    spawn_aliens("triangle", 7)

    screen.fill((0, 0, 0))

    if running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > player_speed:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size - player_speed:
            player_pos[0] += player_speed

        #shoot bullets
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks() / 1000  # Convert milliseconds to seconds
            #check if enough time has passed since the last shot
            if current_time - last_shot_time >= FIRE_RATE:
                bullets.append([player_pos[0] + player_size // 2, player_pos[1]])
                last_shot_time = current_time

        #update bullets
        bullets = [[x, y - bullet_speed] for x, y in bullets]

        #update aliens
        for alien in aliens:
            if random.random() < alien_change_direction_prob:
                move_towards_player(alien, player_pos)

            #check collision with bullets
            for bullet in bullets:
                if (
                        alien[0] < bullet[0] < alien[0] + alien_size
                        and alien[1] < bullet[1] < alien[1] + alien_size
                ):
                    #collision detected
                    bullets.remove(bullet)
                    alien[2] -= 1  #decrease the health of the alien
                    score += 2
                    update_score()

                    #remove the alien if its health is zero
                    if alien[2] <= 0:
                        aliens.remove(alien)

            #check collision with player line
            if (
                    player_pos[0] < alien[0] < player_pos[0] + player_size
                    and player_pos[1] < alien[1] < player_pos[1] + player_size
            ):
                running = False
                game_over = True

            #bounce when hitting the edges
            if alien[0] <= 0 or alien[0] >= WIDTH - alien_size:
                bounce_alien(alien)
            if alien[1] <= 0 or alien[1] >= HEIGHT - alien_size:
                bounce_alien(alien)

        #check if aliens are all killed
        if not aliens:
            score += len(aliens) * 2
            spawn_new_batch()
        # draw player
        pygame.draw.rect(screen, green, (int(player_pos[0]), int(player_pos[1]), player_size, player_size))
        #draw aliens
        draw_aliens()
        #draw bullets
        draw_bullets()
        #draw score
        update_score()
        pygame.display.flip()
        clock.tick(FPS)
        #check if the player reached a score of 100
        if score >= 100:
            running = False
            game_over = True
    elif game_over:
        game_over_screen()
        pygame.quit()
        sys.exit()
    else:
        font = pygame.font.Font(None, 36)
        text = font.render("Press Enter to Start", True, green)
        screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()
        clock.tick(FPS)