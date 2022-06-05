import pygame as pg
from Punkt import Punkt
from Kierunek import Kierunek
import random
from Zwierzeta import Antylopa, CyberOwca, Lis, Owca, Wilk, Zolw, Czlowiek
from Rosliny import BarszczSosnowskiego, Guarana, Mlecz, Trawa, WilczeJagody
import os.path

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1000
SURFACE_HEIGHT = 0.7 * SCREEN_HEIGHT
SURFACE_WIDTH = 0.7 * SCREEN_WIDTH


class Swiat:
    __NAZWY_ORGANIZMOW = ["Czlowiek", "Wilk", "Owca", "Lis", "Antylopa", "Zolw", "CyberOwca", "Mlecz", "Trawa",
                          "Guarana", "WilczeJagody", "BarszczSosnowskiego"]
    __NAZWY_ZWIERZAT = ["Czlowiek", "Wilk", "Owca", "Lis", "Antylopa", "Zolw", "CyberOwca"]
    __ikonki = {}
    __nr_tury = 0
    __kontynuuj = True
    __organizmy = []
    __liczba_organizmow = 0
    __komentarze = []

    def __init__(self, n, m):
        self.__czlowiek = None
        self.__wysokosc = n
        self.__szerokosc = m
        self.UNIT_SIZE = int(SURFACE_WIDTH / max(m, n))
        pg.init()
        self.__ekran = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
        self.__plansza = pg.Surface((SURFACE_WIDTH, SURFACE_HEIGHT)).convert()
        for typ in self.__NAZWY_ORGANIZMOW:
            img = pg.image.load(os.path.join("Ikony", typ + ".png"))
            img_scaled = pg.transform.scale(img, (self.UNIT_SIZE, self.UNIT_SIZE))
            self.__ikonki[typ] = img_scaled

    def __ustal_kolejnosc(self):
        last_org = None
        for org in self.__organizmy:
            if last_org and org > last_org:
                org, last_org = last_org, org
            else:
                last_org = org

    def kontynuuj(self):
        return self.__kontynuuj

    def get_wysokosc(self):
        return self.__wysokosc

    def get_szerokosc(self):
        return self.__szerokosc

    def get_czlowiek(self):
        return self.__czlowiek

    def get_nr_tury(self):
        return self.__nr_tury

    def __update_info_organizmow(self):
        for org in self.__organizmy:
            org.update_wiek_i_rozmnazanie()

    def __usun_martwe(self):
        for org in self.__organizmy:
            if not org.zyje():
                self.__organizmy.remove(org)
                self.__liczba_organizmow -= 1

    def wykonaj_ture(self, kierunek):
        self.__nr_tury += 1
        self.__update_info_organizmow()
        self.__ustal_kolejnosc()
        last_org = None
        for org in self.__organizmy:
            if org == last_org:
                continue
            org.akcja(kierunek)
            last_org = org

        self.__usun_martwe()
        self.rysuj()

    def rysuj_organizmy(self):
        for org in self.__organizmy:
            if org.zyje():
                self.__plansza.blit(self.__ikonki[org.to_string()],
                                    (org.get_pozycja().x * self.UNIT_SIZE, org.get_pozycja().y * self.UNIT_SIZE))

    def rysuj(self):
        self.__ekran.fill((255, 255, 255))  # Bialy
        self.__plansza.fill("#BEBEBE")  # Jasno szary
        self.rysuj_organizmy()
        self.__ekran.blit(self.__plansza, (0, 0))
        pg.display.update()

    def get_sasiad(self, pole, kierunek):
        temp = Punkt(pole.y, pole.x)
        match kierunek:
            case Kierunek.PRAWO:
                if temp.x < self.__szerokosc - 1:
                    temp.x += 1
            case Kierunek.DOL:
                if temp.y < self.__wysokosc - 1:
                    temp.y += 1
            case Kierunek.LEWO:
                if temp.x > 0:
                    temp.x -= 1
            case Kierunek.GORA:
                if temp.y > 0:
                    temp.y -= 1
        return temp

    def nowy_organizm(self, typ_organizmu, pole):
        match typ_organizmu:
            case "Antylopa":
                return Antylopa.Antylopa(pole, self)
            case "Wilk":
                return Wilk.Wilk(pole, self)
            case "Owca":
                return Owca.Owca(pole, self)
            case "Lis":
                return Lis.Lis(pole, self)
            case "Zolw":
                return Zolw.Zolw(pole, self)
            case "CyberOwca":
                return CyberOwca.CyberOwca(pole, self)

            case "Mlecz":
                return Mlecz.Mlecz(pole, self)
            case "Trawa":
                return Trawa.Trawa(pole, self)
            case "Guarana":
                return Guarana.Guarana(pole, self)
            case "WilczeJagody":
                return WilczeJagody.WilczeJagody(pole, self)
            case "BarszczSosnowskiego":
                return BarszczSosnowskiego.BarszczSosnowskiego(pole, self)

            case "Czlowiek":
                return Czlowiek.Czlowiek(pole, self)

    def dodaj_organizm(self, organizm):
        self.__organizmy.insert(0, organizm)
        self.__liczba_organizmow += 1

    def czy_zwierze(self, organizm):
        return organizm.__class__.__name__ in self.__NAZWY_ZWIERZAT

    def sprawdz_pole(self, pole):
        for org in self.__organizmy:
            if org.get_pozycja() == pole:
                return org
        return None

    def nowa_gra(self):
        self.__czlowiek = Czlowiek.Czlowiek(Punkt(self.__wysokosc // 2, self.__szerokosc // 2), self)
        self.dodaj_organizm(self.__czlowiek)
        typy = ["Wilk", "Owca", "Lis", "Antylopa", "Zolw", "CyberOwca",
                "Mlecz", "Trawa", "Guarana", "WilczeJagody", "BarszczSosnowskiego"]
        for i in range(2):
            for typ in typy:
                pozycja_dodawanego_organizmu = Punkt(random.randrange(self.__wysokosc),
                                                     random.randrange(self.__szerokosc))
                while self.sprawdz_pole(pozycja_dodawanego_organizmu) is not None:
                    pozycja_dodawanego_organizmu.y = random.randrange(self.__wysokosc)
                    pozycja_dodawanego_organizmu.x = random.randrange(self.__szerokosc)

                self.dodaj_organizm(self.nowy_organizm(typ, pozycja_dodawanego_organizmu))
        self.rysuj()

    def get_organizmy(self):
        return self.__organizmy

    def test(self):
        self.rysuj()
