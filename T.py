import http.client
import json
import csv
import pandas as pd
import os
import datetime
import re
import argparse

def make_request(endpoint, payload, headers):
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


def derive_stats(l_id,m_id):
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

    payload_info = {"spt_typ": 1, "l_id": l_id, "m_id": m_id}
    payload_overview = {"spt_typ": 1, "l_id": l_id, "m_id": m_id}
    payload_scoreboard = {"m_id": m_id}

    match_info = make_request("/Prod/match-info", payload_info, headers)

    match_overview = make_request("/Prod/match-overview", payload_overview, headers)

    match_scoreboard = make_request("/Prod/match-scoreboard", payload_scoreboard, headers)


    player_names = []
    player_id = []
    role = []
    serial_numbers = []
    runs = []
    balls_faced = []
    fours = []
    sixes = []
    how_out = []
    bowled_by = []
    strike_rates = []
    images = []
    is_first = []
    seasons = []
    has_batted = []
    team = []
    team_id = []
    bowling_team_id = []
    ovr = []
    team_runs = []
    wkt = []
    opponent_team = []
    opponent_team_id = []
    opponent_overs = []
    opponent_runs = []
    opponent_wickets = []

    match_status = []
    Format = []
    leauge = []
    venue = []
    date = []
    position = []

    GameType=[]
    Minutes=[]

    DerivedPosition=[]
    GuessPosition=[]

    dt_object = datetime.datetime.fromtimestamp(match_info.get("result", {}).get('strt_time_ts', "null"))
    formatted_time = dt_object.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    game_date = formatted_time.split('T')[0]
    year = dt_object.strftime("%Y")


    for j in range(2):
        innings = match_scoreboard.get("result", [{}])[0].get("innings", [])
        innings_score = innings[j]
        overview = match_overview.get("result", {}).get("matchInfo", {})
        venue_info = match_info.get("result", {}).get("venue", 'null')
        
        m_status=None
        if overview.get("status", "null")=='completed':
            m_status='FINISHED'
        else:
            m_status='Null'
            

    

        
            
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
            seasons.append(year)
            match_status.append(m_status)
            #match_id.append(overview.get("m_id", "null"))
            #leauge_id.append(overview.get("l_id", "null"))
            Format.append(overview.get("format", "null"))
            leauge.append(overview.get("l_name", "null"))
            venue.append(venue_info)
            date.append(game_date)
            position.append(post)
            GameType.append("null")
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
            seasons.append(year)
            match_status.append(m_status)
            #match_id.append(overview.get("m_id", "null"))
            #leauge_id.append(overview.get("l_id", "null"))
            Format.append(overview.get("format", "null"))
            leauge.append(overview.get("l_name", "null"))
            venue.append(venue_info)
            date.append(game_date)
            position.append(post)
            GameType.append("null")
            Minutes.append("null")
            DerivedPosition.append("null")
            GuessPosition.append("null")

    df_bat = pd.DataFrame({
        'Season': seasons,
        'Date': date,
        'MatchStatus': match_status,
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
        'Venue': venue,
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
        'Format': Format,
        'League': leauge,
        'GameType':GameType, 
        'Minutes':Minutes, 
        'DerivedPosition':DerivedPosition,
        'GuessPosition':DerivedPosition,
    })

    df_bat['MOM'] = 0
    df_bat.loc[df_bat['PlayerName'] == overview.get("man_of_the_match", {}).get("player_name", "null"), 'MOM'] = 1
    #breakpoint()
    
    df_bat['Winner']=None
    w_id = overview.get("winnerTeamId", "null")
    t1_id=overview.get("t1_id", "null")
    t1_name=overview.get("t1_sname", "null")
    t2_id=overview.get("t2_id", "null")
    t2_name=overview.get("t2_sname", "null")

    if int(w_id)==int(t1_id):
        df_bat['Winner']=t1_name
    elif int(w_id)==int(t2_id):
        df_bat['Winner']=t2_name
    else:
        print("team id and name dont match")

        

            
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

    dots=[]
    SixGiven=[]
    FourGiven=[]
    GameID=[]

    for j in range(2):
        innings = match_scoreboard.get("result", [{}])[0].get("innings", [])
        
        bowling_data = innings[j].get("bowlers", [])
        for player in bowling_data:
            pid.append(player.get("pid", "null")),
            bowler_name.append(player.get("name","null"))
            overs.append(player.get("overs", 'null')),
            maidens.append(player.get("maidens", 'null')),
            runs_given.append(player.get("runs", 'null')),
            wickets.append(player.get("wickets", 'null')),
            economy.append(player.get("econ", 'null')),
            wides.append(player.get("wides", 'null')),
            nb.append(player.get("noballs", 'null'))
            dots.append(0)  
            SixGiven.append(0)  
            FourGiven.append(0)
            
            

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
        'SixesGiven': SixGiven 
        
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
                name = text.split(' to ')[0].strip() if ' to ' in text else 'null'

                runs = item.get('run', 0)

                for idx, player in df_bowl.iterrows():
                    if player['bowler_name'].strip().lower() == name.strip().lower():                    
                        
                        if runs == 0:
                            df_bowl.at[idx, 'DotBalls'] += 1  
                        elif runs == 4:
                            df_bowl.at[idx, 'FoursGiven'] += 1 
                        elif runs == 6:
                            df_bowl.at[idx, 'SixesGiven'] += 1
                        else:
                            continue
                        
                        
    #print(df_bowl)

    # filename = 'bowl_stats.csv'
    # if os.path.exists(filename):
    #     os.remove(filename)
    # df_bowl.to_csv(filename, index=False)


    df_bat['original_order'] = df_bat.index

    df_merged = pd.merge(df_bat, df_bowl, on="PlayerID", how="outer")

    df_merged = df_merged.sort_values(by='original_order').drop(columns='original_order')
    df_merged.drop(columns='bowler_name', inplace=True)



    # df_merged = pd.DataFrame(data)

    df_merged['Catch'] = 0
    df_merged['Bowled'] = 0
    df_merged['CaughtBowled'] = 0
    df_merged['Lbw'] = 0
    df_merged['Stumped'] = 0
    df_merged['DirectRunout'] = 0
    df_merged['IndirectRunout'] = 0

    dt_object = datetime.datetime.fromtimestamp(match_info.get("result", {}).get('strt_time_ts', "null"))
    time_str = dt_object.strftime("%Y%m%d")
    t1=match_info.get("result", {}).get('t1_sname', "null")
    t2=match_info.get("result", {}).get('t2_sname', "null")
    df_merged['GameID'] = time_str + t1 + t2


    for index, status in enumerate(df_merged['Status']):
        status_parts = status.split()
        
        if status.startswith('c & b'):
            if len(status_parts) >= 3:
                bowler_last_name = status_parts[4] 
                bowler_initial = status_parts[3][0] 
                
                
                #matches = df_merged[df_merged['PlayerName'].str.contains(f'{bowler_last_name}$', regex=True)]
                matches = df_merged[df_merged['PlayerName'].apply(lambda x: x.split()[-1] == bowler_last_name)]

                for idx in matches.index:
                    
                    player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]

                    if player_first_name[0] == bowler_initial:
                        df_merged.at[idx, 'Catch'] += 1
                        df_merged.at[idx, 'CaughtBowled'] += 1
                        
        elif status.startswith('c'):
            if len(status_parts) >= 6: 
                fielder_initial = status_parts[1][0]  
                fielder_last_name = status_parts[2] 

                fielder_matches = df_merged[df_merged['PlayerName'].apply(lambda x: x.split()[-1] == fielder_last_name)]
                for idx in fielder_matches.index:
                    player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                    if player_first_name[0] == fielder_initial:  
                        df_merged.at[idx, 'Catch'] += 1

                        
        elif status.startswith('b'):
            if len(status_parts) >= 1: 
                bowler_last_name = status_parts[2] 
                bowler_initial = status_parts[1][0] 
                
                matches = df_merged[df_merged['PlayerName'].apply(lambda x: x.split()[-1] == bowler_last_name)]
                for idx in matches.index:
                    player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                    if player_first_name[0] == bowler_initial: 
                        df_merged.at[idx, 'Bowled'] += 1


        elif status.startswith('lbw'):
            if len(status_parts) >= 2:
                bowler_last_name = status_parts[3]
                bowler_initial = status_parts[2]
                
                bowler_matches = df_merged[df_merged['PlayerName'].apply(lambda x: x.split()[-1] == bowler_last_name)]
                for idx in bowler_matches.index:
                    player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                    if player_first_name[0] == bowler_initial:
                        df_merged.at[idx, 'Lbw'] += 1
                    

        elif status.startswith('st'):
            if len(status_parts) >= 5:  
                fielder_last_name = status_parts[2]
                fielder_initial = status_parts[1][0]
                
                fielder_matches = df_merged[df_merged['PlayerName'].apply(lambda x: x.split()[-1] == fielder_last_name)]
                for idx in fielder_matches.index:
                    player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                    if player_first_name[0] == fielder_initial:  
                        df_merged.at[idx, 'Stumped'] += 1
                


        elif 'runout' in status:
            runout_names = status[status.index('(')+1:status.index(')')].split('/')
            if len(runout_names) == 1:
                last_name = runout_names[0].split()[-1]
                matches = df_merged[df_merged['PlayerName'].str.contains(f'{last_name}$', regex=True)]
                for idx in matches.index:
                    player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                    if player_first_name[0] == runout_names[0][0]:  
                        df_merged.at[idx, 'DirectRunout'] += 1
            else:
                for name in runout_names:
                    last_name = name.split()[-1]
                    matches = df_merged[df_merged['PlayerName'].str.contains(f'{last_name}$', regex=True)]
                    for idx in matches.index:
                        player_first_name = df_merged.at[idx, 'PlayerName'].split()[0]
                        if player_first_name[0] == name[0]:  
                            df_merged.at[idx, 'IndirectRunout'] += 1
        
        else:
            continue
    
    return df_merged




