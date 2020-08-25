import sys
import time
import pygame

class Object:
    def __init__(self, face_paths):
        self.faces = []
        for state in face_paths:
            self.faces.append([])
            for face_path in state:
                self.faces[-1].append(pygame.image.load(face_path))
                self.faces[-1][-1].set_alpha(None)
                self.faces[-1][-1].set_colorkey((255, 0, 255))
        self.visible = False
        self.pos_x = 50
        self.pos_y = 50
        self.direction = 0 #0 = direct, 1 = right, -1 = left
        self.state = 0
        self.control_perm = 0 #0 = can walk and attack, 1 = can't attack, 2 = can't walk or attack
        self.face_i = 0
        self.face_change = 1.0 #for available state, this determines how frequently is face changed if faceswitch == True
        self.faceswitch = False

    def get_face(self):
        return(self.faces[self.state][self.face_i])

    def change_direction(self, new_direction):
        self.direction = new_direction
