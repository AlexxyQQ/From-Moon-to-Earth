import random
import sqlite3

import pygame
from pygame import mixer

import global_imports

# Initialize pygame and fonts
pygame.init()
pygame.font.init()
pygame.mixer.pre_init(3400, -16, 1, 512)
pygame.mixer.init()

# Create the screen
WIDTH, HEIGHT = 500, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and Icon
pygame.display.set_caption("From Moon To Earth")

icon = pygame.image.load("Images/icon.png")
pygame.display.set_icon(icon)

# Player Images
PlayerImg_straight = pygame.image.load("Images/PlayerStraight.png")
PlayerImg_left_tilt = pygame.image.load("Images/PlayerLeftTilt.png")
PlayerImg_right_tilt = pygame.image.load("Images/PlayerRightTilt.png")

# Obstacles Images
Obstacle_1 = pygame.image.load("Images/Asteroid1.png")
Obstacle_2 = pygame.image.load("Images/Asteroid2.png")

# BOSSES
img_boss_1 = pygame.image.load("Images/Boss1.png")
img_boss_2 = pygame.image.load("Images/Boss2.png")
img_boss_3 = pygame.image.load("Images/Boss3.png")
img_boss_4 = pygame.image.load("Images/Boss4.png")
img_boss_5 = pygame.image.load("Images/Boss5.png")
img_boss_6 = pygame.image.load("Images/Boss6.png")
img_boss_7 = pygame.image.load("Images/Boss7.png")
# img_boss_8 = pygame.image.load('Images/Boss8.png')
img_boss_9 = pygame.image.load("Images/Boss9.png")
img_boss_10 = pygame.image.load("Images/Boss10.png")

# Bullet Image
Bullet_img = pygame.image.load("Images/Bullet.png")

# Good Stuffs
Health_img = pygame.image.load("Images/Health.png")
Star_img = pygame.image.load("Images/Star.png")
continuous_bullet = pygame.image.load("Images/continuous.png")
Cloud_img = pygame.transform.scale(pygame.image.load("Images/dust.png"), (200, 150))

# Background Image
# scaling width height of the image to th window
BG_static = pygame.transform.scale(
    pygame.image.load("Images/Background_static.png"), (WIDTH, HEIGHT)
)

# Variables
COOLDOWN = 100
bullet_vel = 4
obstacle_num = 5
obstacle_vel = 3
health_vel = 2
power_vel = 2
score = 0
level = 0

powered = False
c_powered = False

# Music
bg_endgame = pygame.mixer.Sound("Audio/Last level sound.wav")
bullet_shoot = pygame.mixer.Sound("Audio/Pot_shoot.wav")
explosion_obs = pygame.mixer.Sound("Audio/Bullet_hit_obstacle.wav")
p_up = pygame.mixer.Sound("Audio/powerUp.wav")
health_depl = pygame.mixer.Sound("Audio/Health_deplition.wav")
hup = pygame.mixer.Sound("Audio/hup.wav")


class Bullet:
    """
    Class for bullet element with its coordinates, image, mask and functions:

    draw : Draws the bullet image provide at the provided coordinates
    move : moves the drawn bullet by changing its y coordinate
    off_screen : check for the bullet position, if its off the screen returns True
    collision : checks for the collision by calling collide function and returns boolean value
    """

    def __init__(self, x, y, img):
        """X,Y Positions, image and mask of image initialization of the object"""
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        """Drawing the object on the screen according to the initialized coordinates and image"""
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        """Moving the drawn object on the screen in y coordinate"""
        self.y += vel

    def off_screen(self, height):
        """Checking the y coordinate and height of object if its off the screen"""
        return not (self.y <= height and self.y >= -40)

    def collision(self, obj):
        """Checking collision of the object with another object provided"""
        return collide(self, obj)


