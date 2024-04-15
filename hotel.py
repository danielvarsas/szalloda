from abc import ABC
from datetime import datetime, timedelta
import random


class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.ar = ar
        self.szobaszam = szobaszam

class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)
        self.agyak_szama = 1
        self.letszam = 1

class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam, ar):
        super().__init__(szobaszam, ar)
        self.agyak_szama = 2
        self.letszam = 2

class Szalloda:
    def __init__(self, nev, szobak):
        self.nev = nev
        self.szobak = szobak
        self.foglalasok = []

    def foglal(self, szoba, datum):
        if datum.date() >= datetime.now().date() and not any(f.datum.date() == datum.date() and f.szoba == szoba for f in self.foglalasok):
            self.foglalasok.append(Foglalas(szoba, datum))
            return szoba.ar
        else:
            return "\nA foglalás sikertelen. A szoba már foglalt ezen a dátumon."

    def lemond(self, szobaszam, datum):
        szobaszam = int(szobaszam)
        szoba = next((s for s in self.szobak if s.szobaszam == szobaszam), None)
        if szoba:
            foglalasok = [f for f in self.foglalasok if f.szoba == szoba and f.datum.date() == datum.date()]
            if foglalasok:
                for foglalas in foglalasok:
                    self.foglalasok.remove(foglalas)
                return "\nA foglalás lemondva."
        return "\nA foglalás nem létezik."

    def listaz(self):
        foglalasok = sorted(self.foglalasok, key=lambda f: (f.szoba.szobaszam, f.datum))
        foglalasok_listazva = []
        for foglalas in foglalasok:
            if foglalas.datum.date() >= datetime.now().date():
                foglalasok_listazva.append(f"{foglalas.szoba.szobaszam}. " f"szoba foglalt {foglalas.datum.strftime('%Y-%m-%d')} dátumra")
        return foglalasok_listazva


class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum


def main():
    szobak = [EgyagyasSzoba(1, 25000), KetagyasSzoba(2, 30000), EgyagyasSzoba(3, 25000)]
    szalloda = Szalloda("Gábor Dénes Hotel", szobak)

    #Példafoglalások
    szalloda.foglalasok.append(Foglalas(szobak[0], datetime.now() + timedelta(days=7)))
    szalloda.foglalasok.append(Foglalas(szobak[1], datetime.now() + timedelta(days=1)))
    szalloda.foglalasok.append(Foglalas(szobak[1], datetime.now() + timedelta(days=1)))
    szalloda.foglalasok.append(Foglalas(szobak[2], datetime.now() + timedelta(days=20)))
    szalloda.foglalasok.append(Foglalas(szobak[2], datetime.now() + timedelta(days=20)))


    while True:
        print("""\n 
 .--..--.   .   .     .      . 
:    |   :  |   |    _|_     | 
| --.|   |  |---| .-. |  .-. | 
:   ||   ;  |   |(   )| (.-' | 
 `--''--'   '   ' `-' `-'`--'`-""")
        print("Kérem válasszon az alábbi menüpontok közül:")
        print("1. Szobafoglalás")
        print("2. Foglalás lemondása")
        print("3. Foglalások listája")
        print("4. Kilépés")

        valasztas = input("Válassz egy lehetőséget: ")

        if valasztas == "1":
            print("\nVálasztható szobatípusok:")
            for szoba in szobak:
                szoba_tipus = 'Egyágyas' if isinstance(szoba, EgyagyasSzoba) else 'Kétágyas'
                print(f"Szobaszám: {szoba.szobaszam}, Típus: {szoba_tipus}")
            while True:
                szobaszam = int(input("Add meg a lefoglalni kívánt szoba számát: "))
                szoba = next((szoba for szoba in szobak if szoba.szobaszam == szobaszam), None)
                if szoba is not None:
                    break
                else:
                    print("A szobaszám nem létezik. Adj meg másikat.")
            while True:
                try:
                    datum = datetime.strptime(input("Add meg a dátumot (YYYY-MM-DD): "), "%Y-%m-%d")
                    if datum.date() < datetime.now().date() and datum.date() != datetime.now().date():
                        print("A dátum régebbi mint a mai. Kérlek, add meg újra a dátumot.")
                    else:
                        break
                except ValueError:
                    print("Hibás formátum. Kérlek, add meg újra a dátumot YYYY-MM-DD formában.")
            szoba = next((szoba for szoba in szobak if szoba.szobaszam == szobaszam), None)
            if szoba and all(foglalas.szoba != szoba or foglalas.datum != datum for foglalas in szalloda.foglalasok):
                foglalas_eredmeny = szalloda.foglal(szoba, datum)
                if foglalas_eredmeny != "\nSikertelen. A szoba már foglalt ezen a dátumon.":
                    print(f"\nA foglalás sikeres. \nA foglalás ára: {foglalas_eredmeny} Ft.")
                else:
                    print(foglalas_eredmeny)

        elif valasztas == "2":
            while True:
                szobaszam = int(input("Add meg a törölni kíván foglalás szoba számát: "))
                szoba = next((szoba for szoba in szobak if szoba.szobaszam == szobaszam), None)
                if szoba is not None:
                    break
                else:
                    print("A szobaszám nem létezik. Kérlek, próbáld újra.")
            while True:
                try:
                    datum = datetime.strptime(input("Add meg a dátumot (YYYY-MM-DD): "), "%Y-%m-%d")
                    if datum.date() < datetime.now().date():
                        print("A dátum régebbi mint a mai. Kérlek, add meg újra a dátumot.")
                    else:
                        break
                except ValueError:
                    print("Hibás dátum formátum. Kérlek, add meg újra a dátumot YYYY-MM-DD formában.")
            if szoba:
                print(szalloda.lemond(szoba.szobaszam, datum))
            else:
                print("\nA foglalás nem létezik.")

        elif valasztas == "3":
            reservations = szalloda.listaz()
            if reservations:
                print("\nJelenleg rögzített foglalások:")
                for reservation in reservations:
                    print(reservation)
            else:
                print("\nNincs foglalt szoba")

        elif valasztas == "4":
            break
        else:
            print("\nNincs ilyen lehetőség, válassz egy lehetőséget a felsoroltak közül.")


if __name__ == "__main__":
    main()