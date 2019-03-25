import pyxel
import random
from random import randint


class App(object):
    def __init__(self, caption, fps):
        self.ship = Ship(0, 120, 11)
        self.enemy = Enemy(245, 0)
        self.enemy2 = Enemy(265, 0)
        self.projectiles = []
        self.enemies = [self.enemy, self.enemy2]
        self.is_game_active = True
        self.maxenemies = 5
        # pyxel.load("asset/asset.pyxel")
        # import pdb; pdb.set_trace()
        pyxel.init(255, 255, caption=caption, fps=fps)
        pyxel.image(0).load(0, 0, "assets/fighter.png")
        pyxel.image(1).load(0, 0, "assets/ground.png")
        pyxel.tilemap(0).set(
            0, 0, ["2200020401006061620040", "4203202122030001020360"], 1)
        # pyxel.image(0).load(0, 0, "assets/cat_16x16.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        if len(self.enemies) < self.maxenemies:
            self.enemies.append(Enemy(255, random.randrange(0, pyxel.height-30)))
        if self.ship.health <= 0:
            self.is_game_active = False 
        for enemy in self.enemies:
            self.update_enemy(enemy)

        # Controls
        self.controls(pyxel)
        #projectiles
        self.projectile_functions()

    def draw_projectile(self, projectile):
        pyxel.pix(projectile.x, projectile.y, projectile.color)

    def draw(self):
        if self.is_game_active:
            pyxel.cls(0)
            pyxel.text(2, 243, f"Health: {self.ship.health}", 11)
            pyxel.text(2, 248, f"Score: {self.ship.score}", 11)
            self.ship.draw_rect()
            for enemy in self.enemies:
                enemy.draw_circ()
            for projectile in self.projectiles:
                self.draw_projectile(projectile)
            pyxel.line(0,240,255,240,7)
                
        else:
            pyxel.cls(0)
            pyxel.text(100, 100, "Game Over! Press Q to quit!", 8)
    
    def controls(self,pyxel):
        if pyxel.btn(pyxel.KEY_UP) and self.ship.y>=2:
            self.ship.y = (self.ship.y - 2)
        if pyxel.btn(pyxel.KEY_DOWN) and self.ship.y+12 <= 240:
            self.ship.y = (self.ship.y + 2)
        if pyxel.btn(pyxel.KEY_LEFT) and self.ship.x>=0:
            self.ship.x = (self.ship.x - 2)
        if pyxel.btn(pyxel.KEY_RIGHT) and self.ship.x<=240:
            self.ship.x = (self.ship.x + 2)
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.projectiles.append(
                Projectile(self.ship.x + 12, self.ship.y + 5, "ship"))
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def update_enemy(self,enemy):
        if enemy.health <= 0:
                self.enemies.remove(enemy)
        if enemy.x <= 0:
            self.enemies.remove(enemy)

        # enemy movements
        # Move enemy forward
        enemy.x = enemy.x - 2
        # Random vertical movement (y axix)
        if random.randrange(1, 100) in range(70) and enemy.y <=230:
            enemy.y = enemy.y + 1
        else:
            if enemy.y >= 0:
                enemy.y = enemy.y - 1
        # Shoot projectiles
        if random.randrange(1, 100) in range(5):
            self.projectiles.append(Projectile(enemy.x - 12, enemy.y, "enemy"))

        #Enemy Projectile collition detection
        for projectile in [_ for _ in self.projectiles if _.affiliation == "ship"]:
            if (
                projectile.x >= enemy.x and projectile.x < enemy.x + 10
            ) and (
                projectile.y >= enemy.y and projectile.y < enemy.y + 10
            ):
                enemy.health -= 2
                self.ship.score += 1
                try:
                    self.projectiles.remove(projectile)
                except:
                    pass

    def projectile_functions(self):
        # projectiles loop
        for projectile in self.projectiles:
            if projectile.x <= 0:
                self.projectiles.remove(projectile)
            if projectile.affiliation == "ship":
                projectile.x += 4
            elif projectile.affiliation == "enemy":
                projectile.x -= 4
            if projectile.x > 255:
                self.projectiles.remove(projectile)

        # projectile collision detection

        for projectile in [_ for _ in self.projectiles if _.affiliation == "enemy"]:
            if (projectile.x >= self.ship.x and projectile.x < self.ship.x + 10) and (
                projectile.y >= self.ship.y and projectile.y < self.ship.y + 10
            ):
                self.ship.health -= 5
                try:
                    self.projectiles.remove(projectile)
                except:
                    pass


class Ship:
    def __init__(self, x, y, color=11,health=50,score=0):
        self.x = x
        self.y = y
        self.color = color
        self._health = health
        self._score = score

    def draw_rect(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, 62, 28,5)
        # pyxel.rect(self.x, self.y, self.x + 10, self.y + 10, self.color)
        # pyxel.pix(self.x, self.y, 2)

    @property
    def health(self):
        return self._health

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self,value):
        self._score = value

    @health.setter
    def health(self, value):
        self._health = value


class Enemy:
    def __init__(self, x, y, color=2,health=1):
        self.x = x
        self.y = y
        self.color = color
        self._health = health

    def draw_rect(self):
        pyxel.rect(self.x, self.y, self.x + 5, self.y + 5, self.color)
        pyxel.pix(self.x, self.y, 5)
        for f in range(self.x, self.x + 5):
            pyxel.pix(f, self.y, 5)
        for f in range(self.y, self.y + 5):
            pyxel.pix(self.x, f, 5)

    def draw_circ(self):
        # pyxel.blt(self.x, self.y, 1, 0, 0, 37, 28,5)
        pyxel.circb(self.x,self.y,5,self.color)

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value


class Projectile(object):
    def __init__(self, x, y, affiliation):
        self._x = x
        self._y = y
        if affiliation == "ship":
            self.color = 8
        else:
            self.color = 7
        self._affiliation = affiliation

    @property
    def affiliation(self):
        return self._affiliation

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


App("Scroll shooter", 30)
