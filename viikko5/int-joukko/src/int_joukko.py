KAPASITEETTI = 5
OLETUSKASVATUS = 5


class IntJoukko:
    # tämä metodi on ainoa tapa luoda listoja
    def _luo_lista(self, koko):
        return [0] * koko

    def __init__(self, kapasiteetti=KAPASITEETTI, kasvatuskoko=OLETUSKASVATUS):
        if not isinstance(kapasiteetti, int) or kapasiteetti < 0:
            raise ValueError("kapasiteetti oltava positiivinen luku")
        if not isinstance(kasvatuskoko, int) or kasvatuskoko < 0:
            raise ValueError("kasvatuskoko oltava positiivinen luku")

        self.kapasiteetti = kapasiteetti
        self.kasvatuskoko = kasvatuskoko
        self.alkiot = self._luo_lista(self.kapasiteetti)
        self.alkioiden_lkm = 0

    def kuuluu(self, n):
        return n in self.alkiot

    def lisaa(self, n):
        if self.kuuluu(n):
            return False

        self.alkiot[self.alkioiden_lkm] = n
        self.alkioiden_lkm += 1

        # Resize if needed
        if self.alkioiden_lkm == len(self.alkiot):
            uusi_koko = self.alkioiden_lkm + self.kasvatuskoko
            uusi_lista = self._luo_lista(uusi_koko)
            self.kopioi_lista(self.alkiot, uusi_lista)
            self.alkiot = uusi_lista

        return True

    def poista(self, n):
        for i in range(self.alkioiden_lkm):
            if self.alkiot[i] == n:
                self._siirra_alkioita_vasemmalle(i)
                self.alkioiden_lkm -= 1
                return True
        return False

    def _siirra_alkioita_vasemmalle(self, alkaen_indeksi):
        for i in range(alkaen_indeksi, self.alkioiden_lkm - 1):
            self.alkiot[i] = self.alkiot[i + 1]
        self.alkiot[self.alkioiden_lkm - 1] = 0

    def kopioi_lista(self, a, b):
        for i in range(0, len(a)):
            b[i] = a[i]

    def mahtavuus(self):
        return self.alkioiden_lkm

    def to_int_list(self):
        return self.alkiot[:self.alkioiden_lkm]

    @staticmethod
    def yhdiste(a, b):
        tulos = IntJoukko()
        for alkio in a.to_int_list():
            tulos.lisaa(alkio)
        for alkio in b.to_int_list():
            tulos.lisaa(alkio)
        return tulos

    @staticmethod
    def leikkaus(a, b):
        tulos = IntJoukko()
        for alkio in a.to_int_list():
            if b.kuuluu(alkio):
                tulos.lisaa(alkio)
        return tulos

    @staticmethod
    def erotus(a, b):
        tulos = IntJoukko()
        for alkio in a.to_int_list():
            if not b.kuuluu(alkio):
                tulos.lisaa(alkio)
        return tulos

    def __str__(self):
        alkiot_str = ", ".join(str(self.alkiot[i]) for i in range(self.alkioiden_lkm))
        return f"{{{alkiot_str}}}"
