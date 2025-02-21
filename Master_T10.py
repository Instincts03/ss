import pandas as pd
from t10_scoreboard_scraper import info_extract

def process_csv():
    id_file="T10_id_info.csv"
    df = pd.read_csv(id_file)
    info = info_extract()

    for index, row in df[df['Check'] == 0].iterrows():
        match_id = str(row['MatchID'])
        league_id = str(row['LeagueID'])
        payload_overview = {"spt_typ": 1, "l_id": league_id, "m_id": match_id}
        response=info_extract.make_request("/Prod/match-overview", payload_overview)
        
        if response.get('result',{}).get('matchInfo',{}).get('status',{}) == "completed":
            try:  
                info.process_single_match(league_id, match_id)
                df.at[index, 'Check'] = 1

            except Exception as e:
                print(f"Error processing Match ID {match_id}, League ID {league_id}: {e}")
                print({'match_id': match_id, 'league_id': league_id, 'error': str(e)})
        
        else:
            continue

    df.to_csv(id_file, index=False)


if __name__ == "__main__":
    process_csv()
