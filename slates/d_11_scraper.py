from libImports import *
import argparse as args
from sqlalchemy import create_engine
import pandas as pd
# from update import get_records_from_sheet

dbname="ECSN_portugal_T10_DB"
user="postgres"
password="12345"
host='localhost'
port="5432"

engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')

def getSchedule():
        engine = create_engine("postgresql+psycopg2://postgres:12345@localhost/ECSN_T10_DB")

        df = pd.read_sql("SELECT * FROM schedule;", engine)
        return df
    
schedule_df = getSchedule()

def ST_team_maps():
        engine = create_engine("postgresql+psycopg2://postgres:12345@localhost/ECSN_T10_DB")

        df = pd.read_sql("SELECT * FROM team;", engine)
        return df
    
team_maps = ST_team_maps()

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


    def get_best_match(team_name, team_list, threshold=0.5):
        best_match = None
        best_score = 0
        for team in team_list:
            score = SequenceMatcher(None,team_name.lower(), team.lower()).ratio()
            if score > best_score:
                best_score = score
                best_match = team
        return best_match

    game_id_counter = {}
    def getGameID(team1, team2, d11_date):
        """Returns Sportsseam's game id for the two team names provided

        Args:
            team1 (str): D11 full Team Name 
            team2 (str): D11 full Team Name 

        Returns:
            str: Returns SS game id from schedule.
        """
        team_list = team_maps['TeamFullName'].tolist()
    
        # Match team names against full names
        matched_team1 = slate.get_best_match(team1, team_list) or team1
        matched_team2 = slate.get_best_match(team2, team_list) or team2
        
        # Get corresponding standardized team names
        std_team1 = team_maps.loc[team_maps['TeamFullName'] == matched_team1, 'TeamName'].iloc[0]
        std_team2 = team_maps.loc[team_maps['TeamFullName'] == matched_team2, 'TeamName'].iloc[0]
        
        # Get schedule data for matched teams
        date_info = schedule_df[
            ((schedule_df.Team == std_team1) & (schedule_df.Opponent == std_team2)) |
            ((schedule_df.Team == std_team2) & (schedule_df.Opponent == std_team1))
        ]
        
        d11_datetime = datetime.strptime(d11_date, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc)

        # Find the closest match based on both date and time
        closest_match = min(
            date_info.itertuples(),
            key=lambda row: abs(
                datetime.strptime(f"{row.Date} {row.Time}", "%Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.utc) - d11_datetime
            )
        )
        return closest_match.GameID
        
        
        #possible = date_info.GameID.values,date_info.Date.values
        # # min_hours_between = 240
        # min_hours_between = 1
        # most_likely_id = None
        
        # for id,date in possible:
        #     match_date = datetime.strptime(date, "%Y-%m-%d").date()
        #     match_time = date_info[date_info.Date == date].Time.values[0]
        #     match_time = datetime.strptime(match_time, "%H:%M:%S").time()
        #     match_datetime = datetime.combine(match_date, match_time)

        #     today = datetime.strftime(
        #         datetime.now(tz=pytz.timezone(
        #             "UTC")), "%Y-%m-%dT%H:%M:%S"
        #     )

        #     today_datetime = datetime.strptime(today, "%Y-%m-%dT%H:%M:%S")
        #     hour_diff = (match_datetime - today_datetime).total_seconds() // 3600
        #     print(hour_diff)
        #     if (hour_diff >= 0) and (hour_diff < min_hours_between):
        #         min_hours_between = hour_diff
        #         most_likely_id = id
        #     elif (hour_diff < 0):
        #         most_likely_id = id
        #     breakpoint()
        # try:
        #     match_id = most_likely_id
        # except:
        #     for day in date_info.Date.values:
        #         if day == d11_date:
        #             match_id = most_likely_id
        # return match_id


    

    def getGameID_fromdt(team1, team2, game_date):
        """Returns Sportsseam's game id for the two team names provided

        Args:
            team1 (str): D11 full Team Name 
            team2 (str): D11 full Team Name 
            game_dt (str): Game datetime obtained from dream11 API JSON

        Returns:
            str: Returns unique SS game id from schedule.
        """
        team_list = team_maps['TeamFullName'].tolist()
    
        # Match team names against full names
        matched_team1 = slate.get_best_match(team1, team_list) 
        matched_team2 = slate.get_best_match(team2, team_list)
        # breakpoint()
        # Get corresponding standardized team names
        std_team1 = team_maps.loc[team_maps['TeamFullName'] == matched_team1, 'TeamName'].iloc[0]
        std_team2 = team_maps.loc[team_maps['TeamFullName'] == matched_team2, 'TeamName'].iloc[0]
        
        # Get schedule data for matched teams
        date_info = schedule_df[
            ((schedule_df.Team == std_team1) & (schedule_df.Opponent == std_team2)) |
            ((schedule_df.Team == std_team2) & (schedule_df.Opponent == std_team1))
        ]
        possible_match_dates = date_info.Date.values
        most_likely_match_date = None
        
        game_dt = datetime.strptime(game_date, "%Y-%m-%dT%H:%M:%S.000Z")
        game_dt_in_str = game_dt.strftime("%Y-%m-%d %H:%M:%S")
        match_id = None
        
        for date in possible_match_dates:
            match_date = datetime.strptime(date, "%Y-%m-%d").date()
            match_time = date_info[date_info.Date == date].Time.values[0]
            match_time = datetime.strptime(match_time, "%H:%M:%S").time()
            match_datetime = datetime.combine(match_date, match_time)
            match_datetime_in_str = match_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # if match_datetime_in_str == game_dt_in_str:
            #     most_likely_match_date = date
            #     match_id = date_info[date_info.Date == most_likely_match_date].GameID.values[0]
            #     break
            # elif date == game_dt.strftime("%Y-%m-%d"):
            #     match_id = slate.getGameID(team1=team1, team2=team2, d11_date=date)
            match_id = slate.getGameID(team1=team1, team2=team2, d11_date=game_date)
  
        # if match_id:
        #     if match_id in slate.game_id_counter:
        #         slate.game_id_counter[match_id] += 1    
        #         match_id = f"{match_id}_{slate.game_id_counter[match_id]}" 
        #     else:
        #         slate.game_id_counter[match_id] = 1
        #     breakpoint()
                
            
        
        return match_id,[matched_team1,std_team1,matched_team2,std_team2]

    
    
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
        all_names = d11_teams + st_teams
        remaining_names = [name for name in all_names if name not in best_pair]
        
        if len(remaining_names) == 2:
            second_pair = tuple(remaining_names)
        else:
            print("error in matching teams")
            return
        
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

    
    def squad():
        engine = create_engine("postgresql+psycopg2://postgres:12345@localhost/ECSN_T10_DB")

        df = pd.read_sql("SELECT * FROM team_squad;", engine)
        return df
    
    team_squad = squad()
    
    def generate_st_team_jsons(t1_name, t1_sname, t2_name, t2_sname):
        """
        Generate team squad JSONs for two teams using team_squad table data
        
        Parameters:
        t1_name (str): Team 1 full name
        t1_sname (str): Team 1 short name
        t2_name (str): Team 2 full name
        t2_sname (str): Team 2 short name
        
        Returns:
        dict: Dictionary containing squad information for both teams
        """
        team_jsons = {}
        
        # Initialize team JSON structure
        if t1_name:
            team_jsons[t1_name] = {"sname": t1_sname, "players": []}
        if t2_name:
            team_jsons[t2_name] = {"sname": t2_sname, "players": []}
        
        # Get and process team 1 squad
        t1_players = slate.team_squad[slate.team_squad['TeamName'] == t1_sname]
        for _, player in t1_players.iterrows():
            name = str(player['PlayerName']).strip()
            p_id = str(player['PlayerID']).strip()
            
            if not name or not p_id:
                continue
                
            team_jsons[t1_name]["players"].append({
                "id": p_id,
                "name": name
            })
        
        # Get and process team 2 squad
        t2_players = slate.team_squad[slate.team_squad['TeamName'] == t2_sname]
        for _, player in t2_players.iterrows():
            name = str(player['PlayerName']).strip()
            p_id = str(player['PlayerID']).strip()
            
            if not name or not p_id:
                continue
                
            team_jsons[t2_name]["players"].append({
                "id": p_id,
                "name": name
            })
        
        return team_jsons
    
    


    slate_counter = {}  
    def match_and_rank_players(team1_json, team2_json, pairs, d11_match_id,gameid):
        
        t1 = pairs.get('p1').get('names') 
        t2 = pairs.get('p2').get('names')
        #d11_date = team1_json.get(t1[0], {}).get('date', '')
        # formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y%m%d")
        #a=list(team1_json.keys())

        # gameid,_=slate.getGameID_fromdt(a[0],a[1],d11_date)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        todays_date = now.strftime("%Y-%m-%d")
        
        matched_players = []
        slate_info=[]
        game_slate=[]
        
        date = team1_json.get(t1[0], {}).get('date', '')
        mdate=datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y%m%d")
        
        

        slateid = "".join(formatted_date.split("-")) + "11"

        if slateid in slate.slate_counter:
            slate.slate_counter[slateid] += 1
        else:
            slate.slate_counter[slateid] = 1

        slate_id=(f"{slateid}_{slate.slate_counter[slateid]}")
        

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
                        "Season": args.year,
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
                        "D11_MatchID": d11_match_id,
                        "Dream11PlayerID": d11_id,
                        "PlayingOrder": B_order,
                    })
                    used_names.add(d11_name)
                    used_names.add(st_name)
                    i+=1
                    
                            
        final_player_df = pd.concat([slate.player_df, pd.DataFrame(matched_players)], ignore_index=True)
        #df_player.to_csv('player_slate.csv',index=False)
        #final_player_df =df_player
        def get_latest_game(team, season):
            """Get latest game played by team from scoreboard table

            Args:
                team (_type_): Name of the team whose latest game is required
                season (_type_): Season from which data is needed

            Raises:
                Exception: Raised when query returns more than one game.

            Returns:
                str: Game ID of latest game
            """
            query = f"""
                    select "GameID" from scoreboard WHERE "Season"::INTEGER = {season}  and ("Team" = '{team}' or "Opponent" = '{team}') order by "Date" DESC limit 1;
                    """
            con = psycopg2.connect(
                user=user, password=password, host=host, port=port, database="ECSN_T10_DB"
            )
            cur = con.cursor()
            cur.execute(query)
            db_result = cur.fetchall()
            con.close()
            if not db_result:
                print("Latest Game Not Found")
            else:
                if len(db_result[0]) == 1:
                    return db_result[0][0]
                else:
                    raise Exception("Invalid number of games found")
            
        def get_latest_game_info(game,season):
            unique_teams_in_game = (
                        final_player_df[final_player_df.GameID == game].Team.unique().tolist()
            )
            print(unique_teams_in_game, "teams")
            latest_game_team1 = get_latest_game(
                team=unique_teams_in_game[0], season=season
            )
            latest_game_team2 = get_latest_game(
                team=unique_teams_in_game[1], season=season
            )
            print(latest_game_team1, latest_game_team2, "games")

            return unique_teams_in_game,latest_game_team1, latest_game_team2
        
        def get_game_players(game_id):
            """Return list of 22 players who have played in provided game if

            Args:
                game_id (str): Game ID whose player list is required

            Raises:
                Exception: Raised when player list is not 22

            Returns:
                list: List of 22 player ids
            """
            query = f"""
                    select "PlayerID" from scoreboard where "GameID" = '{game_id}';
                    """
            con = psycopg2.connect(
                user=user, password=password, host=host, port=port, database="ECSN_T10_DB"
            )
            cur = con.cursor()
            cur.execute(query)
            db_result = cur.fetchall()
            con.close()
            print(db_result)
            if not db_result:
                print("Latest Game Not Found")
                return []
            else:
                if len(db_result) >= 22 and len(db_result) <= 25:
                    return [i[0] for i in db_result]
                else:
                    raise Exception("Invalid number of games found")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        todays_date = now.strftime("%Y-%m-%d")
        
        final_player_df.sort_values(by=["Date"], inplace=True)
        # latest_game = final_player_df.GameID.values[0]
        # sel_by_df = final_player_df[final_player_df.GameID == latest_game]
        #sel_by_df.to_csv(f"./Results/{latest_game}_{now}.csv", index=False)
        for game in final_player_df.GameID.unique():
            if (
                "Announced"
                in final_player_df[
                    final_player_df.GameID == game
                ].OperatorMatchInfo.values.tolist()
            ):
                final_player_df["OperatorMatchInfo"] = final_player_df.apply(
                    lambda row: "Unannounced" if row["OperatorMatchInfo"] == "" else row["OperatorMatchInfo"], axis=1)
                #print("Players Already Announced")
            else: 
                unique_teams_in_game,latest_game_team1, latest_game_team2 = get_latest_game_info(game,args.year)

                latest_game_players_team1 = get_game_players(
                    game_id=latest_game_team1)
                latest_game_players_team2 = get_game_players(
                    game_id=latest_game_team2)
                print(latest_game_players_team1,
                    latest_game_players_team2, "players")

                if len(latest_game_players_team1) > 0:
                    print(latest_game_players_team1 + latest_game_players_team2)
                    final_game_players = (
                        latest_game_players_team1 + latest_game_players_team2
                    )
                    for player in final_player_df[
                        final_player_df.GameID == game
                    ].PlayerID.values.tolist():
                        if player in final_game_players:
                            final_player_df.loc[(final_player_df.GameID == game) & (final_player_df.PlayerID == player), "OperatorMatchInfo"
                                                ] = "Played last match"
                        else:
                            pass
        # final_player_df.to_csv(f"modified_{args.ss_series_name}.csv", index=False)
        final_player_df["InjuryStatus"] = None
        final_player_df["InjuryInfo"] = None
        # excluded = get_records_from_sheet(args.ss_series_name.upper())
        #getting the impact players when the game is announced

        for index, row in final_player_df.iterrows():
            if row["OperatorMatchInfo"] == "Played last match" or row["OperatorMatchInfo"] == "Played last match(sub_out)":
                final_player_df.loc[
                    final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"
                ] = "Probable"
            #managing the status of all substitute players and who played last match after announcement.
            elif row["OperatorMatchInfo"] == "Substitute":
                final_player_df.loc[
                    final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"] = "Questionable"            
            #adjusting the player status for the substitute players who played in the match.
            elif row["OperatorMatchInfo"] == "Played last match (Sub)" or row["OperatorMatchInfo"] == "Played last match(sub_in)":
                final_player_df.loc[
                    final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"
                ] = "Probable(sub)"
            elif row["OperatorMatchInfo"] == "Unavailable":
                final_player_df.loc[
                    final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"
                ] = "Out"
            #making announced players status as probable
            elif row["OperatorMatchInfo"] == "Announced":

                final_player_df.loc[
                    final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"
                ] = "Probable"
            else:
                final_player_df.loc[
                    final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"
                ] = "Questionable"
            final_player_df.loc[final_player_df.PlayerID ==
                                row["PlayerID"], "InjuryInfo"] = None
            
        file_path = "player_slate.csv"
        write_header = not os.path.exists(file_path) 
        final_player_df.to_csv(file_path, mode="a", index=False, header=write_header)
        final_player_df.to_sql('player_slate', engine, if_exists='append', index=False)

        slate_info.append({
            "SlateID": slate_id,
            "Date": mdate,
            "Season": args.year,
            "Operator": "Dream 11",
            "OperatorName": "DailyFantasy",
            "OperatorDay": todays_date,
            "OperatorTime": current_time,
            "SalaryCap": "100",
            "NumberOfGames": "1",
            "GameStatus" : "Announced",
        })
        
        game_slate.append({
            "SlateGameID": gameid+'_11',
            "Season": args.year,
            "Date": mdate,
            "SlateID": slate_id,
            "GameID": gameid,
            "Updated":todays_date,
            "GameStatus" : "Announced"
        })
        
        toss=[]
        
        df_slate = pd.concat([slate.slate_df, pd.DataFrame(slate_info)], ignore_index=True)
        file_path = "slate.csv"
        write_header = not os.path.exists(file_path)  
        df_slate.to_csv(file_path, mode="a", index=False, header=write_header)
        df_slate.to_sql('slate', engine, if_exists='append', index=False)
        
        df_game_slate = pd.concat([slate.game_slate_df, pd.DataFrame(game_slate)], ignore_index=True)
        file_path = "game_slate.csv"
        write_header = not os.path.exists(file_path)  
        df_game_slate.to_csv(file_path, mode="a", index=False, header=write_header)
        
        df_game_slate.to_sql('game_slate', engine, if_exists='append', index=False)
        
        # d11_date = team1_json.get(t1[0], {}).get('date', '')
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
        file_path = "toss.csv"
        write_header = not os.path.exists(file_path)  
        df_toss.to_csv(file_path, mode="a", index=False, header=write_header)
        df_toss.to_sql('toss_info', engine, if_exists='append', index=False)
        
    

        

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=str,default=2025, help="season")
    parser.add_argument('--d11_lid', type=str, help="League ID on D11")
    #parser.add_argument('--d11_mid', type=str, help="Match ID on D11")
    
    args = parser.parse_args()
    for i in [98168,98169,98170,98171,98172,98173,98174,98175,98176,98177,98178,98179,98180,
              98181,98182,98183,98185,98186,98187,98188,98189,98190,98191,98192,98193,98194]:
        d_11=slate.generate_d11_team_jsons(4669,i)
        gameid,info_list=slate.getGameID_fromdt(list(d_11.keys())[0],list(d_11.keys())[1],d_11.get(list(d_11.keys())[0], {}).get('date', ''))
        st=slate.generate_st_team_jsons(info_list[0],info_list[1],info_list[2],info_list[3])
        pairs=slate.match_and_rank_names(list(d_11.keys()),list(st.keys()))
        slate.match_and_rank_players(d_11,st,pairs,i,gameid)
    


        
        
    
        
