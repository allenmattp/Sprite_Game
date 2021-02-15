import block_library
import random
import math

class Good_Block(block_library.Block):

    def __init__(self, filename):
        super().__init__(filename)
        self.center_x = 0
        self.center_y = 0

        self.angle = 0
        self.radius = 0
        self.speed = 0.05

    def update(self):
        self.rect.x = self.radius * math.sin(self.angle) + self.center_x
        self.rect.y = self.radius * math.cos(self.angle) + self.center_y

        self.angle += self.speed