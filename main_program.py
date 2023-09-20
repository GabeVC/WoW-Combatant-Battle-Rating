import api as api
from player import Player
import sys
import json


def main(code):
    fights = api.get_fights(code)
    temp = []
    for fight in fights.items():
        print(fight[0], fight[1])
        temp.append(fight)
    fight = int(input("Please input what number fight you would like to review: "))
    print(fights[fight][1])
    if fights[fight][1] == "Kazzara, the Hellforged":
        temp3 = create_players(fight, code)
        players = kazzara(code, fight, temp3)
    elif fights[fight][1] == "The Amalgamation Chamber":
        temp3 = create_players(fight, code)
        players = shadowflame(code, fight, temp3)
    elif fights[fight][1] == "Assault of the Zaqali":
        temp3 = create_players(fight, code)
        players = zaqali(code, fight, temp3)
    elif fights[fight][1] == "The Forgotten Experiments":
        temp3 = create_players(fight, code)
        players = experiments(code, fight, temp3)
    elif fights[fight][1] == "Rashok, the Elder":
        temp3 = create_players(fight, code)
        players = rashok(code, fight, temp3)
    elif fights[fight][1] == "The Vigilant Steward, Zskarn":
        temp3 = create_players(fight, code)
        players = zskarn(code, fight, temp3)
    elif fights[fight][1] == "Magmorax":
        temp3 = create_players(fight, code)
        players = magmorax(code, fight, temp3)
    elif fights[fight][1] == "Echo of Neltharion":
        temp3 = create_players(fight, code)
        players = neltharion(code, fight, temp3)
    elif fights[fight][1] == "Scalecommander Sarkareth":
        temp3 = create_players(fight, code)
        players = sarkareth(code, fight, temp3)

    players.sort(key=lambda x: x.score, reverse=True)
    for player in players:
        print(player)


def add_parses(players, fight_id, code):
    parses = api.get_parses(code, fight_id)
    for parse in parses.items():
        name = parse[0]
        for player in players:
            if player.name == name:
                player.update_score(parse[1][0])
                player.set_role(parse[1][1])
    return players


def create_players(fight_id, code):
    players = []
    actors = api.get_actors(code)
    combatants = api.get_combatants(code, fight_id)
    fights = api.get_fights(code)

    for combatant in combatants.items():
        for player in combatant[1]:  # the list of playerIDs
            players.append(Player(actors[player], player))
    for fight in fights.items():
        if fight[0] == fight_id:
            if fight[1][2] == True:
                add_parses(players, fight_id, code)
            else:
                for player in players:
                    (player.update_score(50))

    return players


def kazzara(code, fight_id, players):
    for player in players:
        temp = api.get_damage_taken_kazzara(code, fight_id, player.player_id)
        player.update_score(-(temp // 100000))
        player.damaged_points(temp // 100000)
        player.gained_points(0)
    return players


def shadowflame(code, fight_id, players):
    for player in players:
        temp = api.get_damage_taken_shadowflame(code, fight_id, player.player_id)
        player.update_score(-(temp[0] // 100000))
        player.damaged_points(temp[0] // 100000)
        player.update_score(temp[1])
        player.gained_points(temp[1])
    return players


def zaqali(code, fight_id, players):
    for player in players:
        temp = api.get_damage_taken_zaqali(code, fight_id, player.player_id)
        player.update_score(-temp[0] // 100000)
        player.damaged_points(temp[0] // 100000)
        player.update_score(temp[1])
        player.gained_points(temp[1])
    return players


def experiments(code, fight_id, players):
    for player in players:
        temp = api.get_damage_taken_experiments(code, fight_id, player.player_id)
        player.update_score(-(temp // 100000))
        player.damaged_points(temp // 100000)
        player.gained_points(0)
    return players


def rashok(code, fight_id, players):
    for player in players:
        temp = api.get_soaks_done_rashok(code, fight_id, player.player_id)
        player.update_score(-temp[0] // 100000)
        player.update_score(temp[1] * 2)
        player.damaged_points(temp[0] // 100000)
        player.gained_points(temp[1])
    return players


def zskarn(code, fight_id, players):
    for player in players:
        temp = api.get_stats_zskarn(code, fight_id, player.player_id)
        player.update_score(-temp[0] // 100000)
        player.update_score(temp[1])
        player.damaged_points(temp[0] // 100000)
        player.gained_points(temp[1])
    return players


def magmorax(code, fight_id, players):
    for player in players:
        temp = api.get_stats_magmorax(code, fight_id, player.player_id)
        player.update_score(-temp[0] // 100000)
        player.update_score(temp[1])
        player.damaged_points(temp[0] // 100000)
        player.gained_points(temp[1])
    return players


def neltharion(code, fight_id, players):
    for player in players:
        temp = api.get_damage_neltharion(code, fight_id, player.player_id)
        player.update_score(-(temp // 100000))
        player.damaged_points(temp // 100000)
        player.gained_points(0)
    return players


def sarkareth(code, fight_id, players):
    for player in players:
        temp = api.get_stats_sarkareth(code, fight_id, player.player_id)
        player.update_score(-temp[0] // 100000)
        player.damaged_points(temp[0] // 100000)
        player.update_score(temp[1] * 2)
        player.gained_points(temp[1])
    return players


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python your_script.py <log_code>")
        sys.exit(1)

    code = sys.argv[1]
    main(code)