class GoodStuff:
    """
    Main class for the:
    :Health
    :Power Ups
    """

    class Health:
        """
        Health element and its functions for:
        :Drawing
        :Moving
        :Getting object's width
        :Getting object's height
        :Going off screen
        :Collision
        """

        def __init__(self, x, y):
            """X,Y Positions, image and mask of image initialization of the object"""
            self.x = x
            self.y = y
            self.img = Health_img
            self.mask = pygame.mask.from_surface(self.img)

        def draw(self, window):
            """Drawing the object on the screen according to the initialized coordinates and image"""
            window.blit(self.img, (self.x, self.y))

        def move(self, vel):
            """Moving the drawn object on the screen in x coordinate"""
            self.x += vel

        def get_width(self):
            """Returns the width of the element"""
            return self.img.get_width()

        def get_height(self):
            """Returns the height of the element"""
            return self.img.get_height()

        def off_screen(self, width):
            """Checking the x coordinate and width of object if its off the screen"""
            return not (self.y <= width and self.y >= 0)

        def collision(self, obj):
            """Checking collision of the object with another object provided"""
            return collide(self, obj)

    class Power_ups:
        """
        Power Ups element and its functions for:
        :Drawing
        :Moving
        :Getting object's width
        :Getting object's height
        :Going off screen
        :Collision
        """

        def __init__(self, x, y):
            """X,Y Positions, image and mask of image initialization of the object"""
            self.x = x
            self.y = y
            self.img = Star_img
            self.mask = pygame.mask.from_surface(self.img)

        def draw(self, window):
            """Drawing the object on the screen according to the initialized coordinates and image"""
            window.blit(self.img, (self.x, self.y))

        def move(self, vel):
            """Moving the drawn object on the screen in x coordinate"""
            self.x += vel

        def get_width(self):
            """Returns the width of the element"""
            return self.img.get_width()

        def get_height(self):
            """Returns the height of the element"""
            return self.img.get_height()

        def off_screen(self, width):
            """Checking the x coordinate and width of object if its off the screen"""
            return not (self.y <= width and self.y >= 0)

        def collision(self, obj):
            """Checking collision of the object with another object provided"""
            return collide(self, obj)

    class Continuous_B:
        """
        Power Ups element and its functions for:
        :Drawing
        :Moving
        :Getting object's width
        :Getting object's height
        :Going off screen
        :Collision
        """

        def __init__(self, x, y):
            """X,Y Positions, image and mask of image initialization of the object"""
            self.x = x
            self.y = y
            self.img = continuous_bullet
            self.mask = pygame.mask.from_surface(self.img)

        def draw(self, window):
            """Drawing the object on the screen according to the initialized coordinates and image"""
            window.blit(self.img, (self.x, self.y))

        def move(self, vel):
            """Moving the drawn object on the screen in x coordinate"""
            self.x += vel

        def get_width(self):
            """Returns the width of the element"""
            return self.img.get_width()

        def get_height(self):
            """Returns the height of the element"""
            return self.img.get_height()

        def off_screen(self, width):
            """Checking the x coordinate and width of object if its off the screen"""
            return not (self.y <= width and self.y >= 0)

        def collision(self, obj):
            """Checking collision of the object with another object provided"""
            return collide(self, obj)

    class clouds:
        def __init__(self, x, y):
            """X,Y Positions, image and mask of image initialization of the object"""
            self.x = x
            self.y = y
            self.img = Cloud_img
            self.mask = pygame.mask.from_surface(self.img)

        def draw(self, window):
            """Drawing the object on the screen according to the initialized coordinates and image"""
            window.blit(self.img, (self.x, self.y))

        def move(self, vel):
            """Moving the drawn object on the screen in x coordinate"""
            self.x += vel

        def get_width(self):
            """Returns the width of the element"""
            return self.img.get_width()

        def get_height(self):
            """Returns the height of the element"""
            return self.img.get_height()

        def off_screen(self, width):
            """Checking the x coordinate and width of object if its off the screen"""
            return not (self.y <= width and self.y >= 0)


