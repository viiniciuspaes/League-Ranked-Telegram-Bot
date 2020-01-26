import requests
import configuration as con

account_info = {
        "name": "",
        "summoner_level": "",
        "revision": "",
        "id": "",
        "puuid": ""
    }

def update_account_secure_info(sumoner_name, account_info, api_key):
    
    summoner_request_str = "https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(sumoner_name, api_key)

    resp_summoner = requests.get(summoner_request_str)
    if resp_summoner.status_code == 400:
        return Exception("Error response code: {}".format(resp_summoner.status_code))

    resp_summoner = resp_summoner.json()
    account_info["name"] = resp_summoner["name"]
    account_info["summoner_level"] = resp_summoner["summonerLevel"]
    account_info["revision"] = resp_summoner["revisionDate"]
    account_info["id"] = resp_summoner["id"]
    account_info["puuid"] = resp_summoner["puuid"]

    return account_info

def get_mastered_champions_summoner(account_id, api_key):

    champion_request_str = "https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{}?api_key={}".format(account_id, api_key)

    response_champion = requests.get(champion_request_str)
    if response_champion.status_code == 400:
        print("Error response code: {}".format(response_champion.status_code))

    return len(response_champion.json())

def get_ranked_info_summoner(account_id, api_key):

    league_request_str = "https://br1.api.riotgames.com/lol/league/v4/entries/by-summoner/{}?api_key={}".format(account_id, api_key)

    resp_league = requests.get(league_request_str)
    if resp_league.status_code == 400:
        return Exception("Error response code: {}".format(resp_league.status_code))
    
    league_queues = []
    
    resp_league = resp_league.json()
    for league in resp_league:
        queue_dict = {"queue_type": league["queueType"], "tier": league["tier"], "rank": league["rank"],
                    "wins": league["wins"], "loses": league["losses"], "pdl": league["leaguePoints"], "win_rate": "",
                    "total_matches": int(league["wins"]) + int(league["losses"])}
        queue_dict["win_rate"] = str(int((int(league["wins"]) / int(queue_dict["total_matches"]))*100)) + "%"
        league_queues.append(queue_dict)

    return league_queues
