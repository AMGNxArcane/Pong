"""generates training data"""

from ponggame import *
import threading

pygame.init()

class MyThread(threading.Thread):
    def __init__(self,threadid):
        threading.Thread.__init__(self)
        self.gameid = 0
        self.running = True
        self.threadid = threadid
        self.startNewGame()
        self.start()



    def run(self):
        while self.running:
            self.game.step()
            if self.game.steps > 5000:
                self.game.end()
                self.startNewGame()

    def startNewGame(self):
        self.game = Ponggame("data/log{}_{}.txt".format(self.threadid,self.gameid),Brain(None,0),Brain(None,0))
        self.gameid+=1

    def stop(self):
        self.running = False



# screen = pygame.display.set_mode([800,600])
#
# games = []
# for i in range(10000):
#     games.append(Ponggame("data/log{}.txt".format(i)))
#
# for steps in range(10000):
#     for game in games:
#         game.step()
#
# for game in games:
#     game.end()
#
# while True:
#     for event in pygame.event.get():
#        if event.type == (pygame.QUIT):
#            game.end()
#            exit()
#
#     screen.blit(game.draw(),(0,0,800,600))
#     pygame.display.update()

threads = []
for i in range(4):
    threads.append(MyThread(i))

input("Press Enter to stop...")
for t in threads:
    t.stop()
exit()