mid_list=[]
def get_m_id_from_l_id(l_id,header):
    l_payload={"spt_typ":1,"l_id":l_id}
    leauge=make_request("/Prod/completed-matches-by-league", l_payload,header)
    for mats in leauge.get("result",[]):
        m_id=mats.get("m_id","null")
        mid_list.append(m_id)
    return mid_list

parser = argparse.ArgumentParser()

parser.add_argument('--l_id', type=str, default="10871", help="League ID")
parser.add_argument('--m_id', type=str, help="Match ID (if known)")
args = parser.parse_args()

if not args.m_id:
    m_id = get_m_id_from_l_id(args.l_id,headers)
    
    for m_id in mid_list:
        df_m=derive_stats(args.l_id,m_id)
        filename = f'merged_stats_{args.l_id}.csv'

        order=['GameID','Season','GameType','Date','MatchStatus','Team','TeamID','Opponent','OpponentID','Winner','TeamScore','TeamWKLoss','TeamOversPlayed',
            'OpponentScore','OpponentWKLoss','OpponentOversPlayed','Venue','MOM','IsFirstInning','BattingOrder','HasBatted','PlayerID','PlayerName','Status','RunsScored',
            'BallsPlayed','Minutes','FoursHit','SixesHit','StrikeRate','Over','Maiden','RunsGiven','WKTaken','Econ','DotBalls','FoursGiven','SixesGiven','Wides','NoBall',
            'CaughtBowled','Lbw','Catch','Stumped','DirectRunout','Bowled','IndirectRunout','Position','DerivedPosition','GuessPosition','FullPosition','PlayingOrder','Format','League'
        ]


        remaining_columns = [col for col in df_m.columns if col not in order]
        full_order = order + remaining_columns

        df_final = df_m[full_order]
        df_final=df_final.astype('str')          # All columns are converted to string to put Null in empty spaces
        df_final.replace('nan', 'null', inplace=True)
        df_final.fillna('null', inplace=True)

        
        if not os.path.exists(filename) or os.stat(filename).st_size == 0:
            df_final.to_csv(filename, mode='a', header=order, index=False)
        else:
            df_final.to_csv(filename, mode='a', header=False, index=False)

