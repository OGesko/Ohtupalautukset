import requests
from player import Player, PlayerReader, PlayerStats
from rich.console import Console
from rich.table import Table

def main():
    seasons = {
        "2018-19": "https://studies.cs.helsinki.fi/nhlstats/2018-19/players",
        "2019-20": "https://studies.cs.helsinki.fi/nhlstats/2019-20/players",
        "2020-21": "https://studies.cs.helsinki.fi/nhlstats/2020-21/players",
        "2021-22": "https://studies.cs.helsinki.fi/nhlstats/2021-22/players",
        "2022-23": "https://studies.cs.helsinki.fi/nhlstats/2022-23/players",
        "2023-24": "https://studies.cs.helsinki.fi/nhlstats/2023-24/players",
        "2024-25": "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    }

    console = Console()

    console.print("Select season [2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/2024-25]: ")
    season = input()

    console.print("Select nationality [AUT/CZE/AUS/SWE/GER/DEN/SUI/SVK/NOR/RUS/CAN/LAT/BLR/SLO/USA/FIN/GBR]: ")
    nationality = input().upper()

    url = seasons[season]
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(nationality)

    table = Table(title=f"Top scorers of {nationality} season {season}")

    table.add_column("name", justify="left", style="cyan", no_wrap=True)
    table.add_column("team", justify="center", style="magenta")
    table.add_column("goals", justify="right", style="green")
    table.add_column("assists", justify="right", style="green")
    table.add_column("points", justify="right", style="green")

    for player in players:
        table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.points()))

    console.print(table)

if __name__ == "__main__":
    main()
