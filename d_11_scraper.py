from libImports import *
import argparse as args
from sqlalchemy import create_engine
import pandas as pd

def getSchedule():
        engine = create_engine("postgresql+psycopg2://postgres:12345@localhost/ECSN_T10_DB")

        df = pd.read_sql("SELECT * FROM schedule;", engine)
        return df
    
schedule_df = getSchedule()

class slate():
    

    toss_info = [
        "GameID",
        "Date",
        "Team",
        "TeamID",
        "Opponent",
        "OpponentID",
        "TossWinner",
        "TossDecision",
    ]

    player_data_cols_final = [
        "PlayerID",
        "Season",
        "SlateID",
        "Date",
        "SlateGameID",
        "GameID",
        "Team",
        "TeamID",
        "Position",
        "OperatorPlayerID",
        "OperatorPlayerName",
        "OperatorBetsMade",
        "OperatorMatchInfo",
        "OperatorPlayerFantasyPoints",
        "OperatorPlayerCredits",
        "UpdatedDate",
        "UpdatedTime",
        "InjuryStatus",
        "InjuryInfo",
        "D11_MatchID",
        "Dream11PlayerID",
        "PlayingOrder"
    ]

    slate_df_cols_final = [
        "SlateID",
        "Date",
        "Season",
        "Operator",
        "OperatorName",
        "OperatorDay",
        "OperatorTime",
        "SalaryCap",
        "NumberOfGames",
        "GameStatus",
    ]

    game_slate_df_cols_final = [
        "SlateGameID",
        "Season",
        "Date",
        "SlateID",
        "GameID",
        "Updated",
        "GameStatus",
    ]
    
    def getGameID(team1, team2, d11_date):
        """Returns Sportsseam's game id for the two team names provided

        Args:
            team1 (str): ESPN Team abbreviation
            team2 (str): ESPN Team abbreviation

        Returns:
            str: Returns SS game id from schedule.
        """
        print(f"{team1} vs {team2}")
        date_info = schedule_df[
            ((schedule_df.Team == team1) & (schedule_df.Opponent == team2))
            | ((schedule_df.Team == team2) & (schedule_df.Opponent == team1))
        ]
        #print(f"*****{date_info}*******")
        possible_match_date = date_info.Date.values
        # min_hours_between = 240
        min_hours_between = 72
        most_likely_match_date = None

        for date in possible_match_date:
           # print(date)
            match_date = datetime.strptime(date, "%Y-%m-%d").date()
            match_time = date_info[date_info.Date == date].Time.values[0]
            match_time = datetime.strptime(match_time, "%H:%M:%S").time()
            match_datetime = datetime.combine(match_date, match_time)

            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "UTC")), "%Y-%m-%dT%H:%M:%S"
            )

            today_datetime = datetime.strptime(today, "%Y-%m-%dT%H:%M:%S")
            hour_diff = (match_datetime - today_datetime).total_seconds() // 3600
            print(hour_diff)
            if (hour_diff >= 0) and (hour_diff < min_hours_between):
                min_hours_between = hour_diff
                # most_likely_match_date = date
                most_likely_match_date = d11_date
            # most_likely_match_date = possible_match_date[0]
            elif (hour_diff < 0):
                # most_likely_match_date = date
                most_likely_match_date = d11_date
            # most_likely_match_date = possible_match_date[0]
        # print(date_info,most_likely_match_date)
        try:
            match_id = date_info[date_info.Date ==
                            most_likely_match_date].GameID.values[0]
        except:
            for day in date_info.Date.values:
                if day == d11_date:
                    match_id = date_info[date_info.Date ==
                            d11_date].GameID.values[0]
        # print(match_id)
        return match_id


    game_id_counter = {}

    def getGameID_fromdt(team1, team2, game_dt):
        """Returns Sportsseam's game id for the two team names provided

        Args:
            team1 (str): 1st Team abbreviation
            team2 (str): 2nd Team abbreviation
            game_dt (str): Game datetime obtained from dream11 API JSON

        Returns:
            str: Returns unique SS game id from schedule.
        """
        date_info = schedule_df[
            ((schedule_df.Team == team1) & (schedule_df.Opponent == team2))
            | ((schedule_df.Team == team2) & (schedule_df.Opponent == team1))
        ]
        possible_match_date = date_info.Date.values
        most_likely_match_date = None

        game_dt = datetime.strptime(game_dt, "%Y-%m-%dT%H:%M:%S.000Z")
        game_dt_in_str = datetime.strftime(game_dt, "%Y-%m-%d %H:%M:%S")

        match_id = None

        for date in possible_match_date:
            match_date = datetime.strptime(date, "%Y-%m-%d").date()
            match_time = date_info[date_info.Date == date].Time.values[0]
            match_time = datetime.strptime(match_time, "%H:%M:%S").time()
            match_datetime = datetime.combine(match_date, match_time)
            match_datetime_in_str = datetime.strftime(match_datetime, "%Y-%m-%d %H:%M:%S")

            if match_datetime_in_str == game_dt_in_str:
                most_likely_match_date = date
                match_id = date_info[date_info.Date == most_likely_match_date].GameID.values[0]
                break
            else:
                game_date = datetime.strftime(game_dt, "%Y-%m-%d")
                if date == game_date:
                    match_id = slate.getGameID(team1=team1, team2=team2, d11_date=game_date)

        if match_id:
            # Ensure uniqueness by adding _1, _2, etc.
            if match_id in slate.game_id_counter:
                slate.game_id_counter[match_id] += 1
                match_id = f"{match_id}_{slate.game_id_counter[match_id]}"
            else:
                slate.game_id_counter[match_id] = 1
            

        return match_id
    
    
    player_df = pd.DataFrame(columns=player_data_cols_final)
    toss_df = pd.DataFrame(columns=toss_info)
    slate_df = pd.DataFrame(columns=slate_df_cols_final)
    game_slate_df = pd.DataFrame(columns=game_slate_df_cols_final)

    def get_api_response(request_endpoint, payload):
        conn = http.client.HTTPSConnection("www.dream11.com")
        headers = {"Content-Type": "application/json"}

        conn.request("POST", f"{request_endpoint}", payload, headers)
        res = conn.getresponse()

        data = res.read()
        data_str = data.decode("utf-8")
        data_json = json.loads(data_str)
        conn.close()
        return data_json

    def get_create_team_api(d11_series_id, d11_match_id):   ### Gives playing and squad of match
        payload = json.dumps(
            {
                "query": "query ShmeCreateTeamQuery( $site: String! $tourId: Int! $teamId: Int = -1 $matchId: Int!) { site(slug: $site) { name showTeamCombination { count siteKey } teamPreviewArtwork { src } teamCriteria { totalCredits maxPlayerPerSquad totalPlayerCount } roles { id artwork { src } color name pointMultiplier shortName } playerTypes { id name minPerTeam maxPerTeam shortName artwork { src } } tour(id: $tourId) { match(id: $matchId) { id guru tossResult squads { flag { src } flagWithName { src } id jerseyColor name shortName fullName } startTime status players(teamId: $teamId) { artwork { src } squad { id name jerseyColor shortName fullName } credits id name points type { id maxPerTeam minPerTeam name shortName } lineupStatus { status text color } isSelected role { id artwork { src } color name pointMultiplier shortName } lineupOrder battingOrder statistics { selectionRate role { id selectionRate } } } tour { id } } } showSelPercent }}",
                "variables": {
                    "tourId": d11_series_id,
                    "matchId": d11_match_id,
                    "teamId": None,
                    "site": "cricket",
                },
            }
        )
        res_d11 = slate.get_api_response(
            request_endpoint="/graphql/query/pwa/shme-create-team-query", payload=payload
        )
        return res_d11


    def match_squad_ST(st_series_id,st_match_id):
        conn = http.client.HTTPSConnection("apis.sportstiger.com")
        payload = json.dumps({
        "spt_typ": 1,
        "l_id": str(st_series_id),
        "m_id": str(st_match_id)
        })
        headers = {
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
        'sec-ch-ua-mobile': '?0',
        'deviceId': 'cdfd94ef40cd6cd47f38db299af79a75',
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
        conn.request("POST", "/Prod/match-squad", payload, headers)
        res = conn.getresponse()
        data_json = json.loads(res.read().decode("utf-8"))
        return data_json


    def match_and_rank_names(d11_teams, st_teams):
        """
        Matches and ranks names based on similarity.
        
        Args:
            team1 (list): Two names from Team 1.
            team2 (list): Two names from Team 2.
        
        Returns:
            dict: A dictionary with matched pairs and their similarity scores.
        """
        name_pairs = list(permutations(d11_teams + st_teams, 2))
        similarity_scores = {
            pair: SequenceMatcher(None, pair[0], pair[1]).ratio() for pair in name_pairs
        }
        
        sorted_pairs = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
        best_pair = sorted_pairs[0][0]
        remaining_names = set(d11_teams + st_teams) - set(best_pair)
        second_pair = tuple(remaining_names)
        
        return {
            "p1": {"names": list(best_pair), "Similarity": similarity_scores[best_pair]},
            "p2": {"names": list(second_pair), "Similarity": similarity_scores[second_pair]}
        }
        
    def generate_d11_team_jsons(d11_lid,d11_mid):
        team_jsons = {}  # Dictionary to store team-wise players
        res = slate.get_create_team_api(d11_lid, d11_mid)
        team_players = res.get('data', {}).get('site', {}).get('tour', {}).get('match', {}).get('players', [])
        status=res.get('data', {}).get('site', {}).get('tour', {}).get('match', {}).get("status","")
        date=res.get('data', {}).get('site', {}).get('tour', {}).get('match', {}).get("startTime","")
        toss=res.get('data', {}).get('site', {}).get('tour', {}).get('match', {}).get("tossResult","")
        parts=toss.split(' ')
        toss_team=parts[0]
        toss_dec=parts[3]
        
        for player in team_players:
            t_id = player.get('squad', {}).get('id','')  # Team ID
            t_name = player.get('squad', {}).get('fullName','').strip()   # Team name
            p_id = player.get('id','')  # Player ID
            name = player.get('name','').strip()   # Player name
            lineupOrder = player.get('lineupOrder','')
            battingOrder = player.get('battingOrder','')
            Credits = player.get('credits','')
            Points = player.get('points','')
            info = player.get('lineupStatus',{}).get('status','').strip()
            bets = player.get('statistics',{}).get('selectionRate','')
            position = player.get('type',{}).get('name','').strip()

            if not t_id or not t_name or not p_id or not name:  # Skip missing data
                continue
            
            # Ensure the team entry exists
            if t_name not in team_jsons:
                team_jsons[t_name] = {
                    "toss_team":toss_team,
                    "toss_dec":toss_dec,
                    "team_id": t_id,
                    "status":status,
                    "date":date,
                    "players": []
                }

            # Append player data
            team_jsons[t_name]["players"].append({"id": p_id, "name": name,"L_order":lineupOrder,"B_order":battingOrder,
                                                "Credits":Credits,"points":Points,"info":info,"bets":bets,"position":position})

        return team_jsons

    
    
    
    def generate_st_team_jsons(st_lid,st_mid):
        team_jsons = {}  # Dictionary to store team-wise players
        res = slate.match_squad_ST(st_lid, st_mid)
        team_players = res.get('result', {})

        t1_name = team_players.get('t1_name', '').strip() 
        t1_sname = team_players.get('t1_sname', '').strip() 
        t2_name = team_players.get('t2_name', '').strip() 
        t2_sname = team_players.get('t2_sname', '').strip() 
        t1_squad = team_players.get('t1_squad', [])  # Ensure it's a list
        t2_squad = team_players.get('t2_squad', [])  # Ensure it's a list

        if t1_name:
            team_jsons[t1_name] = {"sname": t1_sname, "players": []}  
        if t2_name:
            team_jsons[t2_name] = {"sname": t2_sname, "players": []} 

        for player in t1_squad:
            name = player.get('name', '').strip() 
            p_id = player.get('p_id', '').strip() 

            if not name or not p_id:
                continue 

            team_jsons[t1_name]["players"].append({"id": p_id, "name": name})

        for player in t2_squad:
            name = player.get('name', '').strip() 
            p_id = player.get('p_id', '').strip() 

            if not name or not p_id:
                continue 

            team_jsons[t2_name]["players"].append({"id": p_id, "name": name})

        return team_jsons



    def match_and_rank_players(team1_json, team2_json, pairs, game_id):
        
        t1 = pairs.get('p1').get('names') 
        t2 = pairs.get('p2').get('names')
        d11_date = team1_json.get(t1[0], {}).get('date', '')
        # formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y%m%d")
        gameid=slate.getGameID_fromdt(team2_json.get(t1[1], {}).get('sname',''),team2_json.get(t2[1], {}).get('sname',''),d11_date)
        # print(game_id)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        todays_date = now.strftime("%Y-%m-%d")
        
        matched_players = []
        slate_info=[]
        game_slate=[]
        

        for team_pair in [t1, t2]:
            d11_team_name, st_team_name = team_pair
            
            
            # Extract player data
            d_11_player_list = team1_json.get(d11_team_name, {}).get('players', [])
            st_player_list = team2_json.get(st_team_name, {}).get('players', [])
            d11_team_id=team1_json.get(d11_team_name, {}).get('team_id', '')
            match_info=team1_json.get(d11_team_name, {}).get('status', '')
            credits=team1_json.get(d11_team_name, {}).get('credits', '')
            tsname = team2_json.get(st_team_name, {}).get('sname','')

            
            if not d_11_player_list or not st_player_list:
                print(f"Skipping pair {d11_team_name} vs {st_team_name} due to missing data.")
                continue  # Skip if any team has no players
            
            d11_player = {player['name']: player['id'] for player in d_11_player_list}
            st_player = {player['name']: player['id'] for player in st_player_list}
            
            name_pairs = [
                (d11_team_name, d11_name, d11_id, st_team_name, st_name, st_id, SequenceMatcher(None, d11_name, st_name).ratio())
                for d11_name, d11_id in d11_player.items() for st_name, st_id in st_player.items()
            ]
            
            sorted_pairs = sorted(name_pairs, key=lambda x: x[6], reverse=True)
            
            
            
            used_names = set()
            i=0
            for d11_team_name, d11_name, d11_id, st_team_name, st_name, st_id, score in sorted_pairs:
                if d11_name not in used_names and st_name not in used_names:
                    credits=team1_json.get(d11_team_name, {}).get('players', '')[i].get('Credits')
                    B_order=team1_json.get(d11_team_name, {}).get('players', '')[i].get('B_order')
                    points=team1_json.get(d11_team_name, {}).get('players', '')[i].get('points')
                    info=team1_json.get(d11_team_name, {}).get('players', '')[i].get('info')
                    bets = team1_json.get(d11_team_name, {}).get('players', '')[i].get('bets')
                    bets = f"{bets}%" if bets is not None else "N/A%"
                    position=team1_json.get(d11_team_name, {}).get('players', '')[i].get('position')
                    date = team1_json.get(d11_team_name, {}).get('date', '')
                    mdate=datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
                    formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y%m%d")
                    

                    slate_id = (
                        "".join(formatted_date.split("-")) + "11"       ## TODO- add count
                    )
                    
                    
                    if position=="ALL":
                        position="AR"
                    
                    if info=="PLAYING":
                        info="Announced"
                    elif info=="NOT_PLAYING":
                        info='Unannounced'
                    else:
                        info='Unannounced'
                        
                    parts = d11_name.split()

                    if len(parts) > 1:
                        short_name = f"{parts[0][0]} {parts[-1]}"
                    else:
                        short_name = parts[0]                        
                    
                    matched_players.append({
                        "PlayerID": st_id,
                        "Season": "season",
                        "SlateID": slate_id, 
                        "Date": mdate,
                        "SlateGameID": gameid+'_11',
                        "GameID": gameid,
                        "Team": tsname,
                        "TeamID": d11_team_id, 
                        "Position": position,   
                        "OperatorPlayerID": st_id+'11',
                        "OperatorPlayerName": short_name,
                        "OperatorBetsMade": bets,
                        "OperatorMatchInfo": info,
                        "OperatorPlayerFantasyPoints": points,
                        "OperatorPlayerCredits": credits,
                        "UpdatedDate": todays_date,
                        "UpdatedTime": current_time,
                        "InjuryStatus": None,
                        "InjuryInfo": "Null",
                        "D11_MatchID": game_id,
                        "Dream11PlayerID": d11_id,
                        "PlayingOrder": B_order,
                    })
                    used_names.add(d11_name)
                    used_names.add(st_name)
                    i+=1
                    
                            
                df_player = pd.concat([slate.player_df, pd.DataFrame(matched_players)], ignore_index=True)
                df_player.to_csv('player_slate.csv',index=False)

        slate_info.append({
            "SlateID": slate_id,
            "Date": mdate,
            "Season": "season",
            "Operator": "Dream 11",
            "OperatorName": "DailyFantasy",
            "OperatorDay": todays_date,
            "OperatorTime": current_time,
            "SalaryCap": "100",
            "NumberOfGames": "1",
            "GameStatus" : info,
        })
        
        game_slate.append({
            "SlateGameID": gameid+'_11',
            "Season": "season",
            "Date": mdate,
            "SlateID": slate_id,
            "GameID": gameid,
            "Updated":todays_date,
            "GameStatus" : "Announced"
        })
        
        toss=[]
        
        df_slate = pd.concat([slate.slate_df, pd.DataFrame(slate_info)], ignore_index=True)
        df_slate.to_csv('slate.csv',index=False)
        
        df_game_slate = pd.concat([slate.game_slate_df, pd.DataFrame(game_slate)], ignore_index=True)
        df_game_slate.to_csv('game_slate.csv',index=False)
        
        d11_date = team1_json.get(t1[0], {}).get('date', '')
        # formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y%m%d")
        
        toss_team=team1_json.get(t1[0], {}).get('toss_team')
        toss_dec=team1_json.get(t1[0], {}).get('toss_dec')
        
        d11_team1_id=team1_json.get(t2[0], {}).get('team_id', '')
        d11_team2_id=team1_json.get(t1[0], {}).get('team_id', '')
        t1sname = team2_json.get(t2[1], {}).get('sname','')
        t2sname = team2_json.get(t1[1], {}).get('sname','')
        date = team1_json.get(t1[0], {}).get('date', '')
        mdate=datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y%m%d")
        
        name=slate.match_and_rank_names([toss_team,""],[t1sname,t2sname])
        n1 = name.get('p1').get('names')[1]
                    
        toss.append({
            "GameID": gameid,
            "Date": mdate,
            "Team": t1sname,
            "TeamID": d11_team1_id, 
            "Opponent": t2sname,
            "OpponentID": d11_team2_id,
            "TossWinner":n1,
            "TossDecision":toss_dec,
        })
        df_toss= pd.concat([slate.toss_df, pd.DataFrame(toss)], ignore_index=True)
        df_toss.to_csv('toss.csv',index=False)
        
        

    # def connectIPLRds():
    #     database = SERIES_DB_MAPPER[args.ss_series_name]
    #     connection = psycopg2.connect(
    #         user=user, password=password, host=host, port=port, database=database
    #     )
    #     return connection
        
    # def get_game_players(game_id):
    #     """Return list of 22 players who have played in provided game if

    #     Args:
    #         game_id (str): Game ID whose player list is required

    #     Raises:
    #         Exception: Raised when player list is not 22

    #     Returns:
    #         list: List of 22 player ids
    #     """
    #     query = f"""
    #             select "PlayerID" from scorecard where "GameID" = '{game_id}';
    #             """
    #     con = slate.connectIPLRds()
    #     cur = con.cursor()
    #     cur.execute(query)
    #     db_result = cur.fetchall()
    #     con.close()
    #     print(db_result)
    #     if not db_result:
    #         print("Latest Game Not Found")
    #         return []
    #     else:
    #         if len(db_result) >= 22 and len(db_result) <= 25:
    #             return [i[0] for i in db_result]
    #         else:
    #             raise Exception("Invalid number of games found")
    
    
    # def final_df_with_injury_info(final_player_df, args, now):
    # # Sorting by date
    #     final_player_df.sort_values(by=["Date"], inplace=True)
    #     latest_game = final_player_df.GameID.values[0]
    #     sel_by_df = final_player_df[final_player_df.GameID == latest_game]
    #     sel_by_df.to_csv(f"./Results/{latest_game}_{now}.csv", index=False)

    #     for game in final_player_df.GameID.unique():
    #         if "Announced" in final_player_df[final_player_df.GameID == game].OperatorMatchInfo.values.tolist():
    #             final_player_df["OperatorMatchInfo"] = final_player_df.apply(
    #                 lambda row: "Unannounced" if row["OperatorMatchInfo"] == "" else row["OperatorMatchInfo"], axis=1)
    #         else:
    #             unique_teams_in_game, latest_game_team1, latest_game_team2, final_game_impact_players = get_latest_game_info(game, args.ss_series_name.upper())
    #             latest_game_players_team1 = slate.get_game_players(game_id=latest_game_team1)
    #             latest_game_players_team2 = slate.get_game_players(game_id=latest_game_team2)
                
    #             if len(latest_game_players_team1) > 0:
    #                 final_game_players = latest_game_players_team1 + latest_game_players_team2
    #                 for player in final_player_df[final_player_df.GameID == game].PlayerID.values.tolist():
    #                     if player in final_game_players:
    #                         if final_game_impact_players.shape[0] != 0 and player in final_game_impact_players.PlayerID.values.tolist():
    #                             final_player_df.loc[(final_player_df.GameID == game) & (final_player_df.PlayerID == player), "OperatorMatchInfo"] = final_game_impact_players.loc[(final_game_impact_players.PlayerID) == player]["Sub_status"].values[0]
    #                         else:
    #                             final_player_df.loc[(final_player_df.GameID == game) & (final_player_df.PlayerID == player), "OperatorMatchInfo"] = "Played last match"

    #     final_player_df.to_csv(f"modified_{args.ss_series_name}.csv", index=False)
    #     final_player_df["InjuryStatus"] = None
    #     final_player_df["InjuryInfo"] = None
    #     excluded = get_records_from_sheet(args.ss_series_name.upper())
    #     _, _, _, final_game_impact_players = get_latest_game_info(game, args.ss_series_name.upper())

    #     for index, row in final_player_df.iterrows():
    #         if row["OperatorMatchInfo"] in ["Played last match", "Played last match(sub_out)"]:
    #             final_player_df.loc[final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"] = "Probable"
    #         elif row["OperatorMatchInfo"] == "Substitute":
    #             if final_game_impact_players.shape[0] != 0 and row["PlayerID"] in final_game_impact_players.loc[(final_game_impact_players.PlayerID == row["PlayerID"]) & (final_game_impact_players.Sub_status == "Played last match(sub_in)")].PlayerID.values.tolist():
    #                 final_player_df.loc[final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"] = "Probable(sub)"
    #             else:
    #                 final_player_df.loc[final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"] = "Questionable"
    #         elif row["OperatorMatchInfo"] in ["Played last match (Sub)", "Played last match(sub_in)"]:
    #             final_player_df.loc[final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"] = "Probable(sub)"
    #         elif row["OperatorMatchInfo"] == "Unavailable":
    #             final_player_df.loc[final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"] = "Out"
    #         elif row["OperatorMatchInfo"] == "Announced":
    #             final_player_df.loc[final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"] = "Probable"
    #         else:
    #             final_player_df.loc[final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"] = "Questionable"
            
    #         final_player_df.loc[final_player_df.PlayerID == row["PlayerID"], "InjuryInfo"] = None
            
    #         if len(excluded) > 0 and row["PlayerID"] in excluded.PlayerID.values.tolist():
    #             final_player_df.loc[final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"] = excluded[excluded.PlayerID == row["PlayerID"]].Status.values[0]
    #             final_player_df.loc[final_player_df.PlayerID == row["PlayerID"], "InjuryInfo"] = excluded[excluded.PlayerID == row["PlayerID"]].Info.values[0]

    #     map_df = final_player_df[final_player_df["PlayerID"] == -1]



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--d11_lid', type=str, help="League ID on D11")
    parser.add_argument('--d11_mid', type=str, help="Match ID on D11")
    parser.add_argument('--st_lid', type=str, help="League ID on st")
    parser.add_argument('--st_mid', type=str, help="Match ID on st")
    args = parser.parse_args()
    
    d_11=slate.generate_d11_team_jsons(4669,98176)
    st=slate.generate_st_team_jsons(10899,43374)
    pairs=slate.match_and_rank_names(list(d_11.keys()),list(st.keys()))
    slate.match_and_rank_players(d_11,st,pairs,98176)
    # slate.toss(d_11,st,pairs)

        
        
    
    
        
