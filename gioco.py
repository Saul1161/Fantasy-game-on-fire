"""
Platformer Game

python -m arcade.examples.platform_tutorial.05_add_gravity
"""
import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

TILE_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
PLAYER_SCALE = 0.5
FADE_SPEED = 8   # --- AGGIUNTO ---


class GameView(arcade.Window):

    def __init__(self):

        super().__init__(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            WINDOW_TITLE,
            resizable=True,
            fullscreen=True
        )

        # --- AGGIUNTO ---
        self.in_house = False
        self.is_fading = False
        self.fade_alpha = 0
        self.fade_direction = 1
        self.fade_target = None

        # Player (TUO CODICE)
        self.player_texture = arcade.load_texture(
            "C:/Users/saul.vianello/Downloads/ciao/Fantasy-game-on-fire/Bello.png"
        )
        self.player_sprite = arcade.Sprite(self.player_texture, scale=PLAYER_SCALE)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_sprite.scale = 0.3

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        self.background = None

        # Terreno (TUO CODICE)
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # --- CASA (AGGIUNTO) ---
        self.house_sprite = arcade.Sprite(
            ":resources:images/tiles/house.png",
            scale=0.9
        )
        self.house_sprite.center_x = 1100
        self.house_sprite.center_y = 160

        # Fisica (TUO CODICE)
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.wall_list,
            gravity_constant=GRAVITY
        )

        # --- SFONDI (AGGIUNTO) ---
        self.background_outside = arcade.load_texture(
            ":resources:images/backgrounds/abstract_2.jpg"
        )
        self.background_inside = arcade.load_texture(
            ":resources:images/backgrounds/abstract_1.jpg"
        )

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

    def setup(self):
        pass

    def on_draw(self):
        arcade.start_render()

        # --- AGGIUNTO ---
        if self.in_house:
            arcade.draw_texture_rect(
                self.background_inside,
                arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
            )
        else:
            arcade.draw_texture_rect(
                self.background_outside,
                arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
            )
            self.wall_list.draw()
            self.house_sprite.draw()

        self.player_list.draw()

        # --- FADE (AGGIUNTO) ---
        if self.is_fading:
            arcade.draw_rectangle_filled(
                WINDOW_WIDTH // 2,
                WINDOW_HEIGHT // 2,
                WINDOW_WIDTH,
                WINDOW_HEIGHT,
                (0, 0, 0, self.fade_alpha)
            )

    def on_update(self, delta_time):

        self.physics_engine.update()

        # --- ENTRATA CASA (AGGIUNTO) ---
        if not self.in_house and not self.is_fading:
            if arcade.check_for_collision(self.player_sprite, self.house_sprite):
                self.start_fade("enter")

        # --- LOGICA FADE (AGGIUNTO) ---
        if self.is_fading:
            self.fade_alpha += FADE_SPEED * self.fade_direction

            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.fade_direction = -1

                if self.fade_target == "enter":
                    self.in_house = True
                    self.player_sprite.center_x = WINDOW_WIDTH // 2
                    self.player_sprite.center_y = 120
                else:
                    self.in_house = False
                    self.player_sprite.center_x = 1000
                    self.player_sprite.center_y = 150

            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.is_fading = False

    # --- AGGIUNTO ---
    def start_fade(self, target):
        self.is_fading = True
        self.fade_alpha = 0
        self.fade_direction = 1
        self.fade_target = target
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

    def on_key_press(self, key, modifiers):

        # Salto (TUO CODICE)
        if key in (arcade.key.UP, arcade.key.W):
            if not self.in_house and self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        # Movimento (TUO CODICE)
        if key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # --- USCITA CASA (AGGIUNTO) ---
        if key == arcade.key.E and self.in_house and not self.is_fading:
            self.start_fade("exit")

        if key == arcade.key.ESCAPE:
            self.set_fullscreen(False)

    def on_key_release(self, key, modifiers):

        if key in (arcade.key.LEFT, arcade.key.A,
                   arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = 0

        if key == arcade.key.BACKSLASH:
            self.set_fullscreen(True)


def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()