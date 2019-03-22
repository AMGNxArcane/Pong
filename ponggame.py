import pygame
import random
import numpy as np
import os
import tensorflow as tf


class Ponggame:
    def __init__(self,filename,brain1,brain2):
        self.width,self.height = 800,600
        self.leftPaddle = pygame.Rect([50,self.height/2,20,50])
        self.rightPaddle = pygame.Rect([self.width-70,self.height/2,20,50])
        self.setBall()
        self.steps = 0
        self.leftDir = 0
        self.rightDir = 0
        self.score = [0,0]
        self.filename = filename

        self.file1 = ""#open(filename+"0.txt","w")
        self.file2 = ""#open(filename+"1.txt","w")
        self.brain1 = brain1
        self.brain2 = brain2

    def setBall(self):
        self.ballPos = pygame.math.Vector2(self.width/2,self.height/2)
        self.ballSpeed = pygame.math.Vector2(1,0)
        angle = random.randint(0,360)
        self.ballSpeed = self.ballSpeed.rotate(angle)*2


    def step(self):
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

        if self.steps % 5 == 0:
            self.choice()
        self.steps+=1

    def choice(self):
        leftState = [self.leftPaddle[1],self.ballPos.x,self.ballPos.y,self.ballSpeed.x,self.ballSpeed.y]
        rightState =[self.rightPaddle[1],self.width-self.ballPos.x,self.ballPos.y,self.ballSpeed.x*-1,self.ballSpeed.y]
        c1 = self.brain1.predict(leftState)
        c2 = self.brain2.predict(rightState)


        #s1 = str(self.steps)+","+str(c1)+","+str(leftState)+"\n"
        #s2 = str(self.steps)+","+str(c2)+","+str(rightState)+"\n"
        s1 = str(self.steps)+","+str(c1)
        for x in leftState:
            s1 += ","+str(x)

        s2 = str(self.steps)+","+str(c2)
        for x in rightState:
            s2 += ","+str(x)
        self.file1 += s1+"\n"
        self.file2 += s2+"\n"
        #self.file1.write(s1)
        #self.file2.write(s2)
        self.leftDir = c1
        self.rightDir = c2

    def end(self):
        string = ""
        winner = None
        if self.score[0] > self.score[1]:
            string = self.file1
            winner = 0
        elif self.score[0] < self.score[1]:
            string = self.file2
            winner = 1
        else:
            return None

        with open(self.filename,"w") as f:
            f.write("Winner:"+str(winner)+" Score:"+str(self.score)+"\n")
            f.write(string)
        return winner






    def draw(self):
        canvas = pygame.Surface((self.width,self.height))
        canvas.fill((0,0,0))
        COLOR = (255,255,255)
        pygame.draw.rect(canvas,COLOR,self.leftPaddle)
        pygame.draw.rect(canvas,COLOR,self.rightPaddle)
        pos = (int(self.ballPos.x),int(self.ballPos.y))
        pygame.draw.circle(canvas,COLOR,pos,1)
        return canvas


class Brain:
    """generates choices with predict"""
    def __init__(self,model,randPercent):
        """pass in none for the model to generate randomChoices"""
        self.randPercent=randPercent
        self.model = model

    def predict(self,input):
        if self.model:
            if random.random() < self.randPercent:
                return random.randint(-1,1)
            input = np.array(input).reshape(-1,5)
            return np.argmax(self.model.predict(input))-1
        else:
            return random.randint(-1,1)
