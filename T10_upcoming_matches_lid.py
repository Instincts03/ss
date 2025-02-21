import http.client
import json
import re
import pandas as pd
import os

def make_request(endpoint, payload):
    headers = {
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Brave";v="132"',
    'sec-ch-ua-mobile': '?0',
    'deviceId': '8fbd3417649745ce6a289ad75332cc54',
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

# Upcoming match details
payload_1 = {
    "spt_typ": 1
}

response_data = make_request("/Prod/get-upcoming-matches", payload_1)

existing_df = pd.read_csv('T10_id_info.csv')           ### csv file name to check with
    
for result in response_data.get('result',[])[1:]:
    for match in result.get('data',[]):
        if match.get('matches',"")[0].get('format',"") == "t10":
            cat=result.get('category',"")
            seasons = []
            category = []
            l_name = []
            lid_list = []
            mid_list = []
            check=[]
            
            l_id=match.get('l_id',"")
            name=match.get('l_name',"")
            
            #status for each match
            payload_2 = {
            "spt_typ": 1,
            "l_id": l_id
            }
            status_response = make_request("/Prod/get-competition-info", payload_2)
            if status_response.get('result',{}).get('status',{})=='live':
                if l_id==10483:
                    breakpoint()
                if not ((existing_df['Seasons'] == 2025) & (existing_df['LeagueID'] == l_id)).any():
                    l_payload = {"spt_typ": 1, "l_id": l_id}
                    league = make_request("/Prod/completed-matches-by-league", l_payload)
                    for mats in league.get("result", []):
                        if mats.get("format")=="t10":
                            m_id = mats.get("m_id", "null")
                            mid_list.append(m_id)
                            lid_list.append(l_id)
                            seasons.append(2025)
                            category.append(cat)
                            l_name.append(name)
                            check.append(0)
                            
                    league = make_request("/Prod/upcoming-matches-by-league", l_payload)
                    for mats in league.get("result", []):
                        if mats.get("format")=="t10":
                            m_id = mats.get("m_id", "null")
                            mid_list.append(m_id)
                            lid_list.append(l_id)
                            seasons.append(2025)
                            category.append(cat)
                            l_name.append(name)
                            check.append(0)
                        
                    league = make_request("/Prod/live-matches-by-league", l_payload)
                    for mats in league.get("result", []):
                        if mats.get("format")=="t10":
                            m_id = mats.get("m_id", "null")
                            mid_list.append(m_id)
                            lid_list.append(l_id)
                            seasons.append(2025)
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
            df_info.to_csv('T10_id_info.csv', index=False, mode='a', header=not pd.io.common.file_exists('T10_id_info.csv'))   ###T10

            
        else:
            continue
    
                    