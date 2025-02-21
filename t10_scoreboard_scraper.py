import http.client
import json
import csv
import pandas as pd
import os
import datetime
import re
import argparse
from sqlalchemy import create_engine
import pytz
import re
from difflib import SequenceMatcher

dbname="t10_master_db"
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

class info_extract:
    
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

    
    game_id_counter = {}
    @staticmethod
    def derive_stats(l_id,m_id):
 
        payload_info = {"spt_typ": 1, "l_id": l_id, "m_id": m_id}
        payload_overview = {"spt_typ": 1, "l_id": l_id, "m_id": m_id}
        payload_scoreboard = {"m_id": m_id}

        match_info = info_extract.make_request("/Prod/match-info", payload_info)

        match_overview = info_extract.make_request("/Prod/match-overview", payload_overview)

        match_scoreboard = info_extract.make_request("/Prod/match-scoreboard", payload_scoreboard)
        
        if not match_info.get("status") or not match_info.get("result"):
            return

        if not match_overview.get("status") or not match_overview.get("result"):
            return

        if not match_scoreboard.get("status") or not match_scoreboard.get("result"):
            return
            
        # innings = match_scoreboard.get("result", [{}])[0].get("innings", [])
        # innings_score = innings[j]
        # overview = match_overview.get("result", {}).get("matchInfo", {})
        # venue_info = match_info.get("result", {}).get("venue", 'null')

        player_names = []
        player_id = []
        role = []
        serial_numbers = []
        runs = []
        balls_faced = []
        fours = []
        sixes = []
        how_out = []
        strike_rates = []
        is_first = []
        has_batted = []
        team = []
        team_id = []
        ovr = []
        team_runs = []
        wkt = []
        opponent_team = []
        opponent_team_id = []
        opponent_overs = []
        opponent_runs = []
        opponent_wickets = []
        position = []

        GameType=[]
        Minutes=[]

        DerivedPosition=[]
        GuessPosition=[]

        
        try:
            # Safely extract the timestamp
            timestamp = match_info.get("result", {}).get('strt_time_ts', None)
            
            # Check if the timestamp is not None and is valid
            if timestamp:
                dt_object = datetime.datetime.fromtimestamp(timestamp)
                formatted_time = dt_object.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                
                try:
                    game_date = formatted_time.split('T')[0]
                except Exception as e:
                    print("1")
                    print(e)
                    print(l_id,m_id)
                year = dt_object.strftime("%Y")
            else:
                print("Warning: 'strt_time_ts' is missing or invalid. Skipping this step.")
                formatted_time = game_date = year = "null"

        except Exception as e:
            print(f"Error while processing timestamp: {e}")
            formatted_time = game_date = year = "null"


        for j in range(len(match_scoreboard.get("result", [{}])[0].get("innings", []))):
        
            try:
                innings = match_scoreboard.get("result", [{}])[0].get("innings", [])
                innings_score = innings[j] if len(innings) > j else {}
            except Exception as e:
                print(f"Exception encountered while fetching innings: {e}")
                innings_score = 'null'

            try:
                overview = match_overview.get("result", {}).get("matchInfo", {})
            except Exception as e:
                print(f"Exception encountered while fetching overview: {e}")
                overview = 'null'

            try:
                venue_info = match_info.get("result", {}).get("venue", 'null')
            except Exception as e:
                print(f"Exception encountered while fetching venue info: {e}")
                venue_info = 'null'

            
            m_status=None
            if overview.get("status", "null")=='completed':
                m_status='FINISHED'
            else:
                m_status='Null'
                

            
            try:
                first_var = 1 if j == 0 else 0

                serial_number = 1
                batting_data = innings[j].get("batsmen", [])
                for player in batting_data:
                    
                    role_mapping = {
                        "batter": "BAT",
                        "bowler": "BOWL",
                        "batting all-rounder": "AR",
                        "bowling all-rounder": "AR",
                        "wk-batter": "WK"
                    }

                    post = role_mapping.get(player.get("role", "null"), "null")

                    is_first.append(first_var)
                    serial_numbers.append(serial_number)
                    player_names.append(re.sub(r"\s*\(.*?\)", "", player.get("name", "null")).strip())
                    player_id.append(player.get("pid", "null"))
                    role.append(player.get("role", "null"))
                    runs.append(player.get("runs", 'null')) 
                    balls_faced.append(player.get("balls_faced", 'null')) 
                    strike_rates.append(player.get("strike_rate", 'null')) 
                    fours.append(player.get("fours", 'null'))  
                    sixes.append(player.get("sixes", 'null'))
                    how_out.append(player.get("how_out", 'null'))  
                    #bowled_by.append(player.get("bowled_by", 'null')) 
                    has_batted.append(1)
                    #images.append(player.get("image", 'null')) 
                    serial_number += 1
                    team.append(innings_score.get("t_sname", 'null'))
                    ovr.append(innings_score.get("ovr", 'null'))
                    team_runs.append(innings_score.get("runs", 'null'))
                    wkt.append(innings_score.get("wkt", 'null'))
                    team_id.append(innings_score.get("t_id", 'null'))
                    opponent_team.append(innings[1 - j].get("t_sname", 'null'))
                    opponent_team_id.append(innings[1 - j].get("t_id", 'null'))
                    opponent_overs.append(innings[1 - j].get("ovr", 'null'))
                    opponent_runs.append(innings[1 - j].get("runs", 'null'))
                    opponent_wickets.append(innings[1 - j].get("wkt", 'null'))
                    #match_id.append(overview.get("m_id", "null"))
                    #leauge_id.append(overview.get("l_id", "null"))
                    position.append(post if post else 'null')
                    Minutes.append("null")
                    DerivedPosition.append("null")
                    GuessPosition.append("null")

                yet_to_bat_data = innings[j].get("did_not_bat", [])
                for player in yet_to_bat_data:
                    
                    post = role_mapping.get(player.get("role", "null"), "null")
                    
                    is_first.append(first_var)
                    serial_numbers.append(serial_number)
                    player_names.append(re.sub(r"\s*\(.*?\)", "", player.get("name", "null")).strip())
                    player_id.append(player.get("pid", "null"))
                    role.append(player.get("role", "null"))
                    runs.append('null') 
                    balls_faced.append('null') 
                    strike_rates.append('null') 
                    fours.append('null') 
                    sixes.append('null') 
                    how_out.append('null')
                    #bowled_by.append('null')
                    has_batted.append(0)
                    #images.append('null')
                    serial_number += 1
                    team.append(innings_score.get("t_sname", 'null'))
                    ovr.append(innings_score.get("ovr", 'null'))
                    team_runs.append(innings_score.get("runs", 'null'))
                    wkt.append(innings_score.get("wkt", 'null'))
                    team_id.append(innings_score.get("t_id", 'null'))
                    opponent_team.append(innings[1 - j].get("t_sname", 'null'))
                    opponent_team_id.append(innings[1 - j].get("t_id", 'null'))
                    opponent_overs.append(innings[1 - j].get("ovr", 'null'))
                    opponent_runs.append(innings[1 - j].get("runs", 'null'))
                    opponent_wickets.append(innings[1 - j].get("wkt", 'null'))
                    #match_id.append(overview.get("m_id", "null"))
                    #leauge_id.append(overview.get("l_id", "null"))
                    position.append(post if post else "null")
                    Minutes.append("null")
                    DerivedPosition.append("null")
                    GuessPosition.append("null")
            except Exception as e:
                print(e)
                return
                
                
                
        df_bat = pd.DataFrame({
            'Team': team,
            'TeamID': team_id,
            'Opponent': opponent_team,
            'OpponentID': opponent_team_id,
            'TeamScore': team_runs,
            'TeamWKLoss': wkt,
            'TeamOversPlayed': ovr,
            'OpponentScore': opponent_runs,
            'OpponentWKLoss': opponent_wickets,
            'OpponentOversPlayed': opponent_overs,
            'IsFirstInning': is_first,
            'BattingOrder': serial_numbers,
            'HasBatted': has_batted,
            'PlayerID': player_id,
            'PlayerName': player_names,
            'Status': how_out,
            'RunsScored': runs,
            'BallsPlayed': balls_faced,
            'FoursHit': fours,
            'SixesHit': sixes,
            'StrikeRate': strike_rates,
            'Position': position,
            'FullPosition': role,
            'PlayingOrder': serial_numbers,
            'Minutes':Minutes, 
            'DerivedPosition':DerivedPosition,
            'GuessPosition':DerivedPosition,
        })
                    
        # filename = 'bat_stats.csv'
        # if os.path.exists(filename):
        #     os.remove(filename)
        # df_bat.to_csv(filename, index=False)
        
            
        
        
        
        pid=[]
        bowler_name=[]
        overs=[]
        maidens=[]
        runs_given=[]
        wickets=[]
        economy=[]
        wides=[]
        nb=[]
        bowler_team_id=[]
        dots=[]
        SixGiven=[]
        FourGiven=[]
        

        team = []
        team_id = []
        ovr = []
        team_runs = []
        wkt = []
        opponent_team = []
        opponent_team_id = []
        opponent_overs = []
        opponent_runs = []
        opponent_wickets = []

        for j in range(2):
            innings = match_scoreboard.get("result", [{}])[0].get("innings", [])
            try:
                bowling_data = innings[j].get("bowlers", [])
                for player in bowling_data:
                    pid.append(player.get("pid", "null")),
                    bowler_name.append(re.sub(r"\s*\(.*?\)", "", player.get("name", "null")).strip())
                    overs.append(player.get("overs", 'null')),
                    maidens.append(player.get("maidens", 'null')),
                    runs_given.append(player.get("runs", 'null')),
                    wickets.append(player.get("wickets", 'null')),
                    economy.append(player.get("econ", 'null')),
                    wides.append(player.get("wides", 'null')),
                    nb.append(player.get("noballs", 'null')),
                    bowler_team_id.append(player.get("bowling_team_id","null")),
                    dots.append(0),
                    SixGiven.append(0),  
                    FourGiven.append(0),
                    
                    team.append(innings[1 - j].get("t_sname", 'null'))
                    team_id.append(innings[1 - j].get("t_id", 'null'))
                    ovr.append(innings[1 - j].get("ovr", 'null'))
                    team_runs.append(innings[1 - j].get("runs", 'null'))
                    wkt.append(innings[1 - j].get("wkt", 'null'))
                    opponent_team.append(innings[j].get("t_sname", 'null'))
                    opponent_team_id.append(innings[j].get("t_id", 'null'))
                    opponent_overs.append(innings[j].get("ovr", 'null'))
                    opponent_runs.append(innings[j].get("runs", 'null'))
                    opponent_wickets.append(innings[j].get("wkt", 'null'))
            except Exception as e:
                print(e)
                return
                
                
                

        df_bowl = pd.DataFrame({
            'PlayerID': pid,
            'bowler_name': bowler_name,
            'Over': overs,
            'Maiden': maidens,
            'RunsGiven': runs_given,
            'WKTaken': wickets,
            'Econ': economy,
            'Wides': wides,
            'NoBall': nb,
            'DotBalls': dots, 
            'FoursGiven': FourGiven, 
            'SixesGiven': SixGiven,
            
            'te_am': team,
            'team_ID': team_id,
            'oppo_nent': opponent_team,
            'opponent_ID': opponent_team_id,
            'team_Score': team_runs,
            'team_WKLoss': wkt,
            'team_OversPlayed': ovr,
            'opponent_Score': opponent_runs,
            'opponent_WKLoss': opponent_wickets,
            'opponent_OversPlayed': opponent_overs,
        })

        processed_refids = set()  # Global set to store processed refids

        for i in range(1,3):
            for j in range(2,11,2):
                
                conn = http.client.HTTPSConnection("apis.sportstiger.com")
                payload = json.dumps({
                "m_id": "42922",
                "i_no": i,
                "over": j,
                "refid": 0
                })
                headers = {
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
                'sec-ch-ua-mobile': '?0',
                'deviceId': 'a062e11ceeb47762a3df67c23e1a9fc7',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                'locale': 'en',
                'Sec-GPC': '1',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'host': 'apis.sportstiger.com'
                }
                conn.request("POST", "/Prod/live-updates-cricket", payload, headers)
                res = conn.getresponse()
                given = json.loads(res.read().decode("utf-8"))
                data=given.get('result',{}).get('data',{})
                for item in data:
                    refid = item.get('refid')
                    if refid in processed_refids or item.get('type') == 'end of over':
                        continue
                    
                    processed_refids.add(refid)

                    text = item.get('text', '')
                    try:
                        name = text.split(' to ')[0].strip() if ' to ' in text else 'null'
                    except Exception as e:
                        print("2")
                        print(e)
                        print("name",l_id,m_id)
                    runs = item.get('run', 0)

                    for idx, player in df_bowl.iterrows():
                        try:
                            if player['bowler_name'].strip().lower() == name.strip().lower():
                                
                                if runs == 0:
                                    df_bowl.at[idx, 'DotBalls'] += 1  
                                elif runs == 4:
                                    df_bowl.at[idx, 'FoursGiven'] += 1 
                                elif runs == 6:
                                    df_bowl.at[idx, 'SixesGiven'] += 1
                                else:
                                    continue
                        except:
                            print(player['bowler_name'],"strip_1")
                            
        
        

        
                    
        #print(df_bowl)

        # filename = 'bowl_stats.csv'
        # if os.path.exists(filename):
        #     os.remove(filename)
        # df_bowl.to_csv(filename, index=False)


        # df_bat['original_order'] = df_bat.index

        # df_merged = pd.merge(df_bat, df_bowl, on="PlayerID", how="outer")

        # df_merged = df_merged.sort_values(by='original_order').drop(columns='original_order')
        # df_merged.drop(columns='bowler_name', inplace=True)
        
        df_bat['original_order'] = df_bat.index
        df_merged = pd.merge(df_bat, df_bowl, on="PlayerID", how="outer")
        mask = df_merged['PlayerName'].isna()
        var = 1 if j == 1 else 0
        df_merged.loc[mask, 'PlayerName'] = df_merged.loc[mask, 'bowler_name']
        df_merged.loc[mask, 'IsFirstInning'] = df_merged.loc[mask, 'IsFirstInning'].fillna(var)
        df_merged.loc[mask, 'Team'] = df_merged.loc[mask, 'Team'].fillna(df_merged['te_am'])
        df_merged.loc[mask, 'TeamID'] = df_merged.loc[mask, 'TeamID'].fillna(df_merged['team_ID'])
        df_merged.loc[mask, 'Opponent'] = df_merged.loc[mask, 'Opponent'].fillna(df_merged['oppo_nent'])
        df_merged.loc[mask, 'OpponentID'] = df_merged.loc[mask, 'OpponentID'].fillna(df_merged['opponent_ID'])
        df_merged.loc[mask, 'TeamScore'] = df_merged.loc[mask, 'TeamScore'].fillna(df_merged['team_Score'])
        df_merged.loc[mask, 'TeamWKLoss'] = df_merged.loc[mask, 'TeamWKLoss'].fillna(df_merged['team_WKLoss'])
        df_merged.loc[mask, 'TeamOversPlayed'] = df_merged.loc[mask, 'TeamOversPlayed'].fillna(df_merged['team_OversPlayed'])
        df_merged.loc[mask, 'OpponentScore'] = df_merged.loc[mask, 'OpponentScore'].fillna(df_merged['opponent_Score'])
        df_merged.loc[mask, 'OpponentWKLoss'] = df_merged.loc[mask, 'OpponentWKLoss'].fillna(df_merged['opponent_WKLoss'])
        df_merged.loc[mask, 'OpponentOversPlayed'] = df_merged.loc[mask, 'OpponentOversPlayed'].fillna(df_merged['opponent_OversPlayed'])
        df_merged.loc[mask, 'HasBatted'] = df_merged.loc[mask, 'HasBatted'].fillna(0)
        
        df_merged = df_merged.sort_values(by='original_order').drop(columns=[
            'original_order', 'bowler_name', 'te_am', 'team_ID', 'oppo_nent',
            'opponent_ID', 'team_Score', 'team_WKLoss', 'team_OversPlayed',
            'opponent_Score', 'opponent_WKLoss', 'opponent_OversPlayed'
        ])


        
        df_merged['Winner']=None
        w_id = overview.get("winnerTeamId", "null")
        res_str= overview.get("result_str", "null")
        t1_id=overview.get("t1_id", "null")
        t1_sname=overview.get("t1_sname", "null")
        t1_name=overview.get("t1_name", "null")
        t2_id=overview.get("t2_id", "null")
        t2_sname=overview.get("t2_sname", "null")
        t2_name=overview.get("t2_name", "null")
        
        def get_match_ratio(a, b):
            return SequenceMatcher(None, a, b).ratio()
        
        

        if w_id is not None and w_id != 0:
            if int(w_id)==int(t1_id):
                df_merged['Winner']=t1_sname
            elif int(w_id)==int(t2_id):
                df_merged['Winner']=t2_sname
            else:
                print("team id and name dont match")
                print(l_id,m_id)
        else:
            team_name = re.match(r'^(.*?)\s+won', res_str)
            if team_name:
                team_name = team_name.group(1)
                best_match = max([(t1_name, get_match_ratio(team_name, t1_name)), 
                  (t2_name, get_match_ratio(team_name, t2_name))], key=lambda x: x[1])
                best_team = best_match[0]

                if best_team == t1_name:
                    df_merged['Winner']=t1_sname
                elif best_team == t2_name:
                    df_merged['Winner']=t2_sname
                else:
                    print("No strong match found")
            else:
                team_name = ""
                print("no winner team name provided")
            
            
        
        
        df_merged['MOM'] = 0 
        
        try:
            
            mom_player = overview.get("man_of_the_match", {}).get("player_name", "null")
            if 'PlayerName' in df_merged.columns:
                df_merged.loc[df_merged['PlayerName'] == mom_player, 'MOM'] = 1
            else:
                print("Warning: 'PlayerName' column is missing in df_merged.")

        except KeyError as e:
            print(f"KeyError: Missing key in 'overview' dictionary - {e}")

        except AttributeError as e:
            print(f"AttributeError: Possible NoneType issue - {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")
            
            
        type_value = None
        m_name = match_info.get("result", {}).get('m_name')
        
        try:
            match_name=m_name.strip()
            split_name = match_name.split(',')
        except:
            print(match_name)
            print("20")
        try:
            if len(split_name) > 1 and split_name[1].strip().startswith('Match'):
                type_value = "DRR"
            else:
                type_value = "POFF"
        except:
            print("strip_2")
        
        df_merged['GameType'] = type_value
            
        df_merged['Season']=year
        df_merged['Date']=game_date if game_date else 'null'
        df_merged['MatchStatus']=m_status
        df_merged['Venue']=venue_info if venue_info else 'null'
        df_merged['Format']=overview.get("format", "null")
        df_merged['League']=overview.get("l_name", "null")
    

        # df_merged = pd.DataFrame(data)
        
        df_merged['Catch'] = 0
        df_merged['Bowled'] = 0
        df_merged['CaughtBowled'] = 0
        df_merged['Lbw'] = 0
        df_merged['Stumped'] = 0
        df_merged['DirectRunout'] = 0
        df_merged['IndirectRunout'] = 0
        
        df_merged['PlayerName'] = df_merged['PlayerName'].fillna('')

        ist = pytz.timezone("Asia/Kolkata") 
        utc = pytz.utc

        dt_object = datetime.datetime.fromtimestamp(match_info.get("result", {}).get('strt_time_ts', "null"))
        time_str = dt_object.strftime("%Y%m%d")
        dt_ist = datetime.datetime.fromtimestamp(timestamp, ist)
    
        dt_utc = dt_ist.astimezone(utc)
        
        time_str = dt_utc.strftime("%Y%m%d")
        t1=match_info.get("result", {}).get('t1_sname', "null")
        t2=match_info.get("result", {}).get('t2_sname', "null")
        
        match_id = time_str + t1 + t2
        if match_id:
            if match_id in info_extract.game_id_counter:
                info_extract.game_id_counter[match_id] += 1         
            else:
                info_extract.game_id_counter[match_id] = 1
                
        gameid = f"{match_id}_{info_extract.game_id_counter[match_id]}" 
        df_merged['GameID'] = gameid
        
        
        #print(df_merged['PlayerName'].apply(type))
        #print(df_merged['PlayerName'].apply(type).value_counts())

        df_merged["Status"] = df_merged["Status"].fillna("Null")
        df_merged.to_csv("temp.csv",mode='a')
        for index, status in enumerate(df_merged['Status']):
            # try:
            #     status.strip()
            # except:
            #     print(status,"strip_5")
                
            if status is not None and not status=="Null" and not status=="Not out":
                try:
                    status_strip=str(status)
                    status_parts = status_strip.split()
                except Exception as e:
                        print("3")
                        print(e)
                        print(type(status))
                        print(status_parts,l_id,m_id)
                        breakpoint()
                        #print(index)
                        continue
                val = [
                    (5, 'V'), (4, 'IV'),
                    (3, 'III'), (2, 'II'), (1, 'I')
                ]

                match = re.search(r'\d+', status)
                if match:
                    num = int(match.group())
                    roman_num = ''

                    for i, r in val:
                        while num >= i:
                            roman_num += r
                            num -= i

                    # Fix: Ensure `status` is updated instead of an undefined variable `name`
                    status = re.sub(r'\d+', roman_num, status)

                
                if status.startswith('c & b'):
                    if len(status_parts) == 5:
                        bowler_last_name = status_parts[4] 
                        bowler_initial = status_parts[3][0] 
                        
                        
                        #matches = df_merged[df_merged['PlayerName'].str.contains(f'{bowler_last_name}$', regex=True)]
                        try:
                            matches = df_merged[df_merged['PlayerName'].apply(
                                    lambda x: x.split()[-1] == bowler_last_name if isinstance(x, str) and len(x.split()) > 0 else False
                                )]
                        except Exception as e:
                            print("4")
                            print(e)
                        
                        for idx in matches.index:
                            try:
                                player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                            except Exception as e:
                                print("5")
                                print(e)
                            if player_first_name[0] == bowler_initial:
                                df_merged.at[idx, 'Catch'] += 1
                                df_merged.at[idx, 'CaughtBowled'] += 1
                    else:
                        bowler_last_name = status_parts[-1]  
                        try:
                            bowler_initial = status_parts[3][0]  
                        except IndexError:
                            print("No initial in 'c & b'")
                            bowler_initial = None

                        try:
                            matches = df_merged[df_merged['PlayerName'].apply(
                                lambda x: x.split()[-1] == bowler_last_name if isinstance(x, str) and len(x.split()) > 0 else False
                            )]
                        except Exception as e:
                            print("Error filtering bowler matches:", e)

                        for idx in matches.index:
                            if bowler_initial:  # Only apply initial matching if it exists
                                try:
                                    player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                                except Exception as e:
                                    print("Error extracting first name:", e)
                                    continue  # Skip iteration on error
                                
                                if player_first_name and player_first_name[0] == bowler_initial:
                                    df_merged.at[idx, 'Catch'] += 1
                                    df_merged.at[idx, 'CaughtBowled'] += 1
                            else:
                                # If no initial is found, update all rows matching last name
                                df_merged.at[idx, 'Catch'] += 1
                                df_merged.at[idx, 'CaughtBowled'] += 1
                                
                elif status.startswith('c'):
                    if len(status_parts) == 6: 
                        fielder_initial = status_parts[1][0]  
                        fielder_last_name = status_parts[2] 

                                
                        try:
                            fielder_matches = df_merged[df_merged['PlayerName'].apply(
                                            lambda x: x.split()[-1] == fielder_last_name if isinstance(x, str) and len(x.split()) > 0 else False
                                        )]
                        except Exception as e:
                            print("6")
                            print(e)
                                
                        for idx in fielder_matches.index:
                            try:
                                player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                            except Exception as e:
                                print("7")
                                print(e)
                            if player_first_name[0] == fielder_initial:  
                                df_merged.at[idx, 'Catch'] += 1
                    else:
                        player_name = re.search(r'c(.*?)b', status)
                        
                        if player_name:  # Ensure match is found
                            fielder_last_name = player_name.group(1).split()[-1]
                            try:
                                fielder_initial = status_parts[1][0]
                            except IndexError:
                                print("No initial in 'b'")
                                fielder_initial = None
                        
                            try:
                                fielder_matches = df_merged[df_merged['PlayerName'].apply(
                                    lambda x: x.split()[-1] == fielder_last_name if isinstance(x, str) and len(x.split()) > 0 else False
                                )]
                            except Exception as e:
                                print("Error filtering fielder matches:", e)

                            for idx in fielder_matches.index:
                                if fielder_initial:  # Only apply initial matching if it exists
                                    try:
                                        player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                                    except Exception as e:
                                        print("Error extracting first name:", e)
                                        continue  # Skip iteration on error
                                    
                                    if player_first_name and player_first_name[0] == fielder_initial:
                                        df_merged.at[idx, 'Catch'] += 1
                                else:
                                    # If no initial is found, update all rows matching last name
                                    df_merged.at[idx, 'Catch'] += 1
                    
                elif status.startswith('b'):
                    if len(status_parts) == 3: 
                        bowler_last_name = status_parts[2] 
                        bowler_initial = status_parts[1][0] 
                        
                        try:
                            matches = df_merged[df_merged['PlayerName'].apply(
                                    lambda x: x.split()[-1] == bowler_last_name if isinstance(x, str) and len(x.split()) > 0 else False
                                )]
                        except Exception as e:
                            print("8")
                            print(e)
                        for idx in matches.index:
                            try:
                                player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                            except Exception as e:
                                print("9")
                                print(e)
                            if player_first_name[0] == bowler_initial: 
                                df_merged.at[idx, 'Bowled'] += 1
                    else:
                        bowler_last_name = status_parts[-1]  # Last word as last name
                        
                        # Try extracting initial safely
                        try:
                            bowler_initial = status_parts[1][0]
                        except IndexError:
                            print("No initial in 'b'")
                            bowler_initial = None  # Set initial to None if unavailable
                    
                        try:
                            matches = df_merged[df_merged['PlayerName'].apply(
                                lambda x: x.split()[-1] == bowler_last_name if isinstance(x, str) and len(x.split()) > 0 else False
                            )]
                        except Exception as e:
                            print("Error filtering matches:", e)

                        for idx in matches.index:
                            if bowler_initial:  # Only apply initial matching if it exists
                                try:
                                    player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                                except Exception as e:
                                    print("Error extracting first name:", e)
                                    continue  # Skip iteration on error
                                
                                if player_first_name and player_first_name[0] == bowler_initial:
                                    df_merged.at[idx, 'Bowled'] += 1
                            else:
                                # If no initial is found, update all rows matching last name
                                df_merged.at[idx, 'Bowled'] += 1
                        

                elif status.startswith('lbw'):
                    if len(status_parts) == 4:
                        bowler_last_name = status_parts[3]
                        bowler_initial = status_parts[2]
                        
                        try:
                            bowler_matches = df_merged[df_merged['PlayerName'].apply(
                                        lambda x: x.split()[-1] == bowler_last_name if isinstance(x, str) and len(x.split()) > 0 else False
                                    )]
                        except Exception as e:
                                print("10")
                                print(e)
                    
                        for idx in bowler_matches.index:
                            try:
                                player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                            except Exception as e:
                                print("11")
                                print(e)
                            if player_first_name[0] == bowler_initial:
                                df_merged.at[idx, 'Lbw'] += 1
                        
                    else:
                        bowler_last_name = status_parts[-1]  # Last word as last name

                        # Try extracting the initial safely
                        try:
                            bowler_initial = status_parts[2][0]  # First character of 3rd word
                        except IndexError:
                            print("No initial in 'lbw'")
                            bowler_initial = None  # Set to None if unavailable

                        try:
                            bowler_matches = df_merged[df_merged['PlayerName'].apply(
                                lambda x: x.split()[-1] == bowler_last_name if isinstance(x, str) and len(x.split()) > 0 else False
                            )]
                        except Exception as e:
                            print("Error filtering bowler matches:", e)

                        for idx in bowler_matches.index:
                            if bowler_initial:  # Only apply initial matching if it exists
                                try:
                                    player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                                except Exception as e:
                                    print("Error extracting first name:", e)
                                    continue  # Skip iteration on error
                                
                                if player_first_name and player_first_name[0] == bowler_initial:
                                    df_merged.at[idx, 'Lbw'] += 1
                            else:
                                # If no initial is found, update all rows matching last name
                                df_merged.at[idx, 'Lbw'] += 1
                                

                elif status.startswith('st'):
                    if len(status_parts) == 6:  
                        fielder_last_name = status_parts[2]
                        fielder_initial = status_parts[1][0]
                        
                        try:
                            fielder_matches = df_merged[df_merged['PlayerName'].apply(
                                            lambda x: x.split()[-1] == fielder_last_name if isinstance(x, str) and len(x.split()) > 0 else False
                                        )]
                        except Exception as e:
                                print("12")
                                print(e)
                        
                        for idx in fielder_matches.index:
                            try:
                                player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                            except Exception as e:
                                print("13")
                                print(e)
                            if player_first_name[0] == fielder_initial:  
                                df_merged.at[idx, 'Stumped'] += 1
                    else:
                        fielder_last_name = status_parts[-1]  # Last name is the 3rd word
                        try:
                            fielder_initial = status_parts[1][0]  # Initial is the first character of the 2nd word
                        except IndexError:
                            print("No initial in 'st'")
                            fielder_initial = None  # Set to None if initial is missing

                        try:
                            fielder_matches = df_merged[df_merged['PlayerName'].apply(
                                lambda x: x.split()[-1] == fielder_last_name if isinstance(x, str) and len(x.split()) > 0 else False
                            )]
                        except Exception as e:
                            print("Error filtering fielder matches:", e)

                        for idx in fielder_matches.index:
                            if fielder_initial:  # Only apply initial matching if it exists
                                try:
                                    player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                                except Exception as e:
                                    print("Error extracting first name:", e)
                                    continue  # Skip iteration on error
                                
                                if player_first_name and player_first_name[0] == fielder_initial:
                                    df_merged.at[idx, 'Stumped'] += 1
                            else:
                                # If no initial is found, update all rows matching last name
                                df_merged.at[idx, 'Stumped'] += 1
                            


                elif 'runout' in status:
                    try:
                        start_idx = status.find('(')
                        end_idx = status.find(')')

                        if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                            extracted_text = status[start_idx + 1:end_idx].strip()  # Get text inside parentheses
                            runout_names = [name.strip() for name in extracted_text.split('/') if name.strip()]
                        else:
                            runout_names = []
                                                    
                        if len(runout_names) == 1:
                            try:
                                last_name = runout_names[0].split()[-1]
                            except Exception as e:
                                    print("15")
                                    print(e)
                            try:
                                matches = df_merged[df_merged['PlayerName'].apply(
                                                lambda x: x.split()[-1] == last_name if isinstance(x, str) and len(x.split()) > 0 else False
                                            )]
                            except Exception as e:
                                    print("16")
                                    print(e)
                            for idx in matches.index:
                                try:
                                    player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                                except Exception as e:
                                    print("17")
                                    print(e)
                                if player_first_name[0] == runout_names[0][0]:  
                                    df_merged.at[idx, 'DirectRunout'] += 1
                        else:
                            for name in runout_names:
                                try:
                                    last_name = name.split()[-1]
                                except Exception as e:
                                    print("18")
                                    print(e)
                                try:
                                    matches = df_merged[df_merged['PlayerName'].apply(
                                                lambda x: x.split()[-1] == last_name if isinstance(x, str) and len(x.split()) > 0 else False
                                            )]
                                except Exception as e:
                                    print("19")
                                    print(e)
                                for idx in matches.index:
                                    try:
                                        player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                                    except Exception as e:
                                        print("20")
                                        print(e)
                                    if player_first_name[0] == name[0]:  
                                        df_merged.at[idx, 'IndirectRunout'] += 1
                    except Exception as e:
                        print("runout error")
                        print(e)
                else:
                    continue
        
        return df_merged

    
    def get_m_id_from_l_id(self, l_id):
        self.mid_list = []
        l_payload = {"spt_typ": 1, "l_id": l_id}
        league = info_extract.make_request("/Prod/completed-matches-by-league", l_payload)
        for mats in league.get("result", []):
            m_id = mats.get("m_id", "null")
            self.mid_list.append(m_id)
        return self.mid_list

    @staticmethod
    def process_single_match(l_id, m_id):
        """Process a single match and save results to a CSV."""
        df_m = info_extract.derive_stats(l_id, m_id)
        # filename = f'stats_.csv' if is_multiple else f'merged_stats_{l_id}_{m_id}.csv'
        filename = 'temp_stats.csv'
        
        order = [
            'GameID', 'Season', 'GameType', 'Date', 'MatchStatus', 'Team', 'TeamID', 'Opponent', 'OpponentID', 'Winner', 
            'TeamScore', 'TeamWKLoss', 'TeamOversPlayed', 'OpponentScore', 'OpponentWKLoss', 'OpponentOversPlayed', 
            'Venue', 'MOM', 'IsFirstInning', 'BattingOrder', 'HasBatted', 'PlayerID', 'PlayerName', 'Status', 
            'RunsScored', 'BallsPlayed', 'Minutes', 'FoursHit', 'SixesHit', 'StrikeRate', 'Over', 'Maiden', 'RunsGiven', 
            'WKTaken', 'Econ', 'DotBalls', 'FoursGiven', 'SixesGiven', 'Wides', 'NoBall', 'CaughtBowled', 'Lbw', 'Catch', 
            'Stumped', 'DirectRunout', 'Bowled', 'IndirectRunout', 'Position', 'DerivedPosition', 'GuessPosition', 
            'FullPosition', 'PlayingOrder', 'Format', 'League'
        ]

        # remaining_columns = [col for col in df_m.columns if col not in order]
        # full_order = order + remaining_columns
        
        if df_m is not None:
            remaining_columns = [col for col in df_m.columns if col not in order]
            full_order = order + remaining_columns

        else:
            return

        df_final = df_m[full_order]
        df_final = df_final.astype('str')  # Convert all columns to strings
        df_final.replace('nan', 'null', inplace=True)
        df_final.fillna('null', inplace=True)
        df_final.to_sql('scoreboard', engine, if_exists='append', index=False)
        #print("Data pushed successfully!")

        # if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        #     df_final.to_csv(filename, mode='a', header=order, index=False)
        # else:
        #     df_final.to_csv(filename, mode='a', header=False, index=False)

    def process_league_matches(self, l_id):
        """Process all matches for a given league ID."""
        m_ids = self.get_m_id_from_l_id(l_id)
        for m_id in m_ids:
            self.process_single_match(l_id, m_id)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--l_id', type=str, default="10899", help="League ID")
    parser.add_argument('--m_id', type=str, help="Match ID (if known)")
    args = parser.parse_args()

    processor = info_extract()

    if not args.m_id:
        processor.process_league_matches(args.l_id)
    else:
        processor.process_single_match(args.l_id, args.m_id)

if __name__ == "__main__":
    main()

