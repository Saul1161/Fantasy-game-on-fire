import arcade

# ---------------- COSTANTI ----------------
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

TILE_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
PLAYER_SCALE = 0.5


# ---------------- PLAYER ----------------
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=PLAYER_SCALE)

        base_path = "C:/Users/saul.vianello/Downloads/ciao/Fantasy-game-on-fire/cavaliere_movimento"

        self.idle_texture = arcade.load_texture(f"{base_path}/idle.png")

        self.walk_textures = [
            arcade.load_texture(f"{base_path}/Walk1.png"),
            arcade.load_texture(f"{base_path}/Walk2.png"),
            arcade.load_texture(f"{base_path}/Walk3.png"),
            arcade.load_texture(f"{base_path}/Walk4.png"),
            arcade.load_texture(f"{base_path}/Walk5.png"),
            arcade.load_texture(f"{base_path}/Walk6.png"),
            arcade.load_texture(f"{base_path}/Walk7.png"),
            arcade.load_texture(f"{base_path}/Walk8.png"),
        ]

        self.texture = self.idle_texture
        self.cur_texture = 0
        self.facing_direction = 0  # 0 = destra, 1 = sinistra

    def update_animation(self, delta_time: float = 1 / 60):

        if self.change_x < 0:
            self.facing_direction = 1
        elif self.change_x > 0:
            self.facing_direction = 0

        if self.change_x == 0:
            self.texture = (
                self.idle_texture.flip_left_right()
                if self.facing_direction == 1
                else self.idle_texture
            )
            return

        self.cur_texture += 1
        if self.cur_texture >= len(self.walk_textures) * 5:
            self.cur_texture = 0

        frame = self.cur_texture // 5
        texture = self.walk_textures[frame]

        self.texture = (
            texture.flip_left_right()
            if self.facing_direction == 1
            else texture
        )


# ---------------- GAME ----------------
class GameView(arcade.Window):

    def __init__(self):
        super().__init__(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            WINDOW_TITLE,
            fullscreen=True,
            resizable=True,
        )

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.camera = arcade.Camera2D()

        # -------- PLAYER --------
        self.player = Player()
        self.player.center_x = 64
        self.player.center_y = 128

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # -------- TERRENO --------
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        for x in range(0, 2000, 64):
            wall = arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                scale=TILE_SCALING,
            )
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # -------- SFONDO --------
        self.background = arcade.load_texture(
            "C:/Users/saul.vianello/Downloads/ciao/Fantasy-game-on-fire/stradafinale.png"
        )

        # -------- FISICA --------
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            walls=self.wall_list,
            gravity_constant=GRAVITY,
        )

    # -------- CAMERA --------
    def center_camera_on_player(self):
        screen_center_x = self.player.center_x - WINDOW_WIDTH / 2
        screen_center_y = self.player.center_y - WINDOW_HEIGHT / 2

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        self.camera.move_to((screen_center_x, screen_center_y), 0.1)

    # ---------------- DRAW ----------------
    def on_draw(self):
        self.clear()
        self.camera.use()

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
        )

        self.wall_list.draw()
        self.player_list.draw()

    # ---------------- UPDATE ----------------
    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_list.update_animation(delta_time)
        self.center_camera_on_player()

    # ---------------- INPUT ----------------
    def on_key_press(self, key, modifiers):

        if key in (arcade.key.UP, arcade.key.W):
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED

        if key in (arcade.key.LEFT, arcade.key.A):
            self.player.change_x = -PLAYER_MOVEMENT_SPEED

        if key in (arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = PLAYER_MOVEMENT_SPEED

        if key == arcade.key.ESCAPE:
            self.set_fullscreen(False)

    def on_key_release(self, key, modifiers):

        if key in (
            arcade.key.LEFT,
            arcade.key.A,
            arcade.key.RIGHT,
            arcade.key.D,
        ):
            self.player.change_x = 0

        if key == arcade.key.BACKSLASH:
            self.set_fullscreen(True)


# ---------------- MAIN ----------------
def main():
    GameView()
    arcade.run()


if __name__ == "__main__":
    main()
