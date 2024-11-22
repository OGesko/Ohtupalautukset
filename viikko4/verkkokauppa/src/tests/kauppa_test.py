import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote
from ostoskori import Ostoskori

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.kori_mock = Mock(spec=Ostoskori)

        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock = Mock()
        self.varasto_mock.palauta_varastoon = Mock()
        
        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            saldot = {1: 10, 2: 5, 3: 0}  # Tuote 3 on loppu
            return saldot.get(tuote_id, 0)

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            elif tuote_id == 2:
                return Tuote(2, "leipä", 3)
            return None

        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote
    
        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)
        self.kori_mock.poista = Mock()

    def test_os(self):
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_tilisiirto_oikeilla_parametreilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)

    def test_kaksi_eri_tuotetta_korissa(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 8)

    def test_kaksi_samaa_tuotetta_korissa(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 10)

    def test_tuote_loppu_varastosta(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)

    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        # Ensimmäinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # Maito, hinta 5
        self.kauppa.tilimaksu("pekka", "12345")

        # Tarkista, että ensimmäisen ostoksen summa on oikein
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", ANY, 5)

        # Aloitetaan uusi asiointi ja tehdään uusi ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)  # Leipä, hinta 3
        self.kauppa.tilimaksu("matti", "67890")

        # Tarkista, että uuden ostoksen summa ei sisällä vanhaa summaa
        self.pankki_mock.tilisiirto.assert_called_with("matti", 42, "67890", ANY, 3)

    def test_uusi_viitenumero_jokaiselle_maksutapahtumalle(self):
        # Ensimmäinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)  # Maito, hinta 5
        self.kauppa.tilimaksu("pekka", "12345")

        # Tarkista, että viitegeneraattorin `uusi`-metodia kutsutaan
        self.viitegeneraattori_mock.uusi.assert_called()

        # Tarkista ensimmäisen ostoksen viitenumero
        self.viitegeneraattori_mock.uusi.assert_called_with()
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 1)

        # Toinen ostos
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)  # Leipä, hinta 3
        self.kauppa.tilimaksu("matti", "67890")

        # Tarkista, että viitegeneraattorin `uusi`-metodia kutsutaan uudelleen
        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

    def test_poista_korista_palauttaa_tuotteen_varastoon(self):
        # Alustetaan asiointi ja lisätään tuote koriin
        self.kauppa.aloita_asiointi()
        tuote = Tuote(1, "maito", 5)
        self.kauppa._ostoskori.poista = Mock()
        self.kauppa.lisaa_koriin(1)

        # Poistetaan tuote korista
        self.kauppa.poista_korista(1)

        # Varmistetaan, että varaston `hae_tuote`-metodia kutsuttiin
        self.varasto_mock.hae_tuote.assert_called_with(1)

        # Varmistetaan, että tuotetta poistettiin ostoskorista
        self.kauppa._ostoskori.poista.assert_called_once_with(tuote)

        # Varmistetaan, että tuote palautettiin varastoon
        self.varasto_mock.palauta_varastoon.assert_called_with(tuote)
