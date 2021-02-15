import block_library
import random

class Bad_Block(block_library.Block):

    def update(self):
        self.rect.y -= random.randrange(-5, 1)
        if self.rect.top > 920:
            self.rect.y = -50