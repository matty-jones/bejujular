import pygame
from pygame.locals import *
import random as R
import numpy as np

grid_size = [8, 8]
window_width = 800
window_height = 800
border = 10
cell_line_thickness = 5
piece_types = ["circle", "triangle", "star", "pentagon", "hexagon", "diamond"]


class bejujular:
    def __init__(self):
        self.running = True
        self.display_surf = None
        self.image_surf = None

    def on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode(
            (window_width, window_height), pygame.HWSURFACE
        )
        self.running = True
        grid = game_grid()
        self.grid = grid.grid
        self.pieces = grid.pieces

    def on_event(self, event):
        if event.type == QUIT:
            self.running = False
        if event.type == MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            print(position)

    def on_loop(self):
        pass

    def on_render(self):
        self.display_surf.blit(self.grid, (border, border))
        for piece in self.pieces:
            self.display_surf.blit(piece.render_object, (piece.x, piece.y))
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.running = False

        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


class game_piece:
    def __init__(self, image_loc, occupation_matrix):
        while True:
            self.grid_posn_x = R.randint(0, occupation_matrix.shape[0] - 1)
            self.grid_posn_y = R.randint(0, occupation_matrix.shape[1] - 1)
            if occupation_matrix[self.grid_posn_x, self.grid_posn_y] == 0:
                occupation_matrix[self.grid_posn_x, self.grid_posn_y] = 1
                break
        [self.x, self.y] = self.get_pixel_posn([self.grid_posn_x, self.grid_posn_y])
        self.occupation_matrix = occupation_matrix
        self.render_object = pygame.image.load(image_loc).convert()

    def get_pixel_posn(self, grid_posn):
        # Pieces are 85x85 pixels.
        # Top left of grid is at border + cell_line_thickness
        # Grid extent = border + cell_line_thickness to window_width - border
        pixel_x = (
            (border + cell_line_thickness)
            + (
                grid_posn[0]
                * (
                    np.round(
                        float((window_width - border) - (border + cell_line_thickness))
                        / float(grid_size[0])
                    )
                )
            )
            + 5
        )
        pixel_y = (
            (border + cell_line_thickness)
            + (
                grid_posn[1]
                * (
                    np.round(
                        float((window_width - border) - (border + cell_line_thickness))
                        / float(grid_size[1])
                    )
                )
            )
            + 7
        )
        return [pixel_x, pixel_y]


class game_grid:
    def __init__(self):
        self.grid = pygame.image.load("./assets/grid.png").convert()
        self.occupation_matrix = np.zeros(grid_size)
        self.pieces = []
        self.piece_coords = []
        for piece_number in range(grid_size[0] * grid_size[1]):
            piece_type = R.choice(piece_types)
            new_piece = game_piece("./assets/" + piece_type + ".png", self.occupation_matrix)
            self.pieces.append(new_piece)
            self.piece_coords.append((new_piece.x, new_piece.y))
        print(self.piece_coords)

    def find_nearest_piece(self, posn):
        pass




if __name__ == "__main__":
    R.seed(928345097818235460)
    game = bejujular()
    game.on_execute()
