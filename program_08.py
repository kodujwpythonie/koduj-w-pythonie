from datetime import datetime

WIDTH = 1280
HEIGHT = 640

# definicje klas
class Game:
    def __init__(self, background_active, rooms_in_game):

        # ustawiamy najważniejsze elementy, niektóre na stałe
        self.background_active = background_active
        self.background_position = (0, 0)
        self.game_start = False
        self.game_finish = False
        self.actual_room = 5
        self.start_time = None
        self.all_keys_found = False
        self.show_hidden_door = False
        self.enter_last_door = False
        self.shift_ok = True

        # grafiki na rozpoczęcie i zakończenie gry
        self.intro_canvas = Actor("intro-canvas.png")
        self.intro_canvas.pos = (640, -160)
        self.game_over_canvas = Actor("intro-gameover-canvas.png")
        self.game_over_canvas.pos = (320, -160)

        # elementy związane z naszym bohaterem
        self.floor_level = 460
        self.hero = Actor("character-right-01.png")
        self.hero.pos = (WIDTH / 2, self.floor_level)
        # wyznaczenie rozmiarów gracza
        self.hero.height = 256
        self.hero.width = 140
        self.hero.frame = 1
        self.animation_step = 15

        # słownik z opisami pomieszczeń
        self.rooms = rooms_in_game

        # klucze
        self.pocket = Actor("pocket.png")
        self.pocket.pos = (1000, 100)
        self.keys_in_pocket = [key_00, key_01, key_02, key_03, key_04]

    def draw_intro(self):
        def draw_text(text, x_offset, y_offset, fontsize=20):
            screen.draw.text(
                text,
                (self.intro_canvas.x + x_offset, self.intro_canvas.y + y_offset),
                fontname="ptsansnarrowbold.ttf",
                fontsize=fontsize,
                color=(187, 96, 191),
            )

        # wyświetlenie ekranu startowego gry
        self.intro_canvas.draw()
        animate(self.intro_canvas, pos=(640, 320), duration=0.3, tween="linear")

        draw_text("Maks - powrót do szkoły", -450, -200, fontsize=32)

        # wprowadzenie: przedstawienie historii gry, zadania do wykonania, oraz klawisze aktywne w grze.
        story = (
            "Co powiecie na stworzenie gry przygodowej, w której główny "
            "bohater - Maks, aby dojść do finału, pokonuje "
            "przeszkody i rozwiązuje zagadki? A co, jeśli dodam, że akcja "
            "rozgrywa się w szkole, pozornie najnudniejszym miejscu "
            "na świecie? Może wspólnie uda nam się to miejsce trochę, "
            "ekhm... rozruszać? Znajdź i zbierz wszystkie klucze aby wejść do "
            "rozsadzanej basami auli, na koncert najgorętszego bandu Europy! "
            "\n\n"
            "wyjście z gry - klawisz 'Q'"
            "\n\n"
            "Naciśnij klawisz SPACJI, aby rozpocząć grę!"
        )

        screen.draw.text(
            story,
            (self.intro_canvas.x - 450, self.intro_canvas.y - 160),
            width=900,
            fontname="ptsansnarrowregular.ttf",
            fontsize=20,
            color=(0, 0, 0),
        )

        # opis klawiszy kontrolnych
        draw_text("przejdź przez drzwi", 200, -55)
        draw_text("idź w lewo", 120, 175)
        draw_text("weź klucz", 230, 175)
        draw_text("idź w prawo", 330, 175)

    def draw_pocket(self):
        self.pocket.draw()
        # ustawienie położenia / odległości między kluczami
        key_pos = [-200, -100, 0, 100, 200]

        temp = 0
        # dla każdego klucza w liście kluczy
        for key in self.keys_in_pocket:
            pos = (self.pocket.x + key_pos[temp] - 45, self.pocket.y - 10)
            temp += 1
            if key.in_pocket:
                # jeśli mamy klucz - wyświetlamy z pliku graficznego w konkretnej pozycji
                screen.blit(key.file_name, pos)
            else:
                # jeśli nie mamy klucza wyświetlamy znak zapytania
                screen.blit("question-mark.png", pos)

    def hero_move(self, direction):

        # pobieramy flagę mówiącą o tym, w którą stronę Maks może się przemieścić
        move_flag = self.rooms[self.actual_room].can_move_lr

        if direction == "right":
            # jeżeli jest to możliwe przesuwamy postać
            if self.hero.x < WIDTH - self.hero.width:
                self.hero.x += self.animation_step
            else:
                if move_flag == 2 or move_flag == 3:
                    self.actual_room += 1
                    self.hero.x = 10

        if direction == "left":
            # jeżeli jest to możliwe przesuwamy postać
            if self.hero.x > self.hero.width:
                self.hero.x -= self.animation_step
            else:
                if move_flag == 1 or move_flag == 3:
                    self.actual_room -= 1
                    self.hero.x = WIDTH - self.hero.width

        # sprawdzamy tło dla nowego pomieszczenia
        new_background_image = self.rooms[self.actual_room].file_name
        self.background_active = new_background_image

        # ustawiamy odpowiedni obrazek animujący ruch
        self.hero.image = f"character-{direction}-0{self.hero.frame}.png"
        # zwiększając numer obrazka następnym razem załadujemy inny,
        # co będzie pozornie wyglądało jak ruch
        self.hero.frame += 1
        # jest 8 obrazków, więc jeśli frame > 8
        if self.hero.frame > 8:
            # to wracamy do 1
            self.hero.frame = 1

    def enter_door(self):
        # pobieramy element słownika
        room = self.rooms[self.actual_room]
        if len(room.doors):
            for door in room.doors:
                if (
                    self.hero.x > door.x_left_door
                    and self.hero.x < door.x_right_door
                    and door.open
                    and self.shift_ok
                ):
                    self.shift_ok = False
                    # pobieramy nowy numer pomieszczenia i nazwę pliku tła
                    new_room = door.next_room_number
                    new_background_image = self.rooms[new_room].file_name
                    # ustawiamy odpowiednie właściwości
                    self.background_active = new_background_image
                    self.actual_room = new_room
                    # odblokowujemy po pół sekundy
                    clock.schedule_unique(self.shitf_do, 0.5)
                    # przerywamy pętlę for i kończymy
                    break

    def shitf_do(self):
        self.shift_ok = True

    def draw_key(self):
        # dla każdego klucza w grze
        for key in self.keys_in_pocket:
            # jeżeli klucza nie ma w kieszeni odnalezionych i aktualny numer
            # pomieszczenia jest taki sam jak numer pomieszczenia dla klucza
            if not key.in_pocket and self.actual_room == key.room_number:
                # wyświetlamy klucz
                screen.blit(key.file_name, (key.place_on_floor, 475))

    def get_key(self):
        def check_all_keys(keys):
            for any_key in keys:
                if any_key.in_pocket is False:
                    return False
            else:
                return True

        # dla każdego klucza w grze
        for key in self.keys_in_pocket:
            # jeżeli klucza nie ma w kieszeni odnalezionych i aktualny numer
            # pomieszczenia jest taki sam jak numer pomieszczenia dla klucza
            # a nasz bohater jest blisko klucza
            if (
                not key.in_pocket
                and self.actual_room == key.room_number
                and (120 > self.hero.x - key.place_on_floor >= 0)
            ):
                # ustawiamy klucz jako znaleziony
                key.in_pocket = True
                # i sprawdzamy, czy znaleźliśmy już wszystkie klucze
                self.all_keys_found = check_all_keys(self.keys_in_pocket)

    def update_game(self):
        """ ta metoda będzie wywoływana z funkcji update() programu głównego """

        if not self.game_start and keyboard.space:
            self.game_start = True
            self.start_time = datetime.now()

        if keyboard.q:
            quit()

        if self.game_start:
            if keyboard.right:
                self.hero_move("right")
            if keyboard.left:
                self.hero_move("left")
            if keyboard.up:
                self.enter_door()
            if keyboard.down:
                self.get_key()
            if self.all_keys_found:
                self.show_hidden_door = True

    def draw_scene(self):
        """ ta metoda będzie wywoływana z funkcji draw() programu głównego """

        # rysujemy tło
        screen.blit(self.background_active, self.background_position)

        if self.game_start:
            # rysujemy torbę z kluczami
            self.draw_pocket()
            # rysujemy klucz, jeśli jest w tym pomieszczeniu
            self.draw_key()
            # rysujemy głównego bohatera bazując na jego danych
            self.hero.draw()

        elif self.game_finish:
            pass
        else:
            self.draw_intro()


