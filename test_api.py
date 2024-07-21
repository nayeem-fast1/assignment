import os
from collections import defaultdict
from configparser import ConfigParser
from pathlib import Path

import pytest
import requests


## Grab data from ini file
base_dir = Path(__file__).resolve().parents[1]
config_file = os.path.join(base_dir, "config.ini")
config = ConfigParser()
config.read(config_file)
site_url = config['api']['site_url']
url = config['api']['url']




def test_teams_count():

    response = requests.get(site_url, verify=False)
    data = response.json()

    # Verify the count of teams
    assert len(data["teams"]) == 32, f"Expected 32 teams, but got {len(data['teams'])}"


def test_oldest_team():

    response = requests.get(site_url, verify=False)
    data = response.json()

    # Find the oldest team by founded year
    oldest_team = min(data["teams"], key=lambda team: team["founded"])

    # Verify the oldest team is Montreal Canadiens
    assert oldest_team[
               "name"] == "Montreal Canadiens", f"Expected oldest team to be Montreal Canadiens, but got {oldest_team['name']}"


def test_city_with_multiple_teams():

    response = requests.get(site_url, verify=False)
    data = response.json()

    # Create a dictionary to store the count of teams per city
    city_teams = defaultdict(list)
    for team in data["teams"]:
        city_teams[team["location"]].append(team["name"])

    # Find cities with more than one team
    cities_with_multiple_teams = {city: teams for city, teams in city_teams.items() if len(teams) > 1}

    # Verify that there is at least one city with more than one team
    assert len(cities_with_multiple_teams) > 0, "No city has more than one team."

    # Print the cities with multiple teams and their team names
    for city, teams in cities_with_multiple_teams.items():
        print(f"City: {city}, Teams: {teams}")

def test_metropolitan_division():
    response = requests.get(site_url, verify=False)
    data = response.json()


    # Filter teams in the Metropolitan division
    metropolitan_teams = [team["name"] for team in data["teams"] if team["division"]["name"] == "Metropolitan"]

    # Verify the count of teams in the Metropolitan division
    assert len(metropolitan_teams) == 8, f"Expected 8 teams in the Metropolitan division, but got {len(metropolitan_teams)}"
    print(metropolitan_teams)


if __name__ == "__main__":
    pytest.main()