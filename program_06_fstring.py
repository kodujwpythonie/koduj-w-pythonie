# przykład wykorzystania f-string - od Python 3.6
# PEP 498 -- Literal String Interpolation
# https://www.python.org/dev/peps/pep-0498/
# przykład - Adam Jurkiewicz - https://github.com/abixadamj
#
from datetime import datetime
autor = "Adam Jurkiewicz"
rok_urodzenia = 1974
miasto_urodzenia = "Poznań"
aktualny_rok = datetime.now().year
wiek = aktualny_rok - rok_urodzenia

print("Oto przykład wykorzystania f-string.")
print(f"Autor książki to {autor}.")
print(f"Urodził się w roku {rok_urodzenia} w mieście {miasto_urodzenia}.")
print(f"Teraz mamy rok {aktualny_rok}, więc ma lat {wiek}.")
