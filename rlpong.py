from scipy import *
import matplotlib.pyplot as plt
from pybrain.rl.environments import Environment, Task
from pybrain.rl.learners.valuebased import ActionValueTable
from pybrain.rl.agents import LearningAgent
from pybrain.rl.learners import Q, SARSA #@UnusedImport
from pybrain.rl.experiments import Experiment
import pygame
import numpy as np
plt.gray()
plt.ion()

class Pong(Environment):

    def __init__(self):
        self.width,self.height = 800,600
        self.leftPaddle = pygame.Rect([50,self.height/2,20,50])
        self.rightPaddle = pygame.Rect([self.width-70,self.height/2,20,50])
        self.setBall()
        self.steps = 0
        self.leftDir = 0
        self.rightDir = 0
        self.score = [0,0]


    def setBall(self):
        self.ballPos = pygame.math.Vector2(self.width/2,self.height/2)
        self.ballSpeed = pygame.math.Vector2(1,0)
        angle = random.randint(0,360)
        self.ballSpeed = self.ballSpeed.rotate(angle)*2

    def getSensors(self):
        print("getSensor")
        self.ballPos += self.ballSpeed
        self.leftPaddle[1] += self.leftDir
        self.rightPaddle[1] += self.rightDir
        if self.leftPaddle[1]+self.leftPaddle[3] > self.height:
            self.leftPaddle[1]-=1
        if self.leftPaddle[1]<0:
            self.leftPaddle[1]+=1
        if self.rightPaddle[1]+self.rightPaddle[3] > self.height:
            self.rightPaddle[1]-=1
        if self.rightPaddle[1]<0:
            self.rightPaddle[1]+=1
        if self.ballPos.y > self.height or self.ballPos.y<0:
            self.ballSpeed.y*=-1
        if self.ballPos.x < 0:
            self.score[1]+=1
            self.setBall()
        if self.ballPos.x > self.width:
            self.score[0]+=1
            self.setBall()
        if self.leftPaddle.collidepoint(self.ballPos) or self.rightPaddle.collidepoint(self.ballPos):
            self.ballSpeed.x *= -1

        self.steps+=1
        return np.array([self.leftPaddle[1],self.ballPos.x,self.ballPos.y,self.ballSpeed.x,self.ballSpeed.y])

    def performAction(self,action):
        print("performAction")
        a = np.argmax(action)-1
        self.leftDir = a
        y = self.rightPaddle[1]
        if y < ballPos.y:
            self.rightDir = 1
        else:
            self.rightDir = -1

    def reset(self):
        self.__init__()


class PongTask(Task):
    def __init(self,environment):
        super.__init__(environment)

    def getReward(self):
        score = self.env.score
        return score[0]-score[1]


environment = Pong()
controller = ActionValueTable(5,3)
controller.initialize(1.)
learner = Q()
agent = LearningAgent(controller, learner)
task = PongTask(environment)

experiment = Experiment(task,agent)
while True:
    experiment.doInteractions(100)
    agent.learn()
    agent.reset()
    pylab.pcolor(controller.params.reshape(5,3).max(1).reshape(9,9))
    pylab.draw()
