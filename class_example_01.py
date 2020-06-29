class Key:
    key_type = None
    key_open = None
    key_color = None

    def do_open(self):
        print(f"Klucz {self.key_type} otwiera {self.key_open}.")

    def information(self):
        print(f"Klucz {self.key_type} otwiera {self.key_open}, ma kolor {self.key_color}.")

# tworzymy obiekt i przypisujemy właściwości
key_01 = Key()
key_01.key_type = "Yeti"
key_01.key_open = "drzwi"
key_01.key_color = "czerwony"

# tworzymy obiekt i przypisujemy właściwości
key_02 = Key()
key_02.key_type = "Yeti-2"
key_02.key_open = "kłódkę"
key_02.key_color = "niebieski"

# wykonujemy metody dla obiektów
key_01.information()
key_01.do_open()
key_02.information()
key_02.do_open()