class Game_Asset:
    """
    Class for the Game_Asset with its

    coordinates : initial player and obstacle x,y coordinates
    health : health (default 100) for player
    player image : for the player image
    obstacle image : for the player image
    bullet image : for the player image
    bullets list : for the amount of bullets to be displayed on screen
    cool down counter : bullet cool down counter
    power cool down counter : power ups cool down counter
    power counting : Boolean to check the power ups counting

    Functions
    draw : draws the player image on screen at given coordinates and draws the bullet in bullets list
    cooldown : checks for the cool down counter resets it or increases it
    cooldown_power : checks for power cool down counter , decreases it or resets the power up
    shoot :
    """

    def __init__(self, x, y, health=100):
        """Parameters used by the Game Asset class"""
        self.x = x
        self.y = y
        self.health = health
        self.rocket_img = None
        self.obs_img = None
        self.bullet_img = None
        self.bullets = []
        self.cool_down_counter = 0
        self.power_cool_down_counter = 500
        self.power_counting = False

    def draw(self, window):
        """draws player image on screen at provided x,y coordinates and draws the bullets in bullets list"""
        window.blit(self.rocket_img, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window)

    def cooldown(self):
        """checks for the cool down of bullet and increase it"""
        if self.cool_down_counter >= COOLDOWN:
            self.cool_down_counter = 0
        if not c_powered:
            if self.cool_down_counter > 0:
                self.cool_down_counter += 1
        if c_powered:
            if self.cool_down_counter > 0:
                self.cool_down_counter += 10

    def cooldown_power(self):
        """Decreases the power_cool_down_counter and resets after its back to 0"""
        if self.power_counting:
            """When counting starts decreases the counter"""
            self.power_cool_down_counter -= 1
        if self.power_cool_down_counter == 0:
            """When counter is 0 resets the counter back to 500 and removes the player power up
            and stops the counting"""
            self.power_counting = False
            global powered, c_powered
            powered = False
            c_powered = False
            self.power_cool_down_counter = 500

    def shoot(self):
        """Lets player shoot bullets once the cool down is 0 also check if the player is powered up and let player
        fire multiple bullets."""
        if self.cool_down_counter == 0:
            """Checking if player can shoot"""
            bullet_shoot.play()
            if self.power_cool_down_counter != 0:
                """Checking the power counter"""
                if powered:
                    """Checking if player is powered up and firing multiple bullets"""
                    bullet1 = Bullet(self.x + 30, self.y + 50, self.bullet_img)
                    bullet2 = Bullet(self.x - 30, self.y + 50, self.bullet_img)
                    self.bullets.append(bullet1)
                    self.bullets.append(bullet2)
                    self.power_counting = True
            if not powered:
                """Checking if player is not powered up and letting fire only a single bullet"""

                bullet = Bullet(self.x, self.y - 30, self.bullet_img)
                self.bullets.append(bullet)

            self.cool_down_counter = 1

    def continuous_shoot(self):
        if c_powered:
            if self.cool_down_counter == 0:
                if self.power_cool_down_counter != 0:
                    bullet = Bullet(self.x, self.y - 30, self.bullet_img)
                    self.bullets.append(bullet)
                    self.power_counting = True
                self.cool_down_counter = 1

    def get_width(self):
        """Getting width of the player"""
        return self.rocket_img.get_width()

    def get_height(self):
        """Getting height of the player"""
        return self.rocket_img.get_height()


class Player(Game_Asset):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)  # calling parent class init function
        self.rocket_img = PlayerImg_straight
        self.bullet_img = Bullet_img
        self.mask = pygame.mask.from_surface(
            self.rocket_img
        )  # creating mask for collision
        self.max_health = health

    def move_bullet(self, vel, objs1, objs2, objs3, objs4):
        self.cooldown()
        self.cooldown_power()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            else:
                for obj in objs1:
                    if bullet.collision(obj):
                        explosion_obs.play()
                        if random.randrange(0, 1 * 60) == 1:
                            hup.play()
                            self.health += 10

                        global draw_ex
                        draw_ex = True

                        global score
                        score += 1

                        explosion = Obs_Explo(obj.x + 20, obj.y + 10, 1)
                        explosion_group.add(explosion)

                        objs1.remove(obj)

                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                for obj in objs2:
                    if bullet.collision(obj):
                        p_up.play()
                        objs2.remove(obj)
                        hup.play()
                        self.health += 20
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

                for obj in objs3:
                    if bullet.collision(obj):
                        p_up.play()
                        objs3.remove(obj)
                        global powered
                        powered = True
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

                for obj in objs4:
                    if bullet.collision(obj):

                        explosion = Obs_Explo(obj.x + 50, obj.y + 50, 1)
                        explosion_group.add(explosion)
                        try:
                            self.bullets.remove(bullet)
                        except:
                            pass

                        obj.health -= random.randrange(40, 100)

                        if obj.health <= 0:
                            objs4.remove(obj)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (2, 585 + 115 + 10, 497, 18))
        pygame.draw.rect(
            window,
            (0, 255, 0),
            (2, 585 + 115 + 10, 497 * (self.health / self.max_health), 18),
        )


def obstacle_rotate(obs1, obs2):
    global Obstacle_1, Obstacle_2
    new_Obstacle_1 = pygame.transform.rotozoom(obs1, random.randrange(0, 360), 1)
    new_Obstacle_2 = pygame.transform.rotozoom(obs2, random.randrange(0, 360), 1)
    return [new_Obstacle_1, new_Obstacle_2]


