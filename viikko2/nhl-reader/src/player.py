import requests
class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.team = dict['team']
        self.goals = dict['goals']
        self.assists = dict['assists']
        self.nationality = dict['nationality']

    def points(self):
        return self.goals + self.assists

    def __str__(self):
        return f"{self.name:20}{self.team:4} {self.goals:2} + {self.assists:2} = {self.points()}"

class PlayerReader:
    def __init__(self, url):
        self.url = url

    def players(self):
        response = requests.get(self.url).json()
        players = []
        for player_dict in response:
            player = Player(player_dict)
            players.append(player)
        return players
    
class PlayerStats:
    def __init__(self, reader):
        self.players = reader.players()

    def top_scorers_by_nationality(self, nationality):
        fPlayers = []
        for p in self.players:
            if p.nationality == nationality:
                fPlayers.append(p)
        return sorted(fPlayers, key=lambda p: p.points(), reverse=True)
