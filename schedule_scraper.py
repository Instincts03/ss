import http.client
import json
import datetime
import pandas as pd
import argparse
import pytz
from sqlalchemy import create_engine
import datetime 


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
    

class Schedule:
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
    def schedule_scrap(l_id, season):
        GameID, Season, SeasonType, Date, Status, Team,Teamfn, TeamID, Opponent,Opponentfn, OpponentID = [], [], [], [], [], [], [], [], [], [], []
        Venue, Time, Time_IST, HomeTeam, AwayTeam = [], [], [], [], []

        payload = {"spt_typ": 1, "l_id": str(l_id)}
        endpoints = ["/Prod/completed-matches-by-league", "/Prod/live-matches-by-league", "/Prod/upcoming-matches-by-league"]
        responses = [Schedule.make_request(endpoint, payload) for endpoint in endpoints]

        try:
            for response in responses:
                if "error" in response:
                    print(f"API error: {response['error']}")
                    continue

                for result in response.get("result", []):
                    ist = pytz.timezone('Asia/Kolkata')  # Define IST timezone
                    utc = pytz.utc  # Define UTC timezone

                    timestamp = result.get('strt_time_ts')
                    if timestamp:
                        dt_object_utc = datetime.datetime.fromtimestamp(timestamp, tz=utc)  # Interpret as UTC
                        
                        # Convert UTC to IST
                        dt_object_ist = dt_object_utc.astimezone(ist)

                        # Format UTC and IST times
                        formatted_utc_time = dt_object_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")
                        formatted_ist_time = dt_object_ist.strftime("%Y-%m-%dT%H:%M:%S.000Z")

                        # Extract game date & times
                        game_date = formatted_utc_time.split('T')[0]  # Date remains same for both
                        game_time_utc = formatted_utc_time.split('T')[1].split('.')[0]
                        game_time_ist = formatted_ist_time.split('T')[1].split('.')[0]
                    else:
                        game_date = game_time_utc = game_time_ist = "null"

                    # Determine match type
                    if result.get("m_name", "").split(',')[1].strip().startswith('Match'):
                        type = 'DRR'
                    else:
                        type = 'POFF'

                    # Generate Unique Game ID (Ensure it's based on UTC)
                    time_str = dt_object_utc.strftime("%Y%m%d")  # UTC-based date string
                    t1 = result.get('t1_sname', "null")
                    t2 = result.get('t2_sname', "null")
                    id = f"{time_str}{t1}{t2}"  # Combine components to create ID

                    # Handle game ID counter logic
                    if id:
                        if id in Schedule.game_id_counter:
                            Schedule.game_id_counter[id] += 1
                        else:
                            Schedule.game_id_counter[id] = 1
                        id = f"{id}_{Schedule.game_id_counter[id]}"
                    
                    m_id=result.get('m_id', "")
                    p={"spt_typ":1,"l_id":str(l_id),"m_id":str(m_id)}
                    venue=Schedule.make_request("/Prod/match-info",p).get('result',{}).get('venue',{}).split(',')[0]

                    if result.get('status', 'null')=="completed":
                        status='Finished'
                    else:
                        status='Scheduled'
                    GameID.append(id)
                    Season.append(season)
                    SeasonType.append(type)
                    Date.append(game_date)
                    Status.append(status)
                    Team.append(result.get("t1_sname", "null"))
                    TeamID.append(result.get("t1_id", "null"))
                    Opponent.append(result.get("t2_sname", "null"))
                    OpponentID.append(result.get("t2_id", "null"))
                    Time.append(game_time_utc)
                    Time_IST.append(game_time_ist)
                    HomeTeam.append(result.get("t1_sname", "null"))
                    AwayTeam.append(result.get("t2_sname", "null"))
                    Venue.append(venue)
                    # Teamfn.append(result.get("t1_name", "null"))
                    # Opponentfn.append(result.get("t2_name", "null"))
            
            df_sched = pd.DataFrame({
                "GameID": GameID,
                "Season": Season,
                "SeasonType": SeasonType,
                "Date": Date,
                "Status": Status,
                "Team": Team,
                "TeamID": TeamID,
                "Opponent": Opponent,
                "OpponentID": OpponentID,
                "Venue": Venue,
                "Time": Time,
                "Time_IST": Time_IST,
                "HomeTeam": HomeTeam,
                "AwayTeam": AwayTeam,
                # "Teamfn":Teamfn,
                # "Opponentfn":Opponentfn
            })
            
            df_sched.to_sql('schedule', engine, if_exists='replace', index=False)

            print("Data pushed successfully!")

            # df_sched.to_csv(f"{l_id}_schedule.csv", index=False)
            # print(f"Schedule saved as {l_id}_schedule.csv")

        except Exception as e:
            print(f"Error occurred: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--l_id', type=str, default="10899", help="League ID")
    parser.add_argument('--year', type=int, default="2025", help="Season Year")
    args = parser.parse_args()

    Schedule.schedule_scrap(args.l_id, args.year)

if __name__ == "__main__":
    main()
