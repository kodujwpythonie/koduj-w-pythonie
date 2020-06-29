    def update_game(self):
        """ ta metoda będzie wywoływana z funkcji update() programu głwnego """

        if not self.game_start and keyboard.space:
            self.game_start = True
            self.start_time = datetime.now()
            print(f"Test game_start = {self.game_start}")

            if keyboard.q:
                print("To jest koniec")
                quit()

        if self.game_start:
            if keyboard.right:
                self.hero_move("right")
            if keyboard.left:
                self.hero_move("left")