class Obstacles(Game_Asset):
    OBSTACLES_CHOICES = [Obstacle_1, Obstacle_2]

    def __init__(self, x, y, which):
        super().__init__(
            x,
            y,
        )  # calling parent class init function

        self.obs_img = self.OBSTACLES_CHOICES[which]
        self.mask = pygame.mask.from_surface(self.obs_img)

    def draw(self, window):
        window.blit(self.obs_img, (self.x, self.y))

    def get_width(self):
        return self.obs_img.get_width()

    def get_height(self):
        return self.obs_img.get_height()

    def move(self, vel):
        self.y += vel


class BOSSES(Game_Asset):
    BOSS_CHOICES = [
        img_boss_1,
        img_boss_2,
        img_boss_3,
        img_boss_4,
        img_boss_5,
        img_boss_6,
        img_boss_7,
        img_boss_9,
        img_boss_10,
    ]

    def __init__(self, x, y, which):
        super().__init__(
            x,
            y,
        )  # calling parent class init function

        self.boss_img = pygame.transform.scale(self.BOSS_CHOICES[which], (90, 90))
        self.mask = pygame.mask.from_surface(self.boss_img)

    def draw(self, window):
        window.blit(self.boss_img, (self.x, self.y))

    def get_width(self):
        return self.boss_img.get_width()

    def get_height(self):
        return self.boss_img.get_height()

    def move(self, vel):
        self.y += vel