else:
    df_m=derive_stats(args.l_id,args.m_id)
    filename = f'merged_stats_{args.l_id}_{args.m_id}.csv'

    order=['GameID','Season','GameType','Date','MatchStatus','Team','TeamID','Opponent','OpponentID','Winner','TeamScore','TeamWKLoss','TeamOversPlayed',
        'OpponentScore','OpponentWKLoss','OpponentOversPlayed','Venue','MOM','IsFirstInning','BattingOrder','HasBatted','PlayerID','PlayerName','Status','RunsScored',
        'BallsPlayed','Minutes','FoursHit','SixesHit','StrikeRate','Over','Maiden','RunsGiven','WKTaken','Econ','DotBalls','FoursGiven','SixesGiven','Wides','NoBall',
        'CaughtBowled','Lbw','Catch','Stumped','DirectRunout','Bowled','IndirectRunout','Position','DerivedPosition','GuessPosition','FullPosition','PlayingOrder','Format','League'
    ]


    remaining_columns = [col for col in df_m.columns if col not in order]
    full_order = order + remaining_columns

    df_final = df_m[full_order]
    df_final=df_final.astype('str')          # All columns are converted to string to put Null in empty spaces
    df_final.replace('nan', 'null', inplace=True)
    df_final.fillna('null', inplace=True)

    
    df_final.to_csv(filename, mode='a', header=order, index=False)



