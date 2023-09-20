import requests
import os
from dotenv import load_dotenv
import json
from collections import defaultdict
import concurrent.futures

tokenURL = "https://www.warcraftlogs.com/oauth/token"
publicURL = "https://www.warcraftlogs.com/api/v2/client"

load_dotenv()

session = requests.Session()


def get_token(store=True):
    data = {"grant_type": "client_credentials"}
    auth = (os.getenv("userID"), os.getenv("userSecret"))
    response = session.post(tokenURL, data=data, auth=auth)

    if store and response.status_code == 200:
        store_token(response)
    return response


def store_token(response):
    try:
        with open(".credentials.json", mode="w+", encoding="utf-8") as f:
            json.dump(response.json(), f)
    except OSError as e:
        print(e)
        return None


def read_token():
    try:
        with open(".credentials.json", mode="r+", encoding="utf-8") as f:
            access_token = json.load(f)
        return access_token.get("access_token")
    except OSError as e:
        print(e)
        return None


def retrieve_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {read_token()}"}


ACTOR_QUERY = """
        query($code:String){
            reportData{
                report(code:$code){
                    masterData{
                          actors(type:"Player"){name id}
                
                        
                        }}}}"""

fights_query = """
        query($code:String){
            reportData{
                report(code:$code){
                fights{
                id
                encounterID
                kill
                name
                fightPercentage
                }}}}
        """

fight_query = """
        query($code:String, $fightIDs: [Int]){
            reportData{
                report(code:$code){
                fights(fightIDs:$fightIDs){
                friendlyPlayers
                id
                }}}}
        """
parse_query = """
        query($code:String,$fightIDs: [Int]){
            reportData{
                report(code:$code){
                rankings(fightIDs:$fightIDs)
                }
            }
        }"""
kazzara_bad_damage_taken_queries = [
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:402461)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:404789)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:400432)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:402420)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:406530)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:402207)
                    {
                        data
                    }
                }
            }
        }            
        """,
]

shadowflame_bad_damage_taken_queries = [
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:405704)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:408224)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:407611)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:404910)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:405458)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:403748)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:408190)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:403112)
                    {
                        data
                    }
                }
            }
        }            
        """,
]


zaqali_bad_damage_taken_query = [
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:408117)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:400450)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:401407)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:406976)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:410535)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: Casts, sourceID:$sourceID, abilityID:406535)
                    {
                        data
                    }
                }
            }
        }            
        """,
]

experiments_bad_damage_taken_query = [
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:405601)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:405599)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:408462)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:407733)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:406233)
                    {
                        data
                    }
                }
            }
        }            
        """,
]

rashok_bad_damage_taken_query = [
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:401510)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:403543)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:400777)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:406152 )
                    {
                        data
                    }
                }
            }
        }            
        """,
]

zskarn_bad_damage_taken_query = [
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:405462)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:417229)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:406206)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:406207)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:405439)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: Casts, sourceID:$sourceID, abilityID:405956)
                    {
                        data
                    }
                }
            }
        }            
        """,
]

magmorax_stats_query = [
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:405626)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:412078)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:413364)
                    {
                        data
                    }
                }
            }
        }            
        """,
]

get_stats_neltharion = [
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:409058)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:401883)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:409598)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:402831)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:402120)
                    {
                        data
                    }
                }
            }
        }            
        """,
]