class Obs_Explo(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.x = x
        self.y = y
        for num in range(1, 6):
            img = pygame.image.load(f"Images/explosion/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (50, 50))
            # add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        # setting initial threshold
        explosion_speed = 5
        # update explosion animation
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        # if the animation is complete,delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def database():
    db = sqlite3.connect("Database.db")
    dc = db.cursor()
    try:
        dc.execute(
            f""" UPDATE Highscores SET highscore={score} WHERE player = +'{global_imports.user_playing}'"""
        )
        db.commit()
    except:
        pass


explosion_group = pygame.sprite.Group()


def main():
    """Main loop for game"""

    global score, COOLDOWN, level, obstacle_num, obstacle_vel, powered, c_powered, endgame, lost

    running = True  # State of window
    FPS = 60  # Designated time the while loop runes each second

    # Assigning font for pygame
    main_font = pygame.font.SysFont("Arial", 25)
    lost_font = pygame.font.SysFont("Arial", 65)

    # initila player position
    player = Player(220, 590)

    # Variables
    player_vel = 5
    obstacles = []
    bosses = []
    power_ups = []
    health_ups = []
    clouds_app = []
    continuous_list = []
    background_y_pos = 0
    Message = "You Lost !!!"

    lost = False  # State of game
    endgame = False
    lost_count = 0  # To quit game after losing

    # Setting up clock for the while loop
    clock = pygame.time.Clock()

    def moving_background():
        WIN.blit(BG_static, (0, background_y_pos))
        WIN.blit(BG_static, (0, background_y_pos - HEIGHT))

    def drawing():
        """Drawing elements on screen"""
        global running, Image_list_Explosions_index, coords, angle, radius, endgame

        # Drawing background

        moving_background()

        database()

        # Updating Highscore
        high_score_list = []
        db = sqlite3.connect("Database.db")
        dc = db.cursor()
        dc.execute("SELECT * FROM Highscores")
        all_scores = dc.fetchall()
        for s in all_scores:
            high_score_list.append(int(s[1]))
        highsocre = max(high_score_list)

        if score > highsocre:
            highsocre = score

        # Updating Player Name
        player_name = global_imports.user_playing

        # Designating level and score

        level_label = main_font.render(f"Level: {level}", 1, (129, 216, 208))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        score_label = main_font.render(f"Score: {score}", 1, (129, 216, 208))
        high_score_label = main_font.render(
            f"HighScore: {highsocre}", 1, (129, 216, 208)
        )
        player_name_label = main_font.render(f"{player_name}", 1, (129, 216, 208))

        # Drawing lives,level and score on screen
        WIN.blit(high_score_label, (10, 10))
        WIN.blit(score_label, (10, high_score_label.get_height() + 10))

        WIN.blit(
            player_name_label, (WIDTH / 2 - player_name_label.get_width() + 25, 10)
        )
        if not endgame:
            for obstacle in obstacles:
                obstacle.draw(WIN)

        for health_up in health_ups:
            health_up.draw(WIN)

        for power in power_ups:
            power.draw(WIN)

        for cloud in clouds_app:
            cloud.draw(WIN)

        for bul in continuous_list:
            bul.draw(WIN)

        for boss in bosses:
            boss.draw(WIN)

        player.draw(WIN)

        if lost:
            """If the gave is over text is displayed"""
            lost_label = lost_font.render(f"{Message}", 1, (0, 0, 0))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 300))

        explosion_group.update()

        power_orbs()

        explosion_group.draw(WIN)

        pygame.display.update()

    def clouds_appear():
        """Health orbs generation"""

        if random.randrange(0, 6 * 60) == 1:
            if len(health_ups) < 2:
                for i in range(1):
                    cloud = GoodStuff.clouds(
                        random.randrange(-200, -50), random.randrange(100, 400)
                    )
                    clouds_app.append(cloud)

    def health_orbs():
        """Health orbs generation"""

        # Normal situation
        if player.health < 80:
            if random.randrange(0, 9 * 60) == 1:  # 1 in 540 chance
                if len(health_ups) < 2:
                    for i in range(1):
                        health_up = GoodStuff.Health(
                            random.randrange(-200, -50), random.randrange(100, 400)
                        )
                        health_ups.append(health_up)

        # Dire situation
        if player.health < 30:
            if random.randrange(0, 2 * 60) == 1:  # 1 in 120 chance
                if len(health_ups) < 3:
                    for i in range(1):
                        health_up = GoodStuff.Health(
                            random.randrange(-200, -50), random.randrange(100, 400)
                        )
                        health_ups.append(health_up)

    def increments():
        global obstacle_num, obstacle_vel, level, COOLDOWN, endgame
        if score == 20:
            obstacle_num = 7
            obstacle_vel = 4
            level = 1
            COOLDOWN = 80

        if score == 50:
            obstacle_num = 10
            obstacle_vel = 4
            level = 2
            COOLDOWN = 60

        if score == 80:
            obstacle_num = 11
            obstacle_vel = 5
            level = 3
            COOLDOWN = 40

        if score == 100:
            obstacle_num = 13
            obstacle_vel = 5
            level = 4
            COOLDOWN = 30
        if score == 150:
            endgame = True
            level = 5
            COOLDOWN = 25
        if not endgame:
            if score > 150:
                COOLDOWN = 40
                obstacle_num = random.randrange(8, 20)
                obstacle_vel = random.randrange(2, 8)

    def power_orbs():
        if random.randrange(0, 9 * 60) == 1:  # 1 in 540 chance
            if score > 20:
                if not powered:
                    if len(power_ups) < 1:
                        for i in range(1):
                            power_up = GoodStuff.Power_ups(
                                random.randrange(-200, -50), random.randrange(100, 400)
                            )
                            power_ups.append(power_up)

    def con_bullet():
        ch = 12
        if score > 150:
            ch = 6
        if random.randrange(0, ch * 60) == 1:
            if level >= 2:
                if len(continuous_list) < 1:
                    for i in range(1):
                        bu = GoodStuff.Continuous_B(
                            random.randrange(-200, -50), random.randrange(100, 400)
                        )
                        continuous_list.append(bu)

    """ Running the loop """
    while running:
        """Running while loop accord to the designated FPS"""
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        drawing()

        background_y_pos += 2
        if background_y_pos >= HEIGHT:
            background_y_pos = 0

        if player.health <= 0:
            mixer.stop()

            lost = True

        if lost:
            lost_count += 1
            if lost_count > FPS * 3:
                endgame = False

                running = False

            else:
                """Stops player form moving"""
                continue

        if endgame:
            bg_endgame.set_volume(0.15)
            bg_endgame.play()
        if not endgame:
            bg_endgame.stop()

        if not endgame:
            if len(obstacles) == 0:
                for i in range(obstacle_num):
                    obstacle = Obstacles(
                        random.randrange(10, WIDTH - 50),
                        random.randrange(-800, -100),
                        random.choice([0, 1]),
                    )
                    obstacles.append(obstacle)

        if endgame:
            COOLDOWN = 20
            score = 150

            if len(bosses) == 0:
                boss1 = BOSSES(0, -150, 1)
                bosses.append(boss1)
                boss2 = BOSSES(188, -150, 2)
                bosses.append(boss2)
                boss3 = BOSSES(349, -150, 3)
                bosses.append(boss3)
                boss4 = BOSSES(30 + 122 // 2, -250, 4)
                bosses.append(boss4)
                boss5 = BOSSES(349 - 91, -250, 5)
                bosses.append(boss5)
                boss6 = BOSSES(349 + 90, -250, 6)
                bosses.append(boss6)
                boss7 = BOSSES(0, -250 - 83, 7)
                bosses.append(boss7)
                boss8 = BOSSES(188, -250 - 83, 8)
                bosses.append(boss8)
                boss9 = BOSSES(349, -250 - 83, 0)
                bosses.append(boss9)
                boss10 = BOSSES(0, -250 - 83 - 100, 1)
                bosses.append(boss10)
                boss12 = BOSSES(188, -250 - 83 - 100, 2)
                bosses.append(boss12)
                boss13 = BOSSES(349, -250 - 83 - 100, 3)
                bosses.append(boss13)
                boss14 = BOSSES(30 + 122 // 2, -250 - 83 - 83 - 83, 4)
                bosses.append(boss14)
                boss15 = BOSSES(349 - 91, -250 - 83 - 83 - 83, 5)
                bosses.append(boss15)
                boss16 = BOSSES(349 + 90, -250 - 83 - 83 - 83, 6)
                bosses.append(boss16)
                boss17 = BOSSES(0, -250 - 83 - 83 - 83 - 83, 7)
                bosses.append(boss17)
                boss18 = BOSSES(188, -250 - 83 - 83 - 83 - 83, 8)
                bosses.append(boss18)
                boss19 = BOSSES(349, -250 - 83 - 83 - 83 - 83, 0)
                bosses.append(boss19)

        health_orbs()
        increments()
        clouds_appear()
        con_bullet()

        """ Checking key press """
        keys = pygame.key.get_pressed()

        # Checking for specific keypress and player position and putting boundaries
        if pygame.key.get_focused():
            player.rocket_img = PlayerImg_straight
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
            player.rocket_img = PlayerImg_left_tilt
        if (
            keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH
        ):  # right
            player.x += player_vel
            player.rocket_img = PlayerImg_right_tilt
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if (
            keys[pygame.K_s]
            and player.y + player_vel + player.get_height() + 15 < HEIGHT
        ):  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:  # Space
            if not c_powered:
                player.shoot()
            if endgame:
                if random.randrange(0, 6 * 60) == 1:
                    p_up.play()
                    powered = True

        if c_powered:
            player.continuous_shoot()
        if not endgame:
            for obstacle in obstacles[:]:
                obstacle.move(obstacle_vel)
                Obstacles.OBSTACLES_CHOICES = obstacle_rotate(Obstacle_1, Obstacle_2)

                if collide(obstacle, player):
                    health_depl.play()
                    player.health -= 10
                    obstacles.remove(obstacle)

                if obstacle.y + obstacle.get_height() > HEIGHT + 80:
                    obstacles.remove(obstacle)
                    score += 1
                    for i in range(1):
                        obstacle = Obstacles(
                            random.randrange(10, WIDTH - 50),
                            random.randrange(-800, -100),
                            random.choice([0, 1]),
                        )

                        obstacles.append(obstacle)

        if endgame:

            for boss in bosses[:]:
                boss.move(2)

                if collide(boss, player):
                    player.health = 0
                    bosses.remove(boss)
                if boss.y + boss.get_height() > HEIGHT + 80:
                    if not len(bosses) < 2:
                        bosses.remove(boss)

            if len(bosses) == 1:
                Message = "Game Completed"
                lost = True

        for health_up in health_ups:
            health_up.move(health_vel)
            if collide(health_up, player):
                if not c_powered:
                    hup.play()
                    player.health += 10
                    if player.health > 100:
                        player.health = 100
                    health_ups.remove(health_up)
            if health_up.y + health_up.get_width() > WIDTH + 40:
                health_ups.remove(health_up)

        for power in power_ups:
            power.move(power_vel)
            if collide(power, player):
                p_up.play()
                if not c_powered:
                    powered = True
                    power_ups.remove(power)
            if power.y + power.get_width() > WIDTH + 40:
                power_ups.remove(power)

        for cloud in clouds_app:
            cloud.move(health_vel)
            if cloud.y + cloud.get_width() > WIDTH + 40:
                clouds_app.remove(cloud)

        for bul in continuous_list:
            bul.move(power_vel)
            if collide(bul, player):
                p_up.play()
                if not c_powered:
                    c_powered = True
                    continuous_list.remove(bul)
            if bul.y + bul.get_width() > WIDTH + 40:
                continuous_list.remove(bul)

        player.move_bullet(-bullet_vel, obstacles, health_ups, power_ups, bosses)


main()
