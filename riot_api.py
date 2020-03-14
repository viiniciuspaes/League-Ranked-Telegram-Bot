import requests
import constants as con


def update_account_secure_info(sumoner_name):

    account_info = {
        "name": "",
        "summoner_level": "",
        "revision": "",
        "account_id": "",
        "puuid": ""
    }
    
    account_request = con.account_request + "{}?api_key={}".format(sumoner_name, con.api_key)

    resp_summoner = requests.get(account_request)
    if resp_summoner.status_code == 400:
        return Exception("Error response code: {}".format(resp_summoner.status_code))

    resp_summoner = resp_summoner.json()
    account_info["name"] = resp_summoner["name"]
    account_info["summoner_level"] = resp_summoner["summonerLevel"]
    account_info["revision"] = resp_summoner["revisionDate"]
    account_info["id"] = resp_summoner["id"]
    account_info["puuid"] = resp_summoner["puuid"]

    return account_info

def get_mastered_lol_champions(account_id):

    champion_request = con.champion_request + "{}?api_key={}".format(account_id, con.api_key)

    response_champion = requests.get(champion_request)
    if response_champion.status_code == 400:
        return Exception("Error response code: {}".format(response_champion.status_code))

    return len(response_champion.json())

def get_ranked_lol_info(account_id):

    ranked_lol_request = con.ranked_lol_request + "{}?api_key={}".format(account_id, con.api_key)

    resp_league = requests.get(ranked_lol_request)
    if resp_league.status_code == 400:
        return Exception("Error response code: {}".format(resp_league.status_code))
    
    league_queues = []
    
    resp_league = resp_league.json()
    for league in resp_league:
        queue_dict =  queue_dict = {
                        "queue_type": league["queueType"],
                        "tier": league["tier"],
                        "rank": league["rank"],
                        "wins": league["wins"],
                        "loses": league["losses"],
                        "pdl": league["leaguePoints"],
                        "win_rate": "",
                        "total_matches": int(league["wins"]) + int(league["losses"])
                }
        queue_dict["win_rate"] = str(int((int(league["wins"]) / int(queue_dict["total_matches"]))*100)) + "%"
        league_queues.append(queue_dict)

    return league_queues

def get_ranked_tft_info(account_id):

    ranked_tft_request = con.ranked_tft_request + "{}?api_key={}".format(account_id, con.api_key)

    resp_league = requests.get(ranked_tft_request)
    if resp_league.status_code == 400:
        return Exception("Error response code: {}".format(resp_league.status_code))
    
    league_queues = []
    
    resp_league = resp_league.json()
    for league in resp_league:
        queue_dict = {
                        "queue_type": league["queueType"],
                        "tier": league["tier"],
                        "rank": league["rank"],
                        "wins": league["wins"],
                        "loses": league["losses"],
                        "pdl": league["leaguePoints"],
                        "win_rate": "",
                        "total_matches": int(league["wins"]) + int(league["losses"])
                }
        queue_dict["win_rate"] = str(int((int(league["wins"]) / int(queue_dict["total_matches"]))*100)) + "%"
        league_queues.append(queue_dict)

    return league_queues[0]

