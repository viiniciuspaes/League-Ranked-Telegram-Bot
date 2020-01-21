import requests
api_key = "<insert API key>"
summoner_name = input("Summoner Name: ")

header_params = {
    "api_key": "",
    "player_id": "",
    "name": ""
}

account_info = {
    "name": "",
    "summoner_level": "",
    "revision": "",
    "ranked": [],
    "total_champions": ""
}

summoner_request_str = "https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(summoner_name, api_key)

response_summoner = requests.get(summoner_request_str)
if response_summoner.status_code == 400:
    print("Error response code: {}".format(response_summoner.status_code))

value = response_summoner.json()

account_info["name"] = summoner_name
account_info["summoner_level"] = value["summonerLevel"]
account_info["revision"] = value["revisionDate"]

summoner_id = value["id"]

league_request_str = "https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{}?api_key={}".format(summoner_id,api_key)
champion_request_str = "https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{}?api_key={}".format(summoner_id, api_key)

response_league = requests.get(league_request_str)
if response_league.status_code == 400:
    print("Error response code: {}".format(response_league.status_code))

value = response_league.json()

for league in value:
    queue_dict = {"queue_type": league["queueType"], "tier": league["tier"], "rank": league["rank"],
                  "wins": league["wins"], "loses": league["losses"], "pdl": league["leaguePoints"], "win_rate": "",
                  "total_matches": int(league["wins"]) + int(league["losses"])}
    queue_dict["win_rate"] = str(int((int(league["wins"]) / int(queue_dict["total_matches"]))*100)) + "%"
    account_info["ranked"].append(queue_dict)

response_champion = requests.get(champion_request_str)
if response_champion.status_code == 400:
    print("Error response code: {}".format(response_champion.status_code))

value = response_champion.json()
account_info["total_champions"] = len(value)

print("Summoner Name: {}".format(account_info["name"]))
print("Summoner Level: {}".format(account_info["summoner_level"]))
print("Total Champions with Mastery: {}".format(account_info["total_champions"]))
for league in account_info["ranked"]:
    print("Queue Type: {}".format(league["queue_type"]))
    print("     Tier: {}".format(league["tier"]))
    print("     Rank: {}".format(league["rank"]))
    print("     Total Matches: {}".format(league["total_matches"]))
    print("     Wins: {}".format(league["wins"]))
    print("     Loses: {}".format(league["loses"]))
    print("     Win Rate: {}".format(league["win_rate"]))
    print("     PDL: {}".format(league["pdl"]))

    print("----------------------------------")
print("\nLast Update: {}".format(account_info["revision"]))