class Key:
    def __init__(self, file_name, in_pocket, room_number, place_on_floor):
        """ self oznacza *siebie samego* - czyli konkretny klucz """

        # te właściwości obiektu *self* przepisywane są z parametrów
        self.file_name = file_name
        self.in_pocket = in_pocket
        self.room_number = room_number
        self.place_on_floor = place_on_floor

    # na razie nie robimy nic
    pass


class Door:
    def __init__(self, room_number, door_position, next_room_number, open):
        """ self oznacza *siebie samego* - czyli konkretne drzwii """

        self.room_number = room_number
        # każde drzwi mają pewne wymiary (235 pixeli), więc obliczamy lewy i prawy koniec
        self.x_left_door = door_position - (236 / 2)
        self.x_right_door = door_position + (236 / 2)
        self.next_room_number = next_room_number
        self.open = open

    # na razie nie robimy nic
    pass


class Room:
    def __init__(self, room_number, room_name, can_move_lr, file_name, doors=[]):

        self.room_number = room_number
        self.room_name = room_name
        # czy z pomieszczenia prowadzą przejścia, w lewo i prawo
        # zmienne typu lewo/prawo/góra dół nie muszą występować wszystkie jednocześnie
        # można w tym celu nadać jakieś "flagi" (wartości) dla poszczególnych możliwości
        # np. 0 - brak wyjść, 1 tylko w lewo, 2, tylko w prawo, 3 w lewo i w prawo
        self.can_move_lr = can_move_lr
        # nazwa pliku z tłem pokoju
        self.file_name = file_name
        # lista drzwi znajdujących się w pokoju - domyślnie pusta lista []
        self.doors = doors

    # na razie nie robimy nic
    pass


