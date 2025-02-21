import http.client
import json
import re
import pandas as pd
import os
import argparse as args
# years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
# years=[2025]
# Function to make requests

def main():
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

    # Keep track of unique Match IDs
    unique_match_ids = set()

    csv_file = 'T10_id_info.csv'

    existing_df = pd.read_csv(csv_file, dtype={'LeagueID': int, 'MatchID': int})  
    existing_pairs = set(zip(existing_df['LeagueID'], existing_df['MatchID']))
    
    
    conn = http.client.HTTPSConnection("apis.sportstiger.com")
    payload = json.dumps({
        "spt_typ": 1,
        "year": str(args.year)
    })
    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
        'sec-ch-ua-mobile': '?0',
        'deviceId': 'fbe9aa6786d82161f6bc409cdd67f76f',
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
    conn.request("POST", "/Prod/archive-series-web", payload, headers)
    res = conn.getresponse()
    response_data = json.loads(res.read().decode("utf-8"))
        
    for j in range(len(response_data.get('result', {}).get('competitions', []))):
        if response_data.get('result', {}).get('competitions', [])[j].get('category', "") == "T10 League":
            i = j
            months = response_data.get('result', {}).get('competitions', [])[i].get('data', [])

            seasons = []
            category = []
            l_name = []
            lid_list = []
            mid_list = []
            check=[]
            
            for month in months:
                season = (re.search(r'(\d{4})', month.get('yearMonth', ""))).group(1)
                leagues = month.get('series', [])
                for league in leagues:
                    cat = league.get("cat", "")
                    name = league.get("l_name", "")
                    l_id = league.get('l_id')
                    l_payload = {"spt_typ": 1, "l_id": l_id}
                    league_matches = make_request("/Prod/completed-matches-by-league", l_payload, headers)
                    for mats in league_matches.get("result", []):
                        m_id = mats.get("m_id", "null")
                        # breakpoint()
                        # Check if Match ID is unique
                        if (int(l_id),int(m_id)) not in existing_pairs:
                            existing_pairs.add((l_id, m_id))
                            unique_match_ids.add(m_id)
                            mid_list.append(m_id)
                            lid_list.append(l_id)
                            seasons.append(season)
                            category.append(cat)
                            l_name.append(name)
                            check.append(0)
            
            df_info = pd.DataFrame({
                'Seasons': seasons,
                'Category': category,
                'LeagueName': l_name,
                'LeagueID': lid_list,
                'MatchID': mid_list,
                'Check':check
            })
            
            # Save to CSV
            df_info.to_csv(csv_file, index=False, mode='a', header=not os.path.exists(csv_file))
                
        else:
            continue
        
        
    for j in range(len(response_data.get('result', {}).get('competitions', []))):
        if response_data.get('result', {}).get('competitions', [])[j].get('category', "") == "Domestic":
            months=response_data.get('result', {}).get('competitions', [])[j].get('data',[])
            for month in months:
                series=month.get('series')
                k=0
                for match in series:
                    if '10' in match.get('l_name', ''):
                        i = j
                        
                        #breakpoint()

                        seasons = []
                        category = []
                        l_name = []
                        lid_list = []
                        mid_list = []
                        check=[]
                        
                        season = (re.search(r'(\d{4})', month.get('yearMonth', ""))).group(1)
                        cat = match.get("cat", "")
                        name = match.get("l_name", "")
                        l_id = match.get('l_id')
                        l_payload = {"spt_typ": 1, "l_id": l_id}
                        league_matches = make_request("/Prod/completed-matches-by-league", l_payload, headers)
                        for mats in league_matches.get("result", []):
                            m_id = mats.get("m_id", "null")
                            
                            if (int(l_id),int(m_id)) not in existing_pairs:
                                existing_pairs.add((l_id, m_id))
                                unique_match_ids.add(m_id)
                                mid_list.append(m_id)
                                lid_list.append(l_id)
                                seasons.append(season)
                                category.append(cat)
                                l_name.append(name)
                                check.append(0)
                        
                        df_info = pd.DataFrame({
                            'Seasons': seasons,
                            'Category': category,
                            'LeagueName': l_name,
                            'LeagueID': lid_list,
                            'MatchID': mid_list,
                            'Check':check
                        })
                            
                        # Save to CSV
                        df_info.to_csv(csv_file, index=False, mode='a', header=not os.path.exists(csv_file))
                    else:
                        continue
        else:
            continue
            
if __name__=="__main__":
    parser = args.ArgumentParser()
    parser.add_argument('--year', type=int, default=2025,help="Season (from 2019 to 2025)")
    args = parser.parse_args()
    main()