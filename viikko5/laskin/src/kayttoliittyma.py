from enum import Enum
from tkinter import ttk, constants, StringVar


class Komento(Enum):
    SUMMA = 1
    EROTUS = 2
    NOLLAUS = 3
    KUMOA = 4


class Kayttoliittyma:
    def __init__(self, sovelluslogiikka, root):
        self._sovelluslogiikka = sovelluslogiikka
        self._root = root
        self._viimeisin_komento = None

        def viimeisin_komento_funktio():
            return self._viimeisin_komento

        self._komennot = {
            Komento.SUMMA: Summa(sovelluslogiikka, self._lue_syote),
            Komento.EROTUS: Erotus(sovelluslogiikka, self._lue_syote),
            Komento.NOLLAUS: Nollaus(sovelluslogiikka, self._lue_syote),
            Komento.KUMOA: Kumoa(viimeisin_komento_funktio)
        }

    def kaynnista(self):
        self._arvo_var = StringVar()
        self._arvo_var.set(self._sovelluslogiikka.arvo())
        self._syote_kentta = ttk.Entry(master=self._root)

        tulos_teksti = ttk.Label(textvariable=self._arvo_var)

        summa_painike = ttk.Button(
            master=self._root,
            text="Summa",
            command=lambda: self._suorita_komento(Komento.SUMMA)
        )

        erotus_painike = ttk.Button(
            master=self._root,
            text="Erotus",
            command=lambda: self._suorita_komento(Komento.EROTUS)
        )

        self._nollaus_painike = ttk.Button(
            master=self._root,
            text="Nollaus",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.NOLLAUS)
        )

        self._kumoa_painike = ttk.Button(
            master=self._root,
            text="Kumoa",
            state=constants.DISABLED,
            command=lambda: self._suorita_komento(Komento.KUMOA)
        )

        tulos_teksti.grid(columnspan=4)
        self._syote_kentta.grid(columnspan=4, sticky=(constants.E, constants.W))
        summa_painike.grid(row=2, column=0)
        erotus_painike.grid(row=2, column=1)
        self._nollaus_painike.grid(row=2, column=2)
        self._kumoa_painike.grid(row=2, column=3)

    def _lue_syote(self):
        return self._syote_kentta.get()

    def _suorita_komento(self, komento):
        komento_olio = self._komennot[komento]
        komento_olio.suorita()

        if komento != Komento.KUMOA:
            self._viimeisin_komento = komento_olio

        if self._viimeisin_komento:
            self._kumoa_painike["state"] = constants.NORMAL
        else:
            self._kumoa_painike["state"] = constants.DISABLED

        if self._sovelluslogiikka.arvo() == 0:
            self._nollaus_painike["state"] = constants.DISABLED
        else:
            self._nollaus_painike["state"] = constants.NORMAL

        self._syote_kentta.delete(0, constants.END)
        self._arvo_var.set(self._sovelluslogiikka.arvo())

#    def _kumoa(self):
#        if self._viimeisin_komento:
#            self._viimeisin_komento.kumoa()
#            self._viimeisin_komento = None  # Kumoa disables itself after one use
#
#            self._kumoa_painike["state"] = constants.DISABLED
#            self._arvo_var.set(self._sovelluslogiikka.arvo())


class KomentoRajapinta:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._edellinen_arvo = None

    def suorita(self):
        raise NotImplementedError

    def kumoa(self):
        if self._edellinen_arvo is not None:
            self._sovelluslogiikka.aseta_arvo(self._edellinen_arvo)

class Summa(KomentoRajapinta):
    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        arvo = int(self._lue_syote())
        self._sovelluslogiikka.plus(arvo)

class Erotus(KomentoRajapinta):
    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        arvo = int(self._lue_syote())
        self._sovelluslogiikka.miinus(arvo)


class Nollaus(KomentoRajapinta):
    def suorita(self):
        self._edellinen_arvo = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.nollaa()

class Kumoa:
    def __init__(self, viimeisin_komento_funktio):
        self._viimeisin_komento_funktio = viimeisin_komento_funktio

    def suorita(self):
        viimeisin_komento = self._viimeisin_komento_funktio()
        if viimeisin_komento:
            viimeisin_komento.kumoa()
