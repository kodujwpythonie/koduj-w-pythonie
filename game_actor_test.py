WIDTH = 1280
HEIGHT = 640

background_active = "corridor-01.jpg"
background_position = (0, 0)
bohater = Actor("character-right-01.png")
bohater.pos = (670, 500)

def update():
    screen.blit( background_active, background_position )
    bohater.draw()