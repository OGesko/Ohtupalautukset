class TennisGame:

    score_names = ["Love", "Fifteen", "Thirty", "Forty"]

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.scores = {player1_name: 0, player2_name: 0}

    def won_point(self, player_name):
        self.scores[player_name] += 1

    def get_score(self):
        player1_score = self.scores[self.player1_name]
        player2_score = self.scores[self.player2_name]

        if player1_score == player2_score:
            return self.tied_score(player1_score)

        elif player1_score >= 4 or player2_score >= 4:
            return self.advantage_or_win(player1_score, player2_score)
        
        return f"{self.score_names[player1_score]}-{self.score_names[player2_score]}"

    def tied_score(self, score):
        if score < 3:
            return f"{self.score_names[score]}-All"
        return "Deuce"

    def advantage_or_win(self, player1_score, player2_score):
        difference = player1_score - player2_score

        if difference == 1:
            return f"Advantage {self.player1_name}"
        elif difference == -1:
            return f"Advantage {self.player2_name}"
        elif difference >= 2:
            return f"Win for {self.player1_name}"
        else:
            return f"Win for {self.player2_name}"
