"""
Sprite collecting game, developed as part of:

http://programarcadegames.com/
http://simpson.edu/computer-science/
"""

from block_library import *
from goodblock_library import *
from badblock_library import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 41, 188)
GREEN = (0, 255, 0)


class Player(pygame.sprite.Sprite):
    """ This class is the player-controlled sprite. """

    # -- Methods:
    def __init__(self, filename, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.image.load(filename).convert()
        self.image.set_colorkey(BLACK)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0

    def changespeed(self, x, y):
        """ Change the speed of the player"""
        self.change_x += x
        self.change_y += y

    def update(self):
        """ Find a new position for the player"""
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        if self.rect.right >= screen_width:
            self.rect.x -= 5
            bump_sound.play()

        if self.rect.left <= 0:
            self.rect.x += 5
            bump_sound.play()

        if self.rect.top <= 0:
            self.rect.y += 5
            bump_sound.play()

        if self.rect.bottom >= screen_height:
            self.rect.y -= 5
            bump_sound.play()


# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode([screen_width, screen_height])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
good_block_list = pygame.sprite.Group()
bad_block_list = pygame.sprite.Group()

# This is a list of every sprite.
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

for i in range(25):
    # This represents a good block
    block = Good_Block("assets\\good_block.png")

    # Set a random center location for the block
    block.center_x = random.randrange(screen_width)
    block.center_y = random.randrange(screen_height)
    # Random radius
    block.radius = random.randrange(10, 200)
    # Random start angle
    block.angle = random.random() * 2 * math.pi
    # radians per frame
    block.speed = 0.008

    # Add the block to the list of objects
    good_block_list.add(block)
    all_sprites_list.add(block)

for i in range(25):
    # This represents a bad block
    block = Bad_Block("assets\\bad_block.png")

    # Set a random location for the block
    block.rect.x = random.randrange(0, screen_width - 20)
    block.rect.y = random.randrange(0, screen_height - 15)

    # Add the block to the list of objects
    bad_block_list.add(block)
    all_sprites_list.add(block)

# Create a RED player block
player = Player("assets\\player.png", 20, 15)
all_sprites_list.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

font = pygame.font.SysFont('trebuchetms', 25, True, False)
ouch_font = pygame.font.SysFont('impact', 350, True, False)
game_over_font = pygame.font.SysFont('trebuchetms', 50, True, False)
good_sound = pygame.mixer.Sound("assets\\good_block.wav")
bad_sound = pygame.mixer.Sound("assets\\bad_block.wav")
bump_sound = pygame.mixer.Sound("assets\\bump.wav")
game_over_sound = pygame.mixer.Sound("assets\\tada.wav")

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set speed based on key pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, 3)

        # Reset speed when key is released
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, 3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -3)

    all_sprites_list.update()

    # Clear the screen
    screen.fill(BLUE)

    # Get the current mouse position. This returns the position
    # as a list of two numbers.
    # pos = pygame.mouse.get_pos()

    # Fetch the x and y out of the list,
    # just like we'd fetch letters out of a string.
    # Set the player object to the mouse location
    # player.rect.x = pos[0]
    # player.rect.y = pos[1]

    # See if the player block has collided with anything.
    good_blocks_hit_list = pygame.sprite.spritecollide(player, good_block_list, True)
    bad_blocks_hit_list = pygame.sprite.spritecollide(player, bad_block_list, True)

    # Check the list of collisions.
    for block in good_blocks_hit_list:
        score += 1
        good_sound.play()
        print("Yay!", score)

    for block in bad_blocks_hit_list:
        score -= 1
        bad_sound.play()
        ouch = ouch_font.render("Ouch!", True, BLACK)
        screen.blit(ouch, [(screen_width // 2) - (ouch.get_width() // 2),
                           (screen_height // 2) - (ouch.get_height() // 2)])

    # Draw all the spites
    all_sprites_list.draw(screen)

    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, [5, 5])

    if not good_block_list:
        game_over = game_over_font.render("G A M E O V E R * SCORE: " + str(score), True, BLACK)
        game_over_sound.play()
        screen.blit(game_over, [(screen_width // 2) - (game_over.get_width() // 2),
                                (screen_height // 2) - (game_over.get_height() // 2)])

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 60 frames per second
    clock.tick(60)

pygame.quit()
