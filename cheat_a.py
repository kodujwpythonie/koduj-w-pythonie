# w metodzie update_game() w linii 254 wprowadzić modyfikację:

def update_game(self):
    """ ta metoda będzie wywoływana z funkcji update() programu głwnego """

    if not self.game_start and keyboard.space:
        self.game_start = True
        self.start_time = datetime.now()

    if keyboard.q:
        quit()

    if self.game_start:

        # poniższe pozwala "szybko" zakończyć grę poprzez ustawienie opcji
        if keyboard.a:
            for key in self.keys_in_pocket:
                print(f"Ustawiam klucz: {key}")
                key.in_pocket = True
                self.all_keys_found = True
                self.rooms[8].doors[1].open = True

        if keyboard.right:
            self.hero_move("right")