# podstawowe zmienne
background_active = "corridor-01.jpg"

# tworzymy klucze, a jako *self* będą przypisane nazwy zmiennych key_
key_00 = Key("key-00.png", False, 11, 1025)
key_01 = Key("key-01.png", False, 17, 80)
key_02 = Key("key-02.png", False, 16, 850)
key_03 = Key("key-03.png", False, 4, 950)
key_04 = Key("key-04.png", False, 0, 370)

# tworzymy drzwi zgodnie z planem pomieszczeń
# domyślnie każde z drzwi będzie otwarte
door_00 = Door(0, 963, 5, True)
door_01 = Door(3, 962, 8, True)
door_02 = Door(5, 307, 15, True)
door_03 = Door(5, 967, 0, True)
door_04 = Door(6, 337, 11, True)
door_05 = Door(7, 932, 17, True)
door_06 = Door(8, 767, 3, True)
door_07 = Door(8, 327, 13, False)
door_08 = Door(11, 327, 6, True)
door_09 = Door(13, 327, 8, True)
door_10 = Door(15, 307, 5, True)
door_11 = Door(17, 932, 7, True)

# tworzymy opisy pomieszczeń zgodnie z planem, najpierw tworzymy instancje klasy Room
room_00 = Room(0, "Przyroda 01", 2, "nature-01.jpg", [door_00])
room_01 = Room(1, "Przyroda 02", 1, "nature-02.jpg")
room_03 = Room(3, "Sala Gimnastyczna 01", 2, "gym-01.jpg", [door_01])
room_04 = Room(4, "Sala Gimnastyczna 02", 1, "gym-02.jpg")
room_05 = Room(5, "Korytarz 01 lewy", 2, "corridor-01.jpg", [door_02, door_03])
room_06 = Room(6, "Korytarz 02", 3, "corridor-02.jpg", [door_04])
room_07 = Room(7, "Korytarz 03", 3, "corridor-03.jpg", [door_05])
room_08 = Room(8, "Korytarz 04 prawy", 1, "corridor-04.jpg", [door_06, door_07])
room_11 = Room(11, "WC", 0, "wc.jpg", [door_08])
room_13 = Room(13, "Aula", 0, "assembly-hall.jpg", [door_09])  # Tego nie ma na mapie !
room_15 = Room(15, "Matematyka 01", 2, "maths-01.jpg", [door_10])
room_16 = Room(16, "Matematyka 02", 1, "maths-02.jpg")
room_17 = Room(17, "Informatyka 01", 2, "computer-science-01.jpg", [door_11])
room_18 = Room(18, "Informatyka 02", 1, "computer-science-02.jpg")

# następnie tworzymy słownik odpowiadający numeracją układowi pomieszczeń na mapie
rooms_in_game = {
    0: room_00,
    1: room_01,
    3: room_03,
    4: room_04,
    5: room_05,
    6: room_06,
    7: room_07,
    8: room_08,
    11: room_11,
    13: room_13,
    15: room_15,
    16: room_16,
    17: room_17,
    18: room_18,
}


# tworzymy zmienną gry
game = Game(background_active, rooms_in_game)


def update():
    game.update_game()


def draw():
    game.draw_scene()
