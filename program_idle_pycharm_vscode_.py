# dodajemy import biblioteki
import pgzrun
from datetime import datetime

WIDTH = 1280
HEIGHT = 640
TITLE = "Maks - gra przygodowa"

#
# tutaj pełna reszta kodu
#

# tworzymy zmienną gry
game = Game(background_active, rooms_in_game)


def update():
    game.update_game()


def draw():
    game.draw_scene()

# uruchamiamy bibliotekę PygameZero
pgzrun.go()
