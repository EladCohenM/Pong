from lib2to3.pygram import python_grammar_no_print_statement
from tkinter.messagebox import NO
import pygame
import sys
import random
from pygame import key

from pygame.constants import K_DOWN, K_UP, KEYDOWN

# general setup
pygame.init()
clock = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont("Assistant", 40)

# setting up the window
screen_width = 1200
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

dark_blue = (27, 35, 43)
bg_color = pygame.Color('#2F373F')
orange = (229, 124, 0)

opponent = pygame.Rect(10, 325-75, 10, 150)
player = pygame.Rect(screen_width - 20, 325-75, 10, 150)
ball = pygame.Rect(600-15, 325-15, 30, 30)

ball_vel_x = 7
ball_vel_y = 7
player_vel = 7
opponent_vel = 7

player_score = 0
opponent_score = 0
score_time = True
counter = ""

pong_sound = pygame.mixer.Sound("pong.mp3")
score_sound = pygame.mixer.Sound("score.wav")

# functions


def ball_movement():
    global ball_vel_x, ball_vel_y, score_time, opponent_score, player_score
    if ball.right >= screen_width:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        opponent_score += 1
    elif ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        score_time = pygame.time.get_ticks()
        player_score += 1

    if ball.bottom >= screen_height:
        ball.bottom = screen_height
        ball_vel_y *= -1
    elif ball.top <= 0:
        ball. top = 0
        ball_vel_y *= -1

    if ball.colliderect(player):
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 15 and ball_vel_x > 0:
            ball_vel_x *= -1
        if abs(ball.bottom - player.top) < 15 and ball_vel_y > 0:
            ball_vel_y *= -1
        if abs(ball.top - player.bottom) < 15 and ball_vel_y < 0:
            ball_vel_y *= -1

    if ball.colliderect(opponent):
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 15 and ball_vel_x < 0:
            ball_vel_x *= -1
        if abs(ball.bottom - opponent.top) < 15 and ball_vel_y > 0:
            ball_vel_y *= -1
        if abs(ball.top - opponent.bottom) < 15 and ball_vel_y < 0:
            ball_vel_y *= -1

    ball.x += ball_vel_x
    ball.y += ball_vel_y


def player_movement():
    global player_vel

    keys = pygame.key.get_pressed()
    if keys[K_UP]:
        player.y += -player_vel
    if keys[K_DOWN]:
        player.y += player_vel

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_movement():
    if opponent.bottom < ball.top:
        opponent.y += opponent_vel
    elif opponent.top > ball.bottom:
        opponent.y += -opponent_vel

    if opponent.top < 0:
        opponent.top = 0
    if opponent.bottom > screen_height:
        opponent.bottom = screen_height


def ball_start():
    global ball_vel_x, ball_vel_y, score_time, counter
    ball.center = (screen_width/2, screen_height/2)
    current_time = pygame.time.get_ticks()
    delta = current_time - score_time

    if delta < 3000:
        ball_vel_x, ball_vel_y = 0, 0
    else:
        ball_vel_x = 7 * random.choice([-1, 1])
        ball_vel_y = 7 * random.choice([-1, 1])
        score_time = None

    if delta < 1000:
        counter = "Begins in 3"
    elif 1000 < delta < 2000:
        counter = "Begins in 2"
    elif 2000 < delta < 3000:
        counter = "Begins in 1"
    else:
        counter = ""


# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            break

    # game logic
    ball_movement()
    player_movement()
    opponent_movement()

    # visaulize
    opponent_text = font.render(
        f"opponent score: {opponent_score}", True, dark_blue)
    player_text = font.render(
        f"player score: {player_score}", True, dark_blue)
    counter_text = font.render(f"{counter}", True, dark_blue)

    screen.fill(color=bg_color)
    screen.blit(opponent_text, (15, 15))
    screen.blit(player_text, (screen_width - player_text.get_width() - 15, 15))
    screen.blit(counter_text, (screen_width/2 -
                counter_text.get_width()/2, screen_height/2 + 40))
    if score_time:
        ball_start()
    pygame.draw.rect(screen, orange, opponent)
    pygame.draw.rect(screen, orange, player)
    pygame.draw.aaline(screen, dark_blue, (600, 0), (600, screen_height))
    pygame.draw.ellipse(screen, orange, ball)
    pygame.display.update()

    clock.tick(fps)
