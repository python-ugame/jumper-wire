import ugame
import stage


class Hero(stage.Sprite):
    def __init__(self, x, y):
        super().__init__(tiles, 4, x, y)
        self.dy = 0
        self.dx = 1
        self.dead = False

    def update(self, frame):
        super().update()
        if self.dead:
            sprite.set_frame(8, (frame // 4) * 4)
            return
        bottom_tile = layer1.tile((self.x + 8) // 16, (self.y + 16) // 16)
        if layer1.tile((self.x + 8) // 16, (self.y) // 16) == 0:
            self.dy = 0
        if bottom_tile not in (0, 2):
            self.dy = min(self.dy + 1, 6)
        elif bottom_tile == 2:
            self.dy = min(self.dy + 1, 0)
        else:
            self.dy = min(self.dy, 0)
        self.move(self.x, self.y + self.dy)
        while layer1.tile((self.x + 8) // 16, (self.y + 15) // 16) == 0:
            if self.y % 16 == 0:
                break
            self.move(self.x, self.y - 1)

        keys = ugame.buttons.get_pressed()
        if keys & ugame.K_RIGHT:
            self.dx = 1
            if layer1.tile((self.x + 13) // 16, (self.y + 10) // 16) != 0:
                self.move(self.x + 2, self.y)
            self.set_frame(4 + 1 + frame // 4, 0)
        elif keys & ugame.K_LEFT:
            self.dx = -1
            if layer1.tile((self.x + 2) // 16, (self.y + 10) // 16) != 0:
                self.move(self.x - 2, self.y)
            self.set_frame(4 + 1 + frame // 4, 4)
        elif keys & ugame.K_UP and layer1.tile((self.x + 8) // 16,
                                               (self.y + 15) // 16) == 2:
            self.move(self.x, self.y - 2)
            self.set_frame(4 + 3, (frame // 4) * 4)
        elif keys & ugame.K_DOWN and bottom_tile == 2:
            self.move(self.x, self.y + 2)
            self.set_frame(4 + 3, (frame // 4) * 4)
        else:
            self.set_frame(4 + 0, (frame // 4) * 4)
        if keys & ugame.K_O and self.dy == 0 and bottom_tile in (0, 2):
            self.dy = -6
        if keys & ugame.K_X:
            if bolt.dx == 0:
                bolt.move(self.x + self.dx * 8, self.y)
                bolt.dx = self.dx * 6
            self.set_frame(10, 0 if self.dx > 0 else 4)

    def kill(self):
        self.dead = True


class Sparky(stage.Sprite):
    def __init__(self, x, y):
        super().__init__(tiles, 15, x, y)
        self.dead = False
        self.dx = 1

    def update(self, frame):
        super().update()
        if self.dead:
            if stage.collide(self.x + 3, self.y + 1, self.x + 13, self.y + 15,
                             hero.x + 3, hero.y + 1, hero.x + 13, hero.y + 15):
                self.move(-16, -16)
            return
        sprite.set_frame(15, (frame // 4) * 4)
        bottom_tile = layer1.tile((self.x + 8) // 16, (self.y + 16) // 16)
        forward_tile = layer1.tile((self.x + 8 + 8 * self.dx) // 16,
                                   (self.y + 8) // 16)
        if bottom_tile != 0 or forward_tile == 0:
            self.dx = -self.dx
        self.move(self.x + self.dx, self.y)
        if stage.collide(self.x + 3, self.y + 1, self.x + 13, self.y + 15,
                         bolt.x + 8, bolt.y + 8):
            self.kill()
            bolt.kill()
        if stage.collide(self.x + 3, self.y + 1, self.x + 13, self.y + 15,
                         hero.x + 3, hero.y + 1, hero.x + 13, hero.y + 15):
            hero.kill()

    def kill(self):
        self.dead = True
        sprite.set_frame(12 + self.dx)


class Blinka(stage.Sprite):
    def __init__(self, x, y):
        super().__init__(tiles, 14, x, y)

    def update(self, frame):
        super().update()
        sprite.set_frame(14, (frame // 4) * 4)


class Bolt(stage.Sprite):
    def __init__(self, x, y, dx):
        super().__init__(tiles, 9, x, y)
        self.dx = dx

    def update(self, frame):
        super().update()
        if layer1.tile((self.x + 8) // 16, (self.y + 8) // 16) == 0:
            self.kill()
        else:
            sprite.set_frame(9, (frame // 4) * 4)
            self.move(self.x + self.dx, self.y)

    def kill(self):
        self.dx = 0
        self.move(-16, -16)


walls = stage.Bank.from_bmp16("walls.bmp")
tiles = stage.Bank.from_bmp16("jumper.bmp")
bmp = stage.BMP16("level.bmp")
bmp.read_header()
layer1 = stage.Grid(tiles, buffer=bmp.read_data())
del bmp
layer0 = stage.WallGrid(layer1, (0,), walls)
game = stage.Stage(ugame.display, 12)
bolt = Bolt(-16, -16, 0)
hero = Hero(16, 16)
sprites = [bolt, Sparky(104, 96), Sparky(64, 32), Sparky(16, 96),
           Sparky(96, 16), hero]
game.layers = [layer0] + sprites + [layer1]
game.render_block()
frame = 0

while True:
    frame = (frame + 1) % 8
    for sprite in sprites:
        sprite.update(frame)
    game.render_sprites(sprites)
    game.tick()
