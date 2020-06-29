class Testowy:

    def __init__(self, start, elementy = []):
        self.licznik = start
        self.elementy = elementy

    def info(self):
        print(f"Licznik wynosi: {self.licznik}")
        print(f"Elementy to: {self.elementy}")

    def zeruj_licznik(self):
        self.licznik = 0

test_gry = Testowy(1)

def draw():
    test_gry.info()

def update():
    test_gry.licznik += 1
    test_gry.elementy.append(test_gry.licznik)

    if test_gry.licznik > 10:
        test_gry.zeruj_licznik()
        test_gry.elementy = []