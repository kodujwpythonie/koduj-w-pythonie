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
          # wypisujemy na ekranie nazwę pomieszczenia
          nazwa = self.rooms[self.actual_room].room_name
          screen.draw.text(nazwa, (10,10), fontsize=15)

      elif self.game_finish:
          pass
      else:
          self.draw_intro()
