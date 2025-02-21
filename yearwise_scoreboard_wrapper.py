from t10_scoreboard_scraper import info_extract
import http.client
import json
import argparse

class wrapper():
    @staticmethod
    def year_scoreboard_wrapper_function(year,i):   # i is for index (international,T20,T10,domestic,women)


        conn = http.client.HTTPSConnection("apis.sportstiger.com")
        payload = json.dumps({
        "spt_typ": 1,
        "year": str(year)
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
        
        months=response_data.get('result',{}).get('competitions',{})[i].get('data',[])
        
        lid_list=[]
        
        for month in months:
            leauges=month.get('series',[])
            for leauge in leauges:
                lid=leauge.get('l_id')
                lid_list.append(lid)
            
        processor=info_extract()
        
        for l_id in lid_list:
            processor.process_league_matches(l_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=str, default="2024", help="year")
    args = parser.parse_args()

    wrapper.year_scoreboard_wrapper_function(args.year, 2)