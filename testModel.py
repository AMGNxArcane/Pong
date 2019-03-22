import tensorflow as tf
from tensorflow import keras
import pygame
from ponggame import *

pygame.init()

model = keras.models.load_model("model.h5")

pygame.init()
screen = pygame.display.set_mode([800,600])

game = Ponggame("test.txt",Brain(model,0),Brain(model,0))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    game.step()
    screen.blit(game.draw(),(0,0,800,600))
    pygame.display.update()