get_damage_sarkareth = [
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:401621)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:402746)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:404499)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:403625)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:406989)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:403524)
                    {
                        data
                    }
                }
            }
        }            
        """,
    """
        query($code:String, $fightIDs: [Int], $sourceID: Int){
            reportData{
                report(code:$code){
                    events(fightIDs:$fightIDs, dataType: DamageTaken, sourceID:$sourceID, abilityID:405340)
                    {
                        data
                    }
                }
            }
        }            
        """,
]


def get_data(query: str, **kwargs):
    data = {"query": query, "variables": kwargs}
    with requests.Session() as session:
        session.headers = retrieve_headers()
        response = session.get(publicURL, json=data)
        return response.json()


def get_stats_sarkareth(input, fight, target):
    def query_damage(query):
        data = get_data(query, code=input, fightIDs=fight, sourceID=target)
        events = (
            data.get("data", {})
            .get("reportData", {})
            .get("report", {})
            .get("events", {})
            .get("data", [])
        )
        sum = 0
        soaks = 0
        for event in events:
            if event.get("abilityGameID") == 405340:
                soaks += 1
            elif event.get("overkill"):
                sum += 10
            else:
                sum += event.get("amount")
        return (sum, soaks)

    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        results = list(executor.map(query_damage, get_damage_sarkareth))
    total_sum = 0
    total_soaks = 0
    for sum, soaks in results:
        total_sum += sum
        total_soaks += soaks
    return (total_sum, total_soaks)


def get_damage_neltharion(input, fight, target):
    def query_damage(query):
        data = get_data(query, code=input, fightIDs=fight, sourceID=target)
        events = (
            data.get("data", {})
            .get("reportData", {})
            .get("report", {})
            .get("events", {})
            .get("data", [])
        )
        sum = 0
        for event in events:
            if event.get("overkill"):
                sum += 10
            sum += event.get("amount")
        return sum

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(query_damage, get_stats_neltharion))

    return sum(results)


def get_stats_zskarn(input, fight, target):
    def query_damage(query):
        data = get_data(query, code=input, fightIDs=fight, sourceID=target)
        events = (
            data.get("data", {})
            .get("reportData", {})
            .get("report", {})
            .get("events", {})
            .get("data", [])
        )
        sum = 0
        casts = 0
        for event in events:
            id = event.get("abilityGameID")
            if id == 405956:
                casts += 3
            else:
                if event.get("overkill"):
                    sum += event.get("overkill") + 1000000
                sum += event.get("amount")
        return (sum, casts)

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(query_damage, zskarn_bad_damage_taken_query))
    total_sum = 0
    total_casts = 0
    for sum, casts in results:
        total_sum += sum
        total_casts += casts
    return (total_sum, total_casts)


def get_stats_magmorax(input, fight, target):
    def query_damage(query):
        data = get_data(query, code=input, fightIDs=fight, sourceID=target)
        events = (
            data.get("data", {})
            .get("reportData", {})
            .get("report", {})
            .get("events", {})
            .get("data", [])
        )
        sum = 0
        casts = 0
        overkill = False
        for event in events:
            id = event.get("abilityGameID")
            if id == 413364:
                casts += 1
            else:
                if event.get("overkill"):
                    sum += 1000000
                sum += event.get("amount")
        return (sum, casts)

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(query_damage, magmorax_stats_query))
    total_sum = 0
    total_casts = 0
    for sum, casts in results:
        total_sum += sum
        total_casts += casts
    return (total_sum, total_casts)


def get_stats_zskarn(input, fight, target):
    def query_damage(query):
        data = get_data(query, code=input, fightIDs=fight, sourceID=target)
        events = (
            data.get("data", {})
            .get("reportData", {})
            .get("report", {})
            .get("events", {})
            .get("data", [])
        )
        sum = 0
        casts = 0
        for event in events:
            id = event.get("abilityGameID")
            if id == 405956:
                casts += 3
            else:
                if event.get("overkill"):
                    sum += event.get("overkill") + 1000000
                sum += event.get("amount")
        return (sum, casts)

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(query_damage, zskarn_bad_damage_taken_query))
    total_sum = 0
    total_casts = 0
    for sum, casts in results:
        total_sum += sum
        total_casts += casts
    return (total_sum, total_casts)


def get_soaks_done_rashok(input, fight, target):
    def query_damage(query):
        data = get_data(query, code=input, fightIDs=fight, sourceID=target)
        events = (
            data.get("data", {})
            .get("reportData", {})
            .get("report", {})
            .get("events", {})
            .get("data", [])
        )
        sum = 0
        soaks = 0
        for event in events:
            id = event.get("abilityGameID")
            if id == 406152:
                soaks += 2
            elif id == 400777:
                soaks += 1
            else:
                if event.get("overkill"):
                    sum += event.get("overkill") + 1000000
                sum += event.get("amount")
        return (sum, soaks)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(query_damage, rashok_bad_damage_taken_query))
    total_sum = 0
    total_soaks = 0
    for sum, soaks in results:
        total_sum += sum
        total_soaks += soaks
    print(total_sum, total_soaks, target)
    return (total_sum, total_soaks)


def get_damage_taken_experiments(input, fight, target):
    def query_damage(query):
        data = get_data(query, code=input, fightIDs=fight, sourceID=target)
        events = (
            data.get("data", {})
            .get("reportData", {})
            .get("report", {})
            .get("events", {})
            .get("data", [])
        )
        sum = 0
        for event in events:
            if event.get("overkill"):
                sum += event.get("overkill") + 1000000
            sum += event.get("amount")
        return sum

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(query_damage, experiments_bad_damage_taken_query))

    return sum(results)


def get_damage_taken_zaqali(input, fight, target):
    def query_damage(query):
        data = get_data(query, code=input, fightIDs=fight, sourceID=target)
        events = (
            data.get("data", {})
            .get("reportData", {})
            .get("report", {})
            .get("events", {})
            .get("data", [])
        )
        soaks = 0
        sum = 0
        for event in events:
            id = event.get("abilityGameID")
            if id == 406535:
                soaks += 3
            elif id == 410535:
                soaks += 1
            else:
                sum += event.get("amount")
                if event.get("overkill"):
                    sum += event.get("overkill") + 1000000
        return (sum, soaks)

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(query_damage, zaqali_bad_damage_taken_query))
    total_sum = 0
    total_soaks = 0
    for sum, soaks in results:
        total_sum += sum
        total_soaks += soaks
    return (total_sum, total_soaks)


def get_damage_taken_shadowflame(input, fight, target):
    def query_damage(query):
        data = get_data(query, code=input, fightIDs=fight, sourceID=target)
        events = (
            data.get("data", {})
            .get("reportData", {})
            .get("report", {})
            .get("events", {})
            .get("data", [])
        )
        sum = 0
        soaks = 0
        for event in events:
            id = event.get("abilityGameID")
            if id == 408190 or id == 403112:
                soaks += 2
            elif id == 403748 or id == 405458:
                soaks += 1
            else:
                sum += event.get("amount")
                if event.get("overkill"):
                    sum += event.get("overkill") + 1000000
        return (sum, soaks)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(query_damage, shadowflame_bad_damage_taken_queries))
    total_sum = 0
    total_soaks = 0
    for sum, soaks in results:
        total_sum += sum
        total_soaks += soaks
    return (total_sum, total_soaks)


def get_damage_taken_kazzara(input, fight, target):
    def query_damage(query):
        data = get_data(query, code=input, fightIDs=fight, sourceID=target)
        events = (
            data.get("data", {})
            .get("reportData", {})
            .get("report", {})
            .get("events", {})
            .get("data", [])
        )
        return sum(event.get("amount", 0) for event in events)

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(query_damage, kazzara_bad_damage_taken_queries))

    return sum(results)


def get_parses(input, fights):
    data = get_data(parse_query, code=input, fightIDs=fights)
    parse_dict = {}
    tank_parses = (
        data.get("data", {})
        .get("reportData", {})
        .get("report", {})
        .get("rankings", {})
        .get("data", [])[0]
        .get("roles", {})
        .get("tanks", {})
        .get("characters", [])
    )

    heal_parses = (
        data.get("data", {})
        .get("reportData", {})
        .get("report", {})
        .get("rankings", {})
        .get("data", [])[0]
        .get("roles", {})
        .get("healers", {})
        .get("characters", [])
    )

    dps_parses = (
        data.get("data", {})
        .get("reportData", {})
        .get("report", {})
        .get("rankings", {})
        .get("data", [])[0]
        .get("roles", {})
        .get("dps", {})
        .get("characters", [])
    )

    for parse in tank_parses:
        character_name = parse.get("name")
        character_parse = parse.get("rankPercent")
        if character_name and character_parse:
            parse_dict[character_name] = (character_parse, "tank")
    for parse in heal_parses:
        character_name = parse.get("name")
        character_parse = parse.get("rankPercent")
        if character_name and character_parse:
            parse_dict[character_name] = (character_parse, "healer")
    for parse in dps_parses:
        character_name = parse.get("name")
        character_parse = parse.get("rankPercent")
        if character_name and character_parse:
            parse_dict[character_name] = (character_parse, "dps")

    return parse_dict


def get_actors(input):
    data = get_data(ACTOR_QUERY, code=input)
    actor_dict = {}
    actors = (
        data.get("data", {})
        .get("reportData", {})
        .get("report", {})
        .get("masterData", {})
        .get("actors", [])
    )
    for actor in actors:
        actor_id = actor.get("id")
        actor_name = actor.get("name")
        if actor_id and actor_name:
            actor_dict[actor_id] = actor_name
    return actor_dict


def get_fights(input):
    data = get_data(fights_query, code=input)
    fight_dict = {}
    fights = (
        data.get("data", {}).get("reportData", {}).get("report", {}).get("fights", {})
    )
    for fight in fights:
        fight_id = fight.get("id")
        encounter_id = [
            fight.get("encounterID"),
            fight.get("name"),
            fight.get("kill"),
            fight.get("fightPercentage"),
        ]
        if encounter_id[0] != 0:
            fight_dict[fight_id] = encounter_id
    return fight_dict


def get_combatants(input, ids):
    data = get_data(fight_query, code=input, fightIDs=ids)
    combatants_dict = {}
    combatants = (
        data.get("data", {}).get("reportData", {}).get("report", {}).get("fights", {})
    )
    for combatant in combatants:
        fight_id = combatant.get("id")
        combatant_ids = combatant.get("friendlyPlayers")
        if combatant_ids and fight_id:
            combatants_dict[fight_id] = combatant_ids
    return combatants_dict


def main():
    response = get_token()
    print(response)

    token = read_token()
    print(token)
    log = "Q1BgprFZ8hmt76wV"
    get_damage_taken_kazzara(log, 6, 10)


if __name__ == "__main__":
    main()
