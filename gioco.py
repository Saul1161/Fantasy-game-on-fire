"""
Platformer Game

python -m arcade.examples.platform_tutorial.05_add_gravity
"""
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


class GameView(arcade.Window):
    """Main application class."""

    def __init__(self):
        super().__init__(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            WINDOW_TITLE,
            resizable=True,
            fullscreen=True
        )

        # -------- PLAYER --------
        self.player_texture = arcade.load_texture(
            "C:/Users/saul.vianello/Downloads/ciao/Fantasy-game-on-fire/Bello.png"
        )
        self.player_sprite = arcade.Sprite(
            self.player_texture,
            scale=PLAYER_SCALE
        )
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_sprite.scale = 0.3

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # -------- SFONDO --------
        self.background = None

        # -------- LOCANDA --------
        self.locanda_texture = arcade.load_texture("locanda.png")

        # -------- TERRENO --------
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                scale=TILE_SCALING
            )
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # -------- FISICA --------
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.wall_list,
            gravity_constant=GRAVITY
        )

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.background = arcade.load_texture(
            "C:/Users/saul.vianello/Downloads/ciao/Fantasy-game-on-fire/origbig.png"
        )

    # ---------------- DRAW ----------------
    def on_draw(self):
        """Render the screen."""
        self.clear()  # <-- correzione per Arcade 2.7+

        # Sfondo principale
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
        )

        # Disegna la locanda a destra
        arcade.draw_texture_rect(
            self.locanda_texture,
            arcade.LBWH(
                WINDOW_WIDTH - 800,  # X a destra
                -200,                 # Y
                600,                 # Larghezza
                600                  # Altezza
            )
        )

        # Disegna player e terreno
        self.player_list.draw()
        self.wall_list.draw()

    # ---------------- UPDATE ----------------
    def on_update(self, delta_time):
        self.physics_engine.update()

    # ---------------- INPUT ----------------
    def on_key_press(self, key, modifiers):

        if key in (arcade.key.UP, arcade.key.W):
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        if key in (arcade.key.LEFT, arcade.key.A):
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        if key == arcade.key.ESCAPE:
            self.set_fullscreen(False)

    def on_key_release(self, key, modifiers):

        if key in (arcade.key.LEFT, arcade.key.A,
                   arcade.key.RIGHT, arcade.key.D):
            self.player_sprite.change_x = 0

        if key == arcade.key.BACKSLASH:
            self.set_fullscreen(True)


# ---------------- MAIN ----------------
def main():
    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
