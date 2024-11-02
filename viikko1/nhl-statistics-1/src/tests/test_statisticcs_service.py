import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_no_player(self):
        player = self.stats.search("NoPlayer")
        self.assertIsNone(player)

    def test_player(self):
        player = self.stats.search("Semenko")
        self.assertEqual(player.name, "Semenko")

    def test_team_stats(self):
        team = self.stats.team("EDM")
        self.assertEqual(len(team), 3)
        self.assertEqual(team[0].name, "Semenko")
        self.assertEqual(team[1].name, "Kurri")
        self.assertEqual(team[2].name, "Gretzky")


    def test_top_stats(self):
        top_players = self.stats.top(3)
        self.assertEqual(top_players[0].points, 124)
        self.assertEqual(top_players[1].points, 99)
        self.assertEqual(top_players[2].points, 98)
