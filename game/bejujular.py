import pygame
from pygame.locals import *
import random as R
import numpy as np

gridSize = [8, 8]
windowWidth = 800
windowHeight = 800
border = 10
cellLineThickness = 5
pieceTypes = ['circle', 'triangle', 'star', 'pentagon', 'hexagon', 'diamond']

class bejujular:
    def __init__(self):
        self.running = True
        self.displaySurf = None
        self.imageSurf = None

    def onInit(self):
        pygame.init()
        self.displaySurf = pygame.display.set_mode((windowWidth, windowHeight), pygame.HWSURFACE)
        self.running = True
        self.grid = pygame.image.load("./assets/grid.png").convert()
        occupationMatrix = np.zeros(gridSize)
        self.pieces = []
        for pieceNumber in range(gridSize[0] * gridSize[1]):
            pieceType = R.choice(pieceTypes)
            self.pieces.append(gamePiece("./assets/" + pieceType + ".png", occupationMatrix))

    def onEvent(self, event):
        if event.type == QUIT:
            self.running = False

    def onLoop(self):
        pass

    def onRender(self):
        self.displaySurf.blit(self.grid, (border, border))
        for piece in self.pieces:
            self.displaySurf.blit(piece.renderObject, (piece.x, piece.y))
        pygame.display.flip()

    def onCleanup(self):
        pygame.quit()

    def onExecute(self):
        if self.onInit() == False:
            self.running = False

        while self.running:
            for event in pygame.event.get():
                self.onEvent(event)
            self.onLoop()
            self.onRender()
        self.onCleanup()


class gamePiece:
    def __init__(self, imageLoc, occupationMatrix):
        while True:
            gridPosnX = R.randint(0, occupationMatrix.shape[0] - 1)
            gridPosnY = R.randint(0, occupationMatrix.shape[1] - 1)
            if occupationMatrix[gridPosnX, gridPosnY] == 0:
                occupationMatrix[gridPosnX, gridPosnY] = 1
                break
        [self.x, self.y] = self.getPixelPosn([gridPosnX, gridPosnY])
        self.occupationMatrix = occupationMatrix
        self.renderObject = pygame.image.load(imageLoc).convert()

    def getPixelPosn(self, gridPosn):
        # Pieces are 85x85 pixels.
        # Top left of grid is at border + cellLineThickness
        # Grid extent = border + cellLineThickness to windowWidth - border
        #print(windowWidth - border)
        #print(border + cellLineThickness)
        #print(np.round(float((windowWidth - border) - (border + cellLineThickness)) / float(gridSize[0])))
        #print(gridPosn[0])
        #exit()
        pixelX = (border + cellLineThickness) + (gridPosn[0] * (np.round(float((windowWidth - border) - (border + cellLineThickness)) / float(gridSize[0])))) + 5
        pixelY = (border + cellLineThickness) + (gridPosn[1] * (np.round(float((windowWidth - border) - (border + cellLineThickness)) / float(gridSize[1])))) + 7
        return [pixelX, pixelY]


if __name__ == "__main__":
    R.seed(928345097818235460)
    game = bejujular()
    game.onExecute()
