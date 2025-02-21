import http.client
import json
import pandas as pd
import argparse
from sqlalchemy import create_engine


dbname="ECSN_portugal_T10_DB"
user="postgres"
password="12345"
host='localhost'
port="5432"

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
try:
    with engine.connect() as conn:
        print("Connected to PostgreSQL successfully!")
except Exception as e:
    print("Error:", e)

class Squad:
    @staticmethod
    def make_request(endpoint, payload):
        headers = {
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
            'sec-ch-ua-mobile': '?0',
            'deviceId': 'f4e280779d295c69a92849669a4310da',
            'country': 'india',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'state': 'rajasthan',
            'Content-Type': 'application/json',
            'locale': 'en',
            'Sec-GPC': '1',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'host': 'apis.sportstiger.com'
        }

        conn = http.client.HTTPSConnection("apis.sportstiger.com")
        conn.request("POST", endpoint, json.dumps(payload), headers)
        res = conn.getresponse()

        if res.status == 200:
            response_data = json.loads(res.read().decode("utf-8"))
            conn.close()
            return response_data
        else:
            conn.close()
            return {"error": f"HTTP {res.status}"}

    @staticmethod
    def get_squad_id(l_id, season):
        squad_name_ids = []
        payload = {"spt_typ": 1, "l_id": str(l_id)}
        
        response = Squad.make_request("/Prod/get-series-teams", payload)
        if "error" in response:
            print(f"Error fetching squad IDs: {response['error']}")
            return []

        for team in response.get('result', []):
            squad_name_ids.append({
                "name": team.get('name', ""),
                "short_name": team.get("shortName", ""),
                "id": team.get("_id", ""),
                "format": team.get("format", ""),
                "season": season,
                "flag":team.get('flag', ""),
            })

        return squad_name_ids

    @staticmethod
    def teamid(l_id):
        endpoints = ["/Prod/completed-matches-by-league", "/Prod/live-matches-by-league", "/Prod/upcoming-matches-by-league"]
        responses = [Squad.make_request(endpoint, {"spt_typ": 1, "l_id": str(l_id)}) for endpoint in endpoints]

        unique_teams = {}

        for response in responses:
            if "error" in response:
                print(f"Error fetching teams: {response['error']}")
                continue

            for result in response.get("result", []):
                team_name = result.get("t1_sname", "null")
                team_id = result.get("t1_id", "null")
                opponent_team=result.get("t2_sname", "null")
                opponent_id=result.get("t2_id", "null")
                if team_name != "null" and team_id != "null":
                    unique_teams[team_name] = team_id
                if opponent_team != "null" and opponent_id != "null":
                    unique_teams[opponent_team] = opponent_id
        return unique_teams

    @staticmethod
    def get_squad(team_name, team_id, season,l_id,short_name,flag):
        payload = {"id": str(team_id)}
        squad_response = Squad.make_request("/Prod/get-series-team-squads", payload)

        if "error" in squad_response:
            print(f"Error fetching squad for {team_name}: {squad_response['error']}")
            return []
        
        team_data=[]
        team_ids = Squad.teamid(l_id)
        
        team_data.append({
                
                "TeamID": team_ids.get(short_name, "null"),
                "TeamName": short_name,
                "TeamFullName": team_name,
                "TeamLogoUrl":flag,
                "status":'ACTIVE'
            })

        squad_data = []
        for player in squad_response.get("result", []):
            player_info = Squad.make_request("/Prod/player-info", {"p_id": int(player.get("p_id", "")), "spt_typ": 1})
            player_details = player_info.get("result", {})

            team_ids = Squad.teamid(l_id)
            
            squad_data.append({
                "Season": season,
                "PlayerID": player.get("p_id", ""),
                "PlayerName": player.get("p_name", ""),
                "TeamName": short_name,
                "TeamID": team_ids.get(short_name, "null"),
                "Info": "null",
                "Debut": season,
                "ImageURL": player.get("image", ""),
                "FullName": player.get("p_name", ""),
                "PlayingRole": player.get("role", ""),
                "BattingStyle": player_details.get("batting_style", ""),
                "BowlingStyle": player_details.get("bowling_style", ""),
                "DateOfBirth": player_details.get("birth_date", "")
            })
            
        return squad_data,team_data

def main():
    parser = argparse.ArgumentParser(description="Fetch and save squad data from Sportstiger API.")
    parser.add_argument("--id", type=str,default=10899, help="ID of the cricket series")
    parser.add_argument("--year", type=str,default=2025, help="Season of the tournament")
    args = parser.parse_args()

    squads = []
    teams_data = []
    teams = Squad.get_squad_id(args.id, args.year)
    if not teams:
        print("No teams found. Exiting.")
        return

    for team in teams:
        squad_data, team_data = Squad.get_squad(team["name"], team["id"], team["season"], args.id, team["short_name"], team["flag"])
        squads.extend(squad_data)  
        teams_data.extend(team_data)

    if squads:
        df_squad = pd.DataFrame(squads)
        df_squad.fillna('null')
        
        df_squad.to_sql('team_squad', engine, if_exists='replace', index=False)
        print("Data pushed successfully!")
        # df_squad.to_csv(f"{args.id}_squad.csv", index=False)
        # print(f"Squad data saved to {args.id}_squad.csv")
        
        
    if teams_data:
        df_teams = pd.DataFrame(teams_data)
        df_teams.fillna('null', inplace=True)

        df_teams.to_sql('team', engine, if_exists='replace', index=False)
        print("Team data pushed successfully!")

    else:
        print("No squad data found.")

if __name__ == "__main__":
    main()
