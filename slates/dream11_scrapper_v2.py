# from exceptions import (
#     APINotSupportedException,
#     D11TeamFullNameNotSupportedException,
#     NoLiveMatchesForSeries_Dream11,
#     SeriesNotSupportedException,
# )

#4150

from libImports import *
# from update import get_records_from_sheet
# from postgres_config import postgresCredentials, SERIES_DB_MAPPER
# from automated_scorecard_script import get_data_for_league
# from scorecard_v2_1 import get_playing_11_json
# from espn_hsci_generator import ESPNHMacGenerator
# from enter_extra_data import enter_extra_data
#postgres auth
# host, port, user, password = postgresCredentials()


player_data_cols = [
    "PlayerName",
    "PlayerTeam",
    "PlayerFullTeam",
    "Dream11PlayerID",
    "OperatorPlayerCredits",
    "Position",
    "OperatorMatchInfo",
    "OperatorBetsMade",
    "OperatorPlayerFantasyPoints",
    "D11_MatchID",
    "PlayingOrder"
]

slate_df_cols = [
    "SlateID",
    "Date",
    "DateTime",
    "Season",
    "Operator",
    "OperatorName",
    "OperatorTime",
    "OperatorDate",
    "SalaryCap",
    "GameStatus",
    "D11_MatchID",
]

game_slate_df_cols = [
    "SlateGameID",
    "Season",
    "Date",
    "SlateID",
    "GameID",
    "Updated",
    "GameStatus",
    "D11_MatchID",
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


ids_not_mapped = []

series_id_mapper = {
    "IPL": 1410320,
    "LLC": 1408606,
    "ABUDHABIT10": 1459838,
    "ILT20": 1462172
}

def changeTeamName(x):
    """Change names of teams obtained from dream11 to names which espn uses

    Args:
        x (str): team names from dream11

    Returns:
        str: changed name of team names to espn names
    """
    if x == "Kolkata":
        return "Kolkata Knight Riders"
    if x == "Royal Challengers Bengaluru":
        return "Royal Challengers Bengaluru"
    if x == "Bengaluru":
        return "Royal Challengers Bangalore"
    if x == "Royal Challengers Bangalore":
        return "Royal Challengers Bengaluru"
    if x == "Warwickshire":
        return "Birmingham Bears"
    if x == "Saint Lucia Kings":
        return "St Lucia Kings"
    if x == "Antigua & Barbuda Falcons":
        return "Antigua and Barbuda Falcons"
    if x == "Lucknow":
        return "Lucknow Super Giants"
    if x == "UP Women":
        return "UP Warriorz Women"
    if x == "Gujarat Women":
        return "Gujarat Giants Women"
    if x == "Mumbai Women":
        return "Mumbai Indians Women"
    if x == "Delhi Women":
        return "Delhi Capitals Women"
    if x == "Bangalore Women":
        return "Royal Challengers Bangalore Women"
    if x == "Chennai":
        return "Chennai Super Kings"
    if x == "Chennai Brave Jaguars":
        return "Chennai Braves Jaguars"
    if x == "Sydney Pink Women":
        return "Sydney Sixers Women"
    if x == "Melbourne Green Women":
        return "Melbourne Stars Women"
    if x == "Melbourne Red Women":
        return "Melbourne Renegades Women"
    if x == "Brisbane Women":
        return "Brisbane Heat Women"
    if x == "Hobart Women":
        return "Hobart Hurricanes Women"
    if x == "Perth Women":
        return "Perth Scorchers Women"
    if x == "Adelaide Women":
        return "Adelaide Strikers Women"
    if x == "Sydney Green Women":
        return "Sydney Thunder Women"
    if x == "Southern Super Stars":
        return "Southern Superstars"
    if x == "New York":
        return "MI New York"
    if x == "Seattle":
        return "Seattle Orcas"
    if x == "Texas":
        return "Texas Super Kings"
    if x == "Los Angeles":
        return "Los Angeles Knight Riders"
    if x == "Washington":
        return "Washington Freedom"
    if x == "San Francisco":
        return "San Francisco Unicorns"
    if x == "Deccan":
        return "Deccan Gladiators"
    if x == "Northern":
        return "Northern Warriors"
    # if x == "Morrisville Samp Army":
    #     return "Samp Army"
    if x == "Delhi":
        return "Delhi Bulls"
    if x == "Abu Dhabi":
        return "Abu Dhabi Knight Riders"
    if x == "Abu Dhabi":
        return "Team Abu Dhabi"
    if x == "Bangla":
        return "Bangla Tigers"
    if x == "Brisbane":
        return "Brisbane Heat"
    if x == "Melbourne Green":
        return "Melbourne Stars"
    if x == "Sydney Pink":
        return "Sydney Sixers"
    if x == "Melbourne Red":
        return "Melbourne Renegades"
    if x == "Adelaide":
        return "Adelaide Strikers"
    if x == "Perth":
        return "Perth Scorchers"
    if x == "Hobart":
        return "Hobart Hurricanes"
    if x == "Sydney Green":
        return "Sydney Thunder"
    if x == "Auckland Aces":
        return "Auckland"
    if x == "Canterbury Kings":
        return "Canterbury"
    if x == "Wellington Firebirds":
        return "Wellington"
    if x == "Otago Volts":
        return "Otago"
    if x == "Northern District":
        return "Northern Districts"
    if x == "Central Stags":
        return "Central Districts"
    if x == "Auckland Hearts":
        return "Auckland Women"
    if x == "Canterbury Magicians":
        return "Canterbury Women"
    if x == "Wellington Blaze":
        return "Wellington Women"
    if x == "Otago Sparks":
        return "Otago Women"
    if x == "Northern Brave Women":
        return "Northern Districts Women"
    if x == "Central Hinds":
        return "Central Districts Women"
    if x == "Sharjah":
        return "Sharjah Warriors"
    # if x == "Sharjah Warriorz":
    #     return "Sharjah Warriors"
    if x == "Gulf":
        return "Gulf Giants"
    if x == "Dubai":
        return "Dubai Capitals"
    if x == "Emirates":
        return "MI Emirates"
    if x == " Vipers":
        return "Desert Vipers"
    if x == "Lahore":
        return "Lahore Qalandars"
    if x == "Islamabad":
        return "Islamabad United"
    if x == "Quetta":
        return "Quetta Gladiators"
    if x == "Peshawar":
        return "Peshawar Zalmi"
    if x == "Multan":
        return "Multan Sultans"
    if x == "Karachi":
        return "Karachi Kings"
    if x == "Gloucestershire":
        return "Gloucestershire"
    if x == "Essex":
        return "Essex"
    if x == "USA":
        return "United States of America"
    if x == "Oval Invincibles":
        return "Oval Invincibles (Men)"
    if x == "Birmingham Phoenix":
        return "Birmingham Phoenix (Men)"
    if x == "Southern Brave":
        return "Southern Brave (Men)"
    if x == "London Spirit":
        return "London Spirit (Men)"
    if x == "Manchester Originals":
        return "Manchester Originals (Men)"
    if x == "Welsh Fire":
        return "Welsh Fire (Men)"
    if x == "Northern Superchargers":
        return "Northern Superchargers (Men)"
    if x == "Trent Rockets":
        return "Trent Rockets (Men)"
    if x == "Oval Invincibles Women":
        return "Oval Invincibles (Women)"
    if x == "Birmingham Phoenix Women":
        return "Birmingham Phoenix (Women)"
    if x == "Southern Brave Women":
        return "Southern Brave (Women)"
    if x == "London Spirit Women":
        return "London Spirit (Women)"
    if x == "Manchester Originals Women":
        return "Manchester Originals (Women)"
    if x == "Welsh Fire Women":
        return "Welsh Fire (Women)"
    if x == "Northern Superchargers Women":
        return "Northern Superchargers (Women)"
    if x == "Trent Rockets Women":
        return "Trent Rockets (Women)"
    if x == "DP World Lions":
        return "Lions"
    if x == "North West Dragons":
        return "North West"
    if x == "Boland Rocks":
        return "Boland"
    if x == "Cape Town":
        return "MI Cape Town"
    if x == "Paarl":
        return "Paarl Royals"
    if x == "Durban":
        return "Durban's Super Giants"
    if x == "Johannesburg":
        return "Joburg Super Kings"
    if x == "Eastern Cape":
        return "Sunrisers Eastern Cape"
    if x == "Pretoria":
        return "Pretoria Capitals"
    if x == "Dhaka Capitals":
        return "Dhaka Capital"
    else:
        return x

# def get_hsci_auth_token(url):
#     # mac_generator = ESPNHMacGenerator()
#     hsci_auth_token = mac_generator.generate_hmac(url)
#     headers = {
#             "User-Agent": "Mozilla/5.0",
#             "x-hsci-auth-token": hsci_auth_token
#     }
#     return hsci_auth_token

def name_matching(str2Match, squad_df, player_team, series):
    """Name to espn player id mapping function

    Args:
        str2Match (str): Player name to be mapped
        squad_df (df): Pandas df generated from Sportsseam's database (team_squad table)
        player_team (str): Team of the player whose id is to be mapped (espn team abbreviation)
        series (str): running series name (eg IPL, PSL etc.)

    Returns:
        int: espn player id of the player.
    """
    # if series.lower() == "vb":
    ################# WC ####################
    if str2Match == "Waqar Salamkhel":
        return 1108490
    if str2Match == "Naim Sheikh" and (player_team == "BAN" or player_team == "KT"):
        return 990081
    if str2Match == "Shamim Patwari" and player_team == "BAN":
        return 1161044
    if str2Match == "Khurram Khan" and player_team == "OMAN":
        return 1077309
    if str2Match == "Fayyaz Ahmed" and player_team == "OMAN":
        return 436749
    if str2Match == "Fareed Ahmed Malik" and player_team == "AFG":
        return 568136
    if str2Match == "Michael Jones" and player_team == "SCOT":
        return 1093091
    if str2Match == "Michael Leask" and player_team == "SCOT":
        return 414966
    if str2Match == "Zia Muhammad Shahzad" and player_team == "TSK":
        return 1160390
    if str2Match == "Mohammad Jashimuddin" and player_team == "DRD":
        return 348082
    if str2Match == "Aliss Islam" and player_team == "CV":
        return 1171289
    if str2Match == "Haider Ali-I" and player_team == "DC":
        return 1160970
    if str2Match == "Mohammad Nawaz" and player_team == "KT":
        return 348148
    if str2Match == "Tom Bruce" and player_team == "CC":
        return 707113
    if str2Match == "Salman Hossain" and player_team == "SYS":
        return 932405
    if str2Match == "Mohammad Nabi" and player_team == "RR":
        return 25913
    if str2Match == "Raja Akifullah-Khan" and player_team == "DC":
        return 681067
    if str2Match == "Anamul Haque" and player_team == "KT":
        return 380354
    if str2Match == "Waseem Muhammad" and player_team == "CC":
        return 1241277
    if str2Match == "Nitish Roenick Kumar" and player_team == "USA":
        return 348129
    if str2Match == "Hazratullah Zazai" and player_team == "AFG":
        return 793457
    if str2Match == "Afif Hossain" and player_team == 'BAN':
        return 935995
    if str2Match == "Hasan Mahmud" and player_team == "BAN":
        return 926629
    if str2Match == "Inoshi Fernando" and player_team == "SL-W":
        return 371194
    if str2Match == "Izzy Gaze" and (player_team == "NZ-W" or player_team == "AK-W"):
        return 1211545
    if str2Match == "Kunwarpal Singh Tathgur" and player_team == "CAN":
        return 1206188
    if str2Match == "Parveen Kumar Dhull" and player_team == "CAN":
        return 1365333
    if str2Match == "Allah-Mohammad Ghazanfar" and player_team == "AFG":
        return 1326798
    if str2Match == "Olly Stone" and player_team == "ENG":
        return 457279
    if str2Match == "Christopher King" and player_team == "WAR":
        return 1427726
    if str2Match == "JP King" and player_team == "WAR":
        return 1361874
    if str2Match == "Raghvi Anand Singh Bist" and player_team == "IND-W":
        return 1255629
    if str2Match == "Renuka Singh Thakur" and player_team == "IND-W":
        return 960853
    if str2Match == "Haider Ali-I" and player_team == "TAD":
        return 1160970
    if str2Match == "Safeer Tariq" and player_team == "AJB":
        return 681413
    if str2Match == "Haider Ali" and player_team == "AJB":
        return 1168651
    if str2Match == "Muhammad-Shahid Iqbal Bhutta" and player_team == "DB":
        return 1460540
    if str2Match == "Akhilesh Bodugum" and player_team == "UPN":
        return 1252355
    if str2Match == "Masood-Rahman Gurbaz" and player_team == "UPN":
        return 1304696
    if str2Match == "Muhammad Zubair Khan" and player_team == "CBJ":
        return 590361
    if str2Match == "Ali-Khan" and player_team == "CBJ":
        return 927119
    if str2Match == "Ibrar Ahmed Shah" and player_team == "DG":
        return 1460538
    if str2Match == "Yazmeen Kareem" and player_team == "ND-W":
        return 1239670
    if str2Match == "Mohammad Ali" and player_team == "BRSAL":
        return 1158175
    # if str2Match == "Ramandeep Singh" and player_team == "IND":
    #     return 1079470

    ################## BBL ###################
    bbl_name_mapper = {
        "Fawad Ahmed": 240609,
        "George Garton": 643433,
        "Nic Maddinson": 333780,
        "James Seymour": 781297,
        "Joe Clarke": 571911,
        "Beau Webster": 381329,
        "Qais Ahmad": 914171,
        "Sam Elliot": 1219974,
        "Chris Jordan": 288992,
        "Peter Nevill": 6973,
        "Brody Couch": 1219972,
        "Syed Faridoun": 1291729,
        "Liam Guthrie": 858435,
        "Sam Whiteman": 334394,
        "Gurinder Sandhu": 499660,
        "Daniel Drew": 1062347,
        "Thomas Kelly": 1202263,
        "Jordan Thompson": 766809,
        "Josh Kann": 1170469,
        "Harry Brook": 911707,
        "Joel Paris": 501012,
        "Nick Winter": 501498,
        "Tom Rogers": 627627,
        "Lawrence Neil-Smith": 1130755,
        "Aaron Hardie": 1124283,
        "Nathan McSweeney": 1124290,
        "Nick Hobson": 779929,
        "Cooper Connolly": 1210488,
        "Cameron Gannon": 326635,
        "Tymal Mills": 459257,
        "David Moody": 779937,
        "Lance Morris": 1125317,
        "Tom Lammonby": 902907,
        "Jordan Cox": 1112537,
        "Thomas Andrews": 605566,
        "Andre Russell": 276298,
        "Lachlan Hearne": 1170468,
        "Ahmad Daniyal": 1249564,
        "Todd Murphy": 1193685,
        "Henry Hunt": 784615,
        "Mohammad Hasnain": 1158100,
        "Shadab Khan": 922943,
        "Tom Rogers-I": 1137283,
        "Charlie Wakim": 627623,
        "Justin Avendano": 1125715,
        "Xavier Crone": 1062338,
        "Patrick Rowe": 1130758,
        "Travis Dean": 334358,
        "Lachlan Bangs": 1295054,
        "Fakhar Zaman": 512191,
        "Chris Sabburg": 376179,
        "David Grant": 774211,
        "Steve McGiffin": 1223053,
        "Lachlan Pfeffer": 333800,
        "Jake Lehmann": 437448,
        "Jack Clayton": 1202236,
        "Bryce Street": 943417,
        "Ronan McDonald": 499488,
        "Paddy Dooley": 1089962,
        "Henry Thornton": 837611,
        "Will Sanders": 1295979,
        "Gabe Bell": 638919,
        "Jack Wildermuth": 570854,
        "Jack Wood": 1210733,
        "Ian Cockbain": 297498,
        "Jake Carder": 837609,
        "Nick Bertus": 571788,
        "Tom Fraser Rogers":1137283
    }
    psl_name_mapper = {
        "David Willey": 308251,
        "Johnson Charles": 333066,
        "Mohammad Taha-Khan": 1076394,
        "Sahibzada Farhan": 647785,
        "Rizwan-Hussain": 962107,
        "Dominic Drakes": 906749,
        "Shimron Hetmyer": 670025,
        "Dan Lawrence": 641423,
        "Will Smeed": 1099224,
        "Luke Wood": 573170,
        "Matt Parkinson": 653695,
        "Ghulam Mudassar": 938937,
        "Pat Brown": 891517,
        "Arish Ali Khan": 1076387,
        "Ashir Qureshi": 1125979,
        "Jordan Thompson": 766809,
        "Tom Lammonby": 902907,
        "Ali-Imran": 1066118,
        "Muhammad- Imran": 1234111,
        "Mohammad Imran Randhawa": 916727,
        "Imam-ul Haq": 568276,
        "Amad-Butt": 717373,
        "Hassan Khan": 959789,
        "Waqas Maqsood": 533561,
        "Usman Khan-Shinwari": 697279,
        "Liam Dawson": 211855,
        "Nasir Nawaz": 1072463,
        "Zahid Mehmood": 433614,
        "Fawad Ahmed": 240609,
        "Mohammad Irfan": 429981,
        "Benny Howell": 211748,
        "Khalid Usman": 316318,
        "Will Jacks": 897549,
        "Kieron Pollard":230559,
        'Ahsan Bhatti': 1073111,
        'Izharullahq Naveed': 1076473,
        'Wayne Parnell': 265564,
        'Sam Billings': 297628,
        'Kusal Mendis': 629074,
        'Shane Dadswell': 595406,
        'Khurram Shehzad': 681351,
        'Musa Khan': 1072472,
        'Peter Hatzoglou': 1191384,
        'Faisal Akram': 1171134,
        'Richard Gleeson': 473191,
        'Shakib Al Hasan': 56143,
        'Ben Cutting': 230371,
        'Haris Sohail': 318788,
        'Adam Rossington': 457280,
        'Nuwan Thushara': 955235,
        'Muhammad Ilyas': 1159371,
        'Carlos Brathwaite': 457249,
        'Dwaine Pretorius': 327830,
        'Saud Shakeel': 652687,
        'Tymal Mills': 459257,
        'Tom Curran': 550235,
        'Akif Javed': 1203669,
        'Gus Atkinson': 1039481,
        'Rassie van der-Dussen': 337790,
        'Dasun Shanaka':437316,
        'Najibullah-Zadran':524049,
        'Sheldon Cottrell':495551,
        'Saad Masood':1339104,
        'Yasir Khan-I':1278029,
        'Haider Ali':1168651,
        'Hasan Ali':681305,
        'Shan Masood':233901,
        'Mohammad Shehzad':1171126,
        'Irfan Khan':1199426
    }
    # Manually add player here to map.
    ipl_name_mapper = {

        'Anukul Sudhakar Roy': 1079839,
        'Karun Nair': 398439,
        'Suryansh Shedge':1339698,
        'Shivam Singh':1380113,
        'Shashank Singh':377534,
        'Vishwapratap Singh':1354639
    }
    vb_name_mapper = {
        "Tom Loten":1146768,
        "Haseeb Hameed":632172,
        "Jack Morley":1147569,
        "Jack Blatherwick":1009835,
        "George Balderson":1146763,
        "Toby Pettman":1103905,
        "Liam Patterson-White":1023361,
        "James Pattinson":272465,
        "Daniel Moriarty":949561,
        "Harry Sullivan":1263697,
        "Dominic Leech":1146769,
        "William Luxton":1263698,
        "Josh Sullivan":1146770,
        "Tom Smith":243945,
        "Dimuth Karunaratne":227772,
        "Sam Conners":1041211,
        "Alastair Cook":11728,
        "Sam Bates":1157210,
        "Dan Douthwaite":885181,
        "Jamie Mcilroy":741831,
        "Joe Cooke":772327,
        "Dominic Sibley":519082,
        "Sam Evans":1089047,
        "Rahmanullah Gurbaz":974087,
        "Che Simmons":1263694,
        "Oliver George-Robinson":893955,
        "George Drissell":1012835,
        "Phil Salt":669365,
        "Daryl Mitchell":381743,
        "Matthew Lamb":643999,
        "Zaman Khan":1272475,
        "Mattie McKiernan":570241,
        "Saqib Mahmood":643885,
        "Tom Wood":566805,
        "Jas Singh":1185571,
        "Arafat Bhuiyan":1112524,
        "Ollie Edward Robinson":527776,
        "Michael Burgess":517549,
        "Michael Hogan": 275658,
        "Jack Brooks": 10622,
        "Chris Sole": 671823,
        "Lewis Goldsworthy": 1094990
    }
    wpl_name_mapper = {
        "Laura Kimmince" : 951163,
        "K P Navgire" : 1289983,
        "Natalie Sciver" : 515905
    }
    mlc_name_mapper = {
        "Jasdeep Singh" : 772471,
        "Akhilesh Bodugum" : 1252355
    }
    cpl_name_mapper = {

    }
    cwc_name_mapper = {
        "Zaman- Khan" : 1272475,
        "Mohammad Haris" : 1205559
    }
    abudhabit10_name_mapper = {
        "Zahir Khan" : 712219,
        "Zahoor Khan": 384525,
        "Karnal Zahid": 1249953
    }
    lpl_name_mapper = {
        "Mohammad Haris" : 1205559
    }
    hundred_name_mapper = {
        "Oliver George-Robinson" : 893955,
        "Ollie Edward Robinson" : 527776,
        "Daniel Hughes" : 571761
    }
    whundred_name_mapper = {
        "Nat Wraith" : 1032417,
        "Natalie Sciver-Brunt": 515905
    }
    bpl_name_mapper = {
        "Mohammad Nazmul Islam":446810,
        "Naim Sheikh":990081
    }


    if str2Match in bbl_name_mapper.keys() and args.ss_series_name == "bbl":
        return bbl_name_mapper[str2Match]
    elif str2Match in psl_name_mapper.keys() and args.ss_series_name == "psl":
        return psl_name_mapper[str2Match]
    elif str2Match in ipl_name_mapper.keys() and args.ss_series_name == "ipl":
        return ipl_name_mapper[str2Match]
    elif str2Match in vb_name_mapper.keys() and args.ss_series_name == "vb":
        return vb_name_mapper[str2Match]
    elif str2Match in wpl_name_mapper.keys() and args.ss_series_name == "wpl":
        return wpl_name_mapper[str2Match]
    elif str2Match in mlc_name_mapper.keys() and args.ss_series_name == "mlc":
        return mlc_name_mapper[str2Match]
    elif str2Match in cpl_name_mapper.keys() and args.ss_series_name == "cpl":
        return cpl_name_mapper[str2Match]
    elif str2Match in cwc_name_mapper.keys() and args.ss_series_name == "cwc":
        return cwc_name_mapper[str2Match]
    elif str2Match in abudhabit10_name_mapper.keys() and args.ss_series_name == "abudhabit10":
        return abudhabit10_name_mapper[str2Match]
    elif str2Match in lpl_name_mapper.keys() and args.ss_series_name == "lpl":
        return lpl_name_mapper[str2Match]
    elif str2Match in hundred_name_mapper.keys() and args.ss_series_name == "hundred":
        return hundred_name_mapper[str2Match]
    elif str2Match in whundred_name_mapper.keys() and args.ss_series_name == "whundred":
        return whundred_name_mapper[str2Match]
    elif str2Match in bpl_name_mapper.keys() and args.ss_series_name == "bpl":
        return bpl_name_mapper[str2Match]
    str2Match = str2Match
    
    
    strOptions = list(
        squad_df[squad_df.TeamName == player_team]["PlayerName"])
    if len(strOptions) == 0:
        print("Status is invalid")
        return "Status not processed"
    Ratios = process.extract(str2Match, strOptions)                ### Fuzzy wuzzy logic here
    highest = process.extractBests(str2Match, strOptions)
    if highest[0][1] == highest[1][1]:
        ids_not_mapped.append([str2Match, strOptions])
        return -1
    if int(highest[0][1]) > 75:
        h = highest[0][0]
        temp_df = squad_df[squad_df.PlayerName == h]
        if temp_df.shape[0] == 1:
            return temp_df.PlayerID.values[0]
        else:
            return -1
    else:
        return -1

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
    print(f"*****{date_info}*******")
    possible_match_date = date_info.Date.values
    # min_hours_between = 240
    min_hours_between = 72
    most_likely_match_date = None

    for date in possible_match_date:
        print(date)
        match_date = datetime.strptime(date, "%Y-%m-%d").date()
        match_time = date_info[date_info.Date == date].Time.values[0]
        match_time = datetime.strptime(match_time, "%H:%M").time()
        match_datetime = datetime.combine(match_date, match_time)
        # add timezone of the country where the game is getting played.
        if args.ss_series_name == "vb" or args.ss_series_name == "engvpak-t20" or \
            args.ss_series_name == "engvnz-wodi" or args.ss_series_name == "hundred" or \
            args.ss_series_name == "whundred" or args.ss_series_name == "ausvscot-t20" or \
            args.ss_series_name == "engvire-wodi" or args.ss_series_name == "ausveng-t20" or \
            args.ss_series_name == "ausveng-odi":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Europe/London")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "wc" or args.ss_series_name == "afgvsa-odi" or \
            args.ss_series_name == "irevsa-t20" or args.ss_series_name == "wwc-t20" or \
            args.ss_series_name == "afgvban-odi":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone("Asia/Dubai")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "bbl":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "UTC")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "psl" or args.ss_series_name == "pakvsa-wt20":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Asia/Karachi")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "ipl" or args.ss_series_name == "indvafg-t20" or \
            args.ss_series_name == "indvban-t20":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Asia/Kolkata")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "wpl" or args.ss_series_name == "indvsa-wodi" or \
            args.ss_series_name == "slvwi-t20":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Asia/Kolkata")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "mlc" or args.ss_series_name == "ausvnz-wt20":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "UTC")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "lpl" or args.ss_series_name == "wasiacup" or \
            args.ss_series_name == "slvind-t20" or args.ss_series_name == "slvind-odi":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Asia/Kolkata")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "cpl" or args.ss_series_name == "wcpl":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "UTC")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "asiacup" or args.ss_series_name == "indvnz-wodi":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Asia/Kolkata")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "cwc":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Asia/Kolkata")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "wbbl" or args.ss_series_name == "pakvzim-t20":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "UTC")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "llc":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Asia/Kolkata")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "indvaust20":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Asia/Kolkata")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "abudhabit10" or args.ss_series_name == "ilt20":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Asia/Dubai")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "indvsat20" or args.ss_series_name == "savind-odi" or \
        args.ss_series_name == "zimvind-t20" or args.ss_series_name == "sa20"or \
        args.ss_series_name == "csa-t20":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Africa/Johannesburg")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "engvwit20" or args.ss_series_name == "wiveng-odi":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "America/Port_of_Spain")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "nzvban_odi" or args.ss_series_name == "nzvpak-t20":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Pacific/Auckland")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "super-smash-men" or args.ss_series_name == "super-smash-women" \
        or args.ss_series_name == "ausvnz-wodi":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Pacific/Auckland")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "bpl":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "Asia/Dhaka")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "wivsa-t20":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "America/Port_of_Spain")), "%Y-%m-%dT%H:%M"
            )
        elif args.ss_series_name == "wct20" or args.ss_series_name == "slvwi-wodi" or \
            args.ss_series_name == "cwc-l2-odi" or args.ss_series_name == "ausvpak-odi":
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "UTC")), "%Y-%m-%dT%H:%M"
            )
        else:
            today = datetime.strftime(
                datetime.now(tz=pytz.timezone(
                    "UTC")), "%Y-%m-%dT%H:%M"
            )


        today_datetime = datetime.strptime(today, "%Y-%m-%dT%H:%M")
        hour_diff = (match_datetime - today_datetime).total_seconds() // 3600
        if team1 == "KXIP" and team2 == "SRH":
            print(hour_diff)
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
    print(date_info,most_likely_match_date)
    try:
        match_id = date_info[date_info.Date ==
                         most_likely_match_date].GameID.values[0]
    except:
        for day in date_info.Date.values:
            if day == d11_date:
                match_id = date_info[date_info.Date ==
                         d11_date].GameID.values[0]
    print(match_id)
    return match_id


def getGameID_fromdt(team1, team2, game_dt):
    """Returns Sportsseam's game id for the two team names provided

    Args:
        team1 (str): ESPN Team abbreviation
        team2 (str): ESPN Team abbreviation
        game_dt (str): Game datetime obtained from dream11 api json

    Returns:
        str: Returns SS game id from schedule.
    """
    print(f"{team1} vs {team2}")
    date_info = schedule_df[
        ((schedule_df.Team == team1) & (schedule_df.Opponent == team2))
        | ((schedule_df.Team == team2) & (schedule_df.Opponent == team1))
    ]
    possible_match_date = date_info.Date.values
    most_likely_match_date = None

    from_tz = pytz.utc
    if args.ss_series_name == "vb" or args.ss_series_name == "engvpak-t20" or \
            args.ss_series_name == "engvnz-wodi" or args.ss_series_name == "hundred" or \
            args.ss_series_name == "whundred" or args.ss_series_name == "ausvscot-t20" or \
            args.ss_series_name == "engvire-wodi" or args.ss_series_name == "ausveng-t20" or \
            args.ss_series_name == "ausveng-odi":
        to_tz = pytz.timezone("Europe/London")
    elif args.ss_series_name == "wc" or args.ss_series_name == "afgvsa-odi" or \
            args.ss_series_name == "afgvban-odi":
        to_tz = pytz.timezone("Asia/Dubai")
    elif args.ss_series_name == "bbl":
        to_tz = pytz.timezone("UTC")
    elif args.ss_series_name == "psl" or args.ss_series_name == "pakvsa-wt20":
        to_tz = pytz.timezone("Asia/Karachi")
    elif args.ss_series_name == "ipl" or args.ss_series_name == "indvafg-t20" or \
        args.ss_series_name == "indvban-t20" or args.ss_series_name == "slvwi-t20":
        to_tz = pytz.timezone("Asia/Kolkata")
    elif args.ss_series_name == "wpl" or args.ss_series_name == "indvsa-wodi":
        to_tz = pytz.timezone("Asia/Kolkata")
    elif args.ss_series_name == "mlc" or args.ss_series_name == "ausvnz-wt20":
        to_tz = pytz.timezone("UTC")
    elif args.ss_series_name == "lpl" or args.ss_series_name == "wasiacup" or \
        args.ss_series_name == "slvind-t20" or args.ss_series_name == "slvind-odi":
        to_tz = pytz.timezone("Asia/Kolkata")
    elif args.ss_series_name == "cpl" or args.ss_series_name == "wcpl" or \
        args.ss_series_name == "cwc-l2-odi" or args.ss_series_name == "pakvzim-t20":
        to_tz = pytz.timezone("UTC")
    elif args.ss_series_name == "asiacup" or args.ss_series_name == "indvnz-wodi":
        to_tz = pytz.timezone("Asia/Kolkata")
    elif args.ss_series_name == "cwc":
        to_tz = pytz.timezone("Asia/Kolkata")
    elif args.ss_series_name == "wbbl":
        to_tz = pytz.timezone("UTC")
    elif args.ss_series_name == "llc":
        to_tz = pytz.timezone("Asia/Kolkata")
    elif args.ss_series_name == "indvaust20":
        to_tz = pytz.timezone("Asia/Kolkata")
    elif args.ss_series_name == "abudhabit10" or args.ss_series_name == "ilt20" or \
        args.ss_series_name == "irevsa-t20" or args.ss_series_name == "wwc-t20":
        to_tz = pytz.timezone("Asia/Dubai")
    elif args.ss_series_name == "indvsat20" or args.ss_series_name == "savind-odi" or \
        args.ss_series_name == "zimvind-t20" or args.ss_series_name == "sa20" or\
        args.ss_series_name == "csa-t20":
        to_tz = pytz.timezone("Africa/Johannesburg")
    elif args.ss_series_name == "engvwit20":
        to_tz = pytz.timezone("America/Port_of_Spain")
    elif args.ss_series_name == "nzvban_odi" or args.ss_series_name == "nzvpak-t20" or \
        args.ss_series_name == "ausvnz-wodi":
        to_tz = pytz.timezone("Pacific/Auckland")
    elif args.ss_series_name == "super-smash-men" or args.ss_series_name == "super-smash-women":
        to_tz = pytz.timezone("Pacific/Auckland")
    elif args.ss_series_name == "bpl":
        to_tz = pytz.timezone("Asia/Dhaka")
    elif args.ss_series_name == "wivsa-t20" or args.ss_series_name == "wiveng-odi":
        to_tz = pytz.timezone("America/Port_of_Spain")
    elif args.ss_series_name == "wct20" or args.ss_series_name == "slvwi-wodi" or args.ss_series_name == "ausvpak-odi":
        to_tz = pytz.timezone("UTC")
    else:
        to_tz = pytz.timezone("UTC")

    game_dt = datetime.strptime(game_dt, "%Y-%m-%dT%H:%M:%S.000Z")
    game_dt_in_utc = game_dt.replace(tzinfo=from_tz)
    game_dt_in_tz = game_dt_in_utc.astimezone(to_tz)
    game_dt_in_str = datetime.strftime(game_dt_in_tz, "%Y-%m-%d %H:%M:%S")

    for date in possible_match_date:
        print(date)
        match_date = datetime.strptime(date, "%Y-%m-%d").date()
        match_time = date_info[date_info.Date == date].Time.values[0]
        match_time = datetime.strptime(match_time, "%H:%M").time()
        match_datetime = datetime.combine(match_date, match_time)
        print(match_datetime)
        match_datetime_in_str = datetime.strftime(
            match_datetime, "%Y-%m-%d %H:%M:%S")

        if match_datetime_in_str == game_dt_in_str:
            print("if statisfied")
            most_likely_match_date = date
            match_id = date_info[
                date_info.Date == most_likely_match_date
            ].GameID.values[0]
            print(match_id)
            return match_id
        else:
            game_date = datetime.strftime(game_dt_in_tz, "%Y-%m-%d")
            if date == game_date:
                match_id = getGameID(team1=team1, team2=team2, d11_date=game_date)
                print(match_id)
            else:
                print("date is not matching with game_date")
    return match_id


def get_api_response(request_endpoint, payload):
    conn = http.client.HTTPSConnection("www.dream11.com")
    headers = {"Content-Type": "application/json"}

    conn.request("POST", f"{request_endpoint}", payload, headers)
    res = conn.getresponse()
    if res.status != 200:
        logger.error(f"API failed for {request_endpoint}")
        # raise APINotSupportedException("API Issues")

    data = res.read()
    data_str = data.decode("utf-8")
    data_json = json.loads(data_str)
    conn.close()
    return data_json


def get_live_games_for_series(d11_series_id):
    match_ids_for_series = []

    payload = json.dumps(
        {
            "query": "query ShmeHomeSiteMatchQuery($slug: String!) { site(slug: $slug) { slug name tours { id name } matches(page: 0, statuses: [NOT_STARTED, UP_COMING], pageSize:1000) { edges { id name startTime status matchHighlight { text color } squads { id name shortName squadColorPalette flag { src type } flagWithName { src type } } tour { id name slug } } } }}",
            "variables": {"slug": "cricket"},
        }
    )

    res = get_api_response(
        request_endpoint="/graphql/query/pwa/shme-home-site-match-query",
        payload=payload,
    )
    for i in res["data"]["site"]["matches"]["edges"]:
        if i["tour"]["id"] == d11_series_id and i["status"] == "NOT_STARTED":
            match_ids_for_series.append(i["id"])
    return match_ids_for_series

###
def get_create_team_api(d11_series_id, d11_match_id):
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
    res = get_api_response(
        request_endpoint="/graphql/query/pwa/shme-create-team-query", payload=payload
    )
    return res


def get_player_data_for_match(d11_match_id, res):
    """Generate required game data from dream11 api json

    Args:
        d11_match_id (int): dream11 game id
        res (json): dream11 api json for individual game

    Returns:
        list: Returns python list containing required game data for all players.
    """
    main_list = []
    for i in res["data"]["site"]["tour"]["match"]["players"]:
        cred = i["credits"]
        d11_player_id = i["id"]
        name = i["name"]
        pos = i["type"]["name"]
        total_pts = i["points"]
        team = i["squad"]["name"]
        team_fullname = i["squad"]["fullName"]
        team_fullname = changeTeamName(team_fullname)
        try:
            match_info = i["lineupStatus"]["text"]
        except:
            match_info = None
        selection_rate = i["statistics"]["selectionRate"]
        betsmade = f"{round(selection_rate, 2)}%"
        if i["lineupOrder"] is None:
            playing_order = i["battingOrder"]
        else:
            playing_order = i["lineupOrder"]
        main_list.append(
            [
                name,
                team,
                team_fullname,
                d11_player_id,
                cred,
                pos,
                match_info,
                betsmade,
                total_pts,
                d11_match_id,
                playing_order
            ]
        )

    return main_list


def get_slate_data(res):
    game_date = res["data"]["site"]["tour"]["match"]["startTime"].split("T")[0]
    game_datetime = res["data"]["site"]["tour"]["match"]["startTime"]
    if league in utc_support:
        game_datetime = datetime.strptime(
            game_datetime.split(".")[0], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.utc).astimezone(
            tz=pytz.timezone("UTC")).strftime("%Y-%m-%dT%H:%M:%S")
    else:
        game_datetime = datetime.strptime(
            game_datetime.split(".")[0], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.utc).astimezone(
            tz=pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%dT%H:%M:%S")
    game_date = game_datetime.split("T")[0]
    slate_id = "abc"
    season = args.season  # @TODO Make this dynamic
    operator = "Dream11"
    operator_name = "DailyFantasy"
    now = datetime.now()
    operator_time = now.strftime("%Y-%m-%dT%H:%M:%S")
    operator_date = now.strftime("%Y-%m-%d")
    salary_cap = 100
    game_status = "Announced"
    d11_match_id = res["data"]["site"]["tour"]["match"]["id"]
    return [
        [
            slate_id,
            game_date,
            game_datetime,
            season,
            operator,
            operator_name,
            operator_time,
            operator_date,
            salary_cap,
            game_status,
            d11_match_id,
        ]
    ]


def get_game_slate_data(res, team_df):
    d11_team1 = changeTeamName(
        res["data"]["site"]["tour"]["match"]["squads"][0]["fullName"]
    )
    d11_team2 = changeTeamName(
        res["data"]["site"]["tour"]["match"]["squads"][1]["fullName"]
    )
    print(d11_team1, d11_team2)

    try:
        game_team1 = team_df[team_df.TeamFullName ==
                             d11_team1].TeamName.values[0]
        # print(f"{game_team1=}")
    except:
        game_team1 = None
    try:
        game_team2 = team_df[team_df.TeamFullName ==
                             d11_team2].TeamName.values[0]
        # print(f"{game_team2=}")    
    except:
        game_team2 = None

    if game_team1 is None or game_team2 is None:
        logger.info("The team full names from Dream11 are not supported")
        # raise D11TeamFullNameNotSupportedException(
        #     "The team full names from Dream11 are not supported"
        # )

    match_start_time = res["data"]["site"]["tour"]["match"]["startTime"]

    if league in utc_support:
        game_datetime = datetime.strptime(
            match_start_time.split(".")[0], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.utc).astimezone(
            tz=pytz.timezone("UTC")).strftime("%Y-%m-%dT%H:%M:%S")
    else:
        game_datetime = datetime.strptime(
            match_start_time.split(".")[0], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=pytz.utc).astimezone(
            tz=pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%dT%H:%M:%S")
    game_id = getGameID_fromdt(
        team1=game_team1, team2=game_team2, game_dt=match_start_time
    )
    d11_match_id = res["data"]["site"]["tour"]["match"]["id"]
    slate_game_id = game_id + "11"
    season = args.season
    # game_date = res["data"]["site"]["tour"]["match"]["startTime"].split("T")[0]
    game_date = game_datetime.split("T")[0]
    slate_id = "abc"
    now = datetime.now()
    operator_date = now.strftime("%Y-%m-%d")
    game_status = "Announced"
    return [
        [
            slate_game_id,
            season,
            game_date,
            slate_id,
            game_id,
            operator_date,
            game_status,
            d11_match_id,
        ]
    ]


def get_toss_info(res, team_df, schedule_df):
    """
    Function generates and returns toss info for api json passed.
    Args:
        res (_type_): The Dream 11 API json object
        team_df (_type_): Pandas df generated from Sportsseam's database (team table)
        schedule_df (_type_): Pandas df generated from Sportsseam's database (schedule table)

    Raises:
        D11TeamFullNameNotSupportedException: Raised when team names on dream 11 are not supported or are None

    Returns:
        list: Returns a list with toss data as required
    """
    team1 = res["data"]["site"]["tour"]["match"]["squads"][0]["shortName"]
    team2 = res["data"]["site"]["tour"]["match"]["squads"][1]["shortName"]
    d11_team1 = changeTeamName(
        res["data"]["site"]["tour"]["match"]["squads"][0]["fullName"]
    )
    d11_team2 = changeTeamName(
        res["data"]["site"]["tour"]["match"]["squads"][1]["fullName"]
    )
    print(d11_team1, d11_team2)
    try:
        game_team1 = team_df[team_df.TeamFullName ==
                             d11_team1].TeamName.values[0]
    except:
        game_team1 = None
    try:
        game_team2 = team_df[team_df.TeamFullName ==
                             d11_team2].TeamName.values[0]
    except:
        game_team2 = None

    if game_team1 is None or game_team2 is None:
        logger.info("The team full names from Dream11 are not supported")
        # raise D11TeamFullNameNotSupportedException(
        #     "The team full names from Dream11 are not supported"
        # )

    match_start_time = res["data"]["site"]["tour"]["match"]["startTime"]
    game_id = getGameID_fromdt(
        team1=game_team1, team2=game_team2, game_dt=match_start_time
    )
    d11_match_id = res["data"]["site"]["tour"]["match"]["id"]
    # if d11_match_id == 38160:
    #     game_id = '20220219IULQ'
    toss_result = res["data"]["site"]["tour"]["match"]["tossResult"]
    if toss_result:
        if "bat" in toss_result.lower() or "batting" in toss_result.lower():
            toss_decision = "BAT"
        else:
            toss_decision = "BOWL"
        print(toss_decision)
        toss_winner = toss_result.split(" ")[0]
        if toss_winner == team1:
            toss_winner_full_name = res["data"]["site"]["tour"]["match"]["squads"][0][
                "fullName"
            ]
        elif toss_winner == team2:
            toss_winner_full_name = res["data"]["site"]["tour"]["match"]["squads"][1][
                "fullName"
            ]
        toss_winner_full_name = changeTeamName(toss_winner_full_name)
        espn_shortname = team_df[
            team_df.TeamFullName == toss_winner_full_name
        ].TeamName.values[0]
        toss_schedule = schedule_df[schedule_df.GameID == game_id][
            ["GameID", "Date", "Team", "TeamID", "Opponent", "OpponentID"]
        ].values.tolist()[0]
        print(toss_schedule)
        toss_schedule.extend([espn_shortname, toss_decision])
        print(toss_schedule, "after")
        return toss_schedule
    else:
        toss_schedule = schedule_df[schedule_df.GameID == game_id][
            ["GameID", "Date", "Team", "TeamID", "Opponent", "OpponentID"]
        ].values.tolist()[0]
        toss_schedule.extend([None, None])
        return toss_schedule


def push_into_database(slate_game_id, database_name, table_name, df, slate_id="ABC"):
    
    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database_name}"
    )
    conn = engine.raw_connection()
    cur = conn.cursor()
    if table_name == "game_slate" or table_name == "player_slate":
        cur.execute(
            f"""DELETE FROM {table_name} WHERE "SlateGameID" = '{slate_game_id}';"""
        )
        df.head(0).to_sql(f"{table_name}", engine,
                          if_exists="append", index=False)
    if table_name == "slate":
        cur.execute(
            f"""DELETE FROM {table_name} WHERE "SlateID" = '{slate_id}';""")
        df.head(0).to_sql(f"{table_name}", engine,
                          if_exists="append", index=False)
    if table_name == "toss_info":
        cur.execute(
            f"""DELETE FROM {table_name} WHERE "GameID" = '{slate_game_id[:-2]}';"""
        )
        df.head(0).to_sql(f"{table_name}", engine,if_exists="append", index=False)

    output = io.StringIO()
    df.to_csv(output, sep="\t", header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    print(f"$$$${table_name}")
    print(f"####{output}")
    cur.copy_from(output, f"{table_name}", null="")
    conn.commit()
    conn.close()
    cur.close()


def changeGameStatus(slate_id, cur):
    cur.execute(
        f"""
        UPDATE slate SET "GameStatus" = 'Announced' WHERE "SlateID" = '{slate_id}';
    """
    )


def changeOperatorDay(slate_id, cur, op_day):
    cur.execute(
        f"""
        UPDATE slate SET "OperatorDay" = '{op_day}' WHERE "SlateID" = '{slate_id}';
    """
    )


def changeOperatorTime(slate_id, cur, op_time):
    cur.execute(
        f"""
        UPDATE slate SET "OperatorTime" = '{op_time}' WHERE "SlateID" = '{slate_id}';
    """
    )


def get_latest_game(team, season):
    """Get latest game played by team from scorecard table

    Args:
        team (_type_): Name of the team whose latest game is required
        season (_type_): Season from which data is needed

    Raises:
        Exception: Raised when query returns more than one game.

    Returns:
        str: Game ID of latest game
    """
    query = f"""
            select "GameID" from scorecard where "Season" = {season} and ("Team" = '{team}' or "Opponent" = '{team}') order by "Date" DESC limit 1;
            """
    con = connectIPLRds()
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
            select "PlayerID" from scorecard where "GameID" = '{game_id}';
            """
    con = connectIPLRds()
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


def get_impact_players(gameid, season, db, team, league, season_id):
    final_df = pd.DataFrame(columns=["PlayerID", "Team", "Sub_status"])
    # ESPNCricInfo season id for IPL 2023
    # @TODO make it dynamic
    # season_id = 1345038

    # game_ids, game_id_mapper, espn_game_ids = get_data_for_league(
    #     season_id=season_id,season=season,db=db,league=league, format="T20"
    # )

    # espn_game_id = game_id_mapper[gameid]
    # print("espn id", espn_game_id)
    # url = f"https://hs-consumer-api.espncricinfo.com/v1/pages/match/scorecard?lang=en&seriesId={season_id}&matchId={espn_game_id}"

    try:
        # hsci_auth_token = get_hsci_auth_token(url)
        agent = {"User-Agent":"Mozilla/5.0","x-hsci-auth-token":hsci_auth_token}
        response = requests.get(url,headers = agent)
        response_json = json.loads(response.text)
        response_df = pd.json_normalize(response_json["match"], record_path=["replacementPlayers"])

        for i in range(len(response_df)):
            final_df.loc[len(final_df.index)] = [
                response_df.iloc[i]["replacingPlayer.objectId"],
                response_df.iloc[i]["team.abbreviation"],"Played last match(sub_out)"]
            final_df.loc[len(final_df.index)] = [
                response_df.iloc[i]["player.objectId"],response_df.iloc[i]["team.abbreviation"],
                "Played last match(sub_in)"]
        final_df = final_df.loc[final_df.Team == team].reset_index(drop=True)
    except Exception as e:
        raise Exception("Error getting response for scorecard from espn")
    return final_df


def get_latest_game_info(game, league):
    unique_teams_in_game = (
                final_player_df[final_player_df.GameID == game].Team.unique().tolist()
    )
    print(unique_teams_in_game, "teams")
    latest_game_team1 = get_latest_game(
        team=unique_teams_in_game[0], season=args.season
    )
    latest_game_team2 = get_latest_game(
        team=unique_teams_in_game[1], season=args.season
    )
    print(latest_game_team1, latest_game_team2, "games")

    series_id = series_id_mapper.get(league)
    if series_id is not None and (latest_game_team1 and latest_game_team2 is not None):
        game_impact_players_team1 = get_impact_players(
            latest_game_team1, args.season, SERIES_DB_MAPPER[args.ss_series_name],
            unique_teams_in_game[0], league, series_id
        )
        game_impact_players_team2 = get_impact_players(
            latest_game_team2, args.season, SERIES_DB_MAPPER[args.ss_series_name],
            unique_teams_in_game[1], league, series_id
        )
    else:
        game_impact_players_team1 = pd.DataFrame()
        game_impact_players_team2 = pd.DataFrame()

    final_game_impact_players = pd.concat(
        [game_impact_players_team1, game_impact_players_team2]).reset_index(drop=True)

    return unique_teams_in_game,latest_game_team1, latest_game_team2,final_game_impact_players

def make_request(query, variables):
    conn = http.client.HTTPSConnection("www.dream11.com")
    payload = {
            "query": query,
            "variables": variables
        }
    serialized_payload = json.dumps(payload)
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6ImdqZDNkektfdW1CN0dFYllJa0RWaDBfdkt2WSJ9.eyJhdWQiOlsiYXBpLmRyZWFtMTEuY29tIiwiZ3VhcmRpYW4iXSwiZXhwIjoxNzMyNDM0OTUwLCJpYXQiOjE3MTY4ODI5NTAsImlzcyI6ImRyZWFtMTEuY29tIiwic3ViIjoiMTk4ODAxMDE0IiwiYXpwIjoiMiIsInJmdCI6IjEifQ.cVqE5CUFjtqL4pec0a5BEi9pYqA5ZCdNdCPU3QWIX3g1ChxFrj0VRhPDd9ONVVooSl4AcW_DnECmyGpp5Tdb4ab9GykBEPr9oWkmQ9SwG39dk4xKGFo03iajpdj3fR4uZz31xAY4eZI4jomSR_zfEXIayqfPzfLfT3-dM-3X8fg0sIxWuTum48hM1AKPp4VaqPvowfH1LEswejX7qnjRdTjZZlBxtjQeECU6SQtLpe_GdjlFSkQrmWq0KXdZVZ-WnPeTbG7Ttobvy09lgiGkyymEzPLxnN7P_BW5Bwaq77w42djKU4WUMMuq8wn304pQ0W58dyDilY1QE8LomwYnJA'
        }
    conn.request("POST", "/graphql/query/react-native/player-info-pre-rl", serialized_payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

def get_player_info(d11_player_id, d11_tour_id, d11_match_id):
        query = """
        query PlayerInfoPreRL($site: String!, $tourId: Int!, $teamId: Int = -1, $matchId: Int!, $id: Int!) {
            player(id: $id, teamId: $teamId, matchId: $matchId, site: $site, tourId: $tourId) {
                nationality
                birthday
            }
        }
        """
        variables = {
            "site": "cricket",
            "id": d11_player_id,
            "tourId": d11_tour_id,
            "matchId": d11_match_id,
            "teamId": -1
        }
        player_info = make_request(query, variables)
        return player_info['data']['player']['birthday'], player_info['data']['player']['nationality']

def trim_player_name(name):
    """
    Trim player names that end with -I or -II

    Args:
        name (str): Original player name

    Returns:
        str: Trimmed player name
    """
    # List of suffixes to trim
    suffixes = ['-I', '-II', '-III']

    for suffix in suffixes:
        if name.endswith(suffix):
            return name[:-len(suffix)].strip()

    return name

def get_espn_player_id(player_name):
    player_name = trim_player_name(player_name)
    conn = http.client.HTTPSConnection("sportscenter.api.espn.com")
    query = f"/apis/v1/search?query={player_name.replace(' ', '%20')}&type=player&region=in&version=679"

    conn.request("GET", query)
    res = conn.getresponse()
    data = res.read()
    espn_data = json.loads(data.decode("utf-8"))

    espn_player_ids = []

    if 'content' in espn_data and espn_data['content'] and 'items' in espn_data['content'][0]:
        items = espn_data['content'][0]['items']
        for item in items:
            # if 'Cricket' in item.get('label', ''):
            espn_player_ids.append(int(item['id']))

    if not espn_player_ids:
        print(f"No such player in espn database with name {player_name}")
    return espn_player_ids

def call_google_Api(pl_df):
    for index, player in pl_df.iterrows():
        d11_player_id = player['Dream11PlayerID']
        d11_tour_id = args.d11_series_id
        d11_match_id = player['D11_MatchID']
        birthday, nationality = get_player_info(d11_player_id, d11_tour_id, d11_match_id)
        
        pl_df.at[index, 'Birthday'] = birthday
        pl_df.at[index, 'Nationality'] = nationality
        print(f"Processing player: {player['PlayerName']}, Nationality: {nationality} for name resolving")
        if player['Nationality'] is not None:
            query = f"{player['PlayerName']} {player['Nationality']} cricketer espncrickinfo"
        else:
            query = f"{player['PlayerName']} {nationality} cricketer espncrickinfo"
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={google_api_key}&cx={google_api_cx}"
        response = requests.get(url)
        results = response.json()
        pattern = r"https://www\.espncricinfo\.com/cricketers/([^&]+)"
        for item in results.get('items', []):
            title = item['title']
            link = item['link']
            match = re.search(pattern, link)
            if match:
                print(title)
                player_id = int(match.group(1).split('-')[-1])
                print(f"Scraped ESPN player ID from Google search API for {player['PlayerName']}: {player_id}")
                pl_df.at[index, 'PlayerID'] = player_id
                break
        return pl_df

def get_espn_playerid_from_google_api(players_df):
    players_df['Birthday'] = None
    players_df['Nationality'] = None

    players_with_nan_espn_id = players_df[players_df["PlayerID"] == -1]

    for index, player in players_with_nan_espn_id.iterrows():

        d11_player_id = row['Dream11PlayerID']
        d11_tour_id = args.d11_series_id
        d11_match_id = row['D11_MatchID']

        birthday, nationality = get_player_info(d11_player_id, d11_tour_id, d11_match_id)

        players_df.at[index, 'Birthday'] = birthday
        players_df.at[index, 'Nationality'] = nationality

        print(f"Processing player: {player['PlayerName']}, Nationality: {nationality}")

        if player['Nationality'] is not None:
            query = f"{player['PlayerName']} {player['Nationality']} cricketer espncrickinfo"
        else:
            query = f"{player['PlayerName']} {nationality} cricketer espncrickinfo"

        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={google_api_key}&cx={google_api_cx}"

        response = requests.get(url)
        results = response.json()
        pattern = r"https://www\.espncricinfo\.com/cricketers/([^&]+)"

        for item in results.get('items', []):
            title = item['title']
            link = item['link']
            match = re.search(pattern, link)

            if match:
                print(title)
                player_id = int(match.group(1).split('-')[-1])
                print(f"Scraped ESPN player ID from Google search API for {player['PlayerName']}: {player_id}")
                players_df.at[index, 'PlayerID'] = player_id
                break

    return players_df

def get_espn_player_dob(espn_player_id,p_name):
    api = f"https://hs-consumer-api.espncricinfo.com/v1/pages/player/home?playerId={espn_player_id}"
    mac_generator = ESPNHMacGenerator()
    hsci_auth_token = mac_generator.generate_hmac(api)
    agent = {"User-Agent":"Mozilla/5.0",
             "x-hsci-auth-token":hsci_auth_token}
    espncrick_data = requests.get(api,headers=agent).json()
    espn_dob = espncrick_data['player']['dateOfBirth']

    if espn_dob is None:
        raise KeyError(f"Date of Birth not found for ESPN Player ID: {espn_player_id} having name {p_name}")
    if espn_dob['month'] is None or espn_dob['date'] is None:
        print(f"For player {p_name} with PlayerID {espn_player_id} espn dob has month or date as None")
        espn_dob = None
    return espn_dob

if __name__ == "__main__":
    logging.config.fileConfig(fname="./logger.config")
    logger = logging.getLogger(__name__)
    logger.info("Started...")
    # get series_id from user
    parser = argparse.ArgumentParser(
        description="This script generates Dream11 data for the series provided"
    )
    parser.add_argument(
        "--d11_series_id",
        type=int,
        help="The dream 11 series_id for which you want the data",
        required=True,
    )
    parser.add_argument(
        "--ss_series_name",
        type=str,
        help="The sportsseam series name for the series id enterted for which you want the data",
        required=True,
    )
    parser.add_argument(
        "--season",
        type=int,
        help="The current season of the league getting played",
        required=True,
        default=2022,
    )
    parser.add_argument(
        "--format",
        type=str,
        help="The format you want to filter the schedule for (e.g., ODI, T20, Test, etc.)",
        default="T20"
    )
    args = parser.parse_args()
    logger.info(
        f"Initiating Dream11 scrapper for series id {args.d11_series_id} and series name {args.ss_series_name}"
    )
    # base_url = "http://127.0.0.1:5000/"
    base_url = "https://spontasyapi.sportsseam.com"
    # if args.d11_series_id not in [1908, 2042, 1828, 2178, 2177, 2271, 2332, 2419, 2493,3094,3142,
    #                               3197,3298,3434,3475,3520,3565,3676,3729,3786,3798,3807,3824,3836,
    #                               3837,3849,3857,3853,3854,3887,3889,3900,3911,3913,3969,3959,4027,
    #                               4157,4164,4175,4169,4200,4195,4212,4218,4231,4227,4250,4258,4257,
    #                               4273,4280,3473,3480,4337,4351,4355,4363,4372,4384,4392,4395,3967,
    #                               4389,4394,4430,4427,4441,4442,4470,4493,4496,4505,4506,4514,4515]:
    #     logger.error(f"Invalid series id {args.d11_series_id}")
    #     exit(-1)
    # if args.ss_series_name.lower() not in ["ipl", "cpl", "vb", "psl", "wc", "bbl","wpl", "mlc",
    #                                        "lpl", "asiacup", "cwc", "wbbl", "llc", "indvaust20",
    #                                        "abudhabit10","indvsat20","engvwit20","savind-odi",
    #                                        "nzvban_odi", "super-smash-men", "super-smash-women",
    #                                        "sa20","indvafg-t20","nzvpak-t20","bpl","ilt20",
    #                                        "engvpak-t20","wivsa-t20","wct20","slvwi-wodi",
    #                                        "indvsa-wodi","engvnz-wodi","zimvind-t20","wasiacup",
    #                                        "hundred","whundred","slvind-t20","slvind-odi","wcpl",
    #                                        "ausvscot-t20","engvire-wodi","ausveng-t20","pakvsa-wt20",
    #                                        "afgvsa-odi","cwc-l2-odi","ausveng-odi","ausvnz-wt20",
    #                                        "csa-t20","irevsa-t20","wwc-t20","indvban-t20","slvwi-t20",
    #                                        "indvnz-wodi","wiveng-odi","ausvpak-odi","afgvban-odi"]:
    #     logger.error(f"Invalid series name {args.ss_series_name}")
    #     exit(-1)

    def connectIPLRds():
        database = SERIES_DB_MAPPER[args.ss_series_name]
        connection = psycopg2.connect(
            user=user, password=password, host=host, port=port, database=database
        )
        return connection

    def getAllPlayers():
        player_df = pd.read_sql_query(
            """select * from players;""", con=connectIPLRds())
        return player_df

    def getTeamsActive():
        url = f"{base_url}/{args.ss_series_name}/teams"
        payload = {}
        headers = {"x-aws-req": "true"}
        response = requests.request("GET", url, headers=headers, data=payload)
        team_df = pd.DataFrame(json.loads(response.text))
        return team_df[team_df.Status == "Active"]

    def getSquad(teamid):
        url = f"{base_url}/{args.ss_series_name}/squad/{args.season}/{teamid}"
        payload = {}
        headers = {"x-aws-req": "true"}
        response = requests.request("GET", url, headers=headers, data=payload)
        return pd.DataFrame(json.loads(response.text))

    def getActivePlayerInfo(season):
        player_df = pd.read_sql_query(
            f"""select * from team_squad where "Season"= {season};""",
            con=connectIPLRds(),
        )
        return player_df

    def getSchedule(season):     ### select * from schedule where season=season3
        url = f"{base_url}/{args.ss_series_name}/schedule/{season}"
        payload = {}
        headers = {"x-aws-req": "true"}
        response = requests.request("GET", url, headers=headers, data=payload)
        return pd.DataFrame(json.loads(response.text))

    def getScorecard(season):
        url = f"{base_url}/{args.ss_series_name}/scorecard/{season}"
        payload = {}
        headers = {"x-aws-req": "true"}
        response = requests.request("GET", url, headers=headers, data=payload)
        return pd.DataFrame(json.loads(response.text))

    def getActiveTeam(season):     ### select * from team_squad where season=season
        url = f"{base_url}/{args.ss_series_name}/team/{season}"
        payload = {}
        headers = {"x-aws-req": "true"}
        response = requests.request("GET", url, headers=headers, data=payload)
        return pd.DataFrame(json.loads(response.text))

    def getGameSlate(season):
        df = pd.read_sql_query(
            f"""select * from game_slate where "Season" = {season} order by "Date";""",
            con=connectIPLRds(),
        )
        return df

    def name_resloving_using_google_api(players_df):
        players_df['Birthday'] = None
        players_df['Nationality'] = None

        # Checking if same PlayerID is assigned to two or more players
        duplicate_player_id = players_df[players_df.duplicated(subset=["PlayerID", "GameID"], keep=False)]
        if duplicate_player_id.shape[0] > 1 :
            for index, player in duplicate_player_id.iterrows():
                d11_player_id = player['Dream11PlayerID']
                d11_tour_id = args.d11_series_id
                d11_match_id = player['D11_MatchID']

                birthday, nationality = get_player_info(d11_player_id, d11_tour_id, d11_match_id)
                
                players_df.at[index, 'Birthday'] = birthday
                players_df.at[index, 'Nationality'] = nationality

                print(f"Processing player: {player['PlayerName']}, Nationality: {nationality} for name resolving")

                if player['Nationality'] is not None:
                    query = f"{player['PlayerName']} {player['Nationality']} cricketer espncrickinfo"
                else:
                    query = f"{player['PlayerName']} {nationality} cricketer espncrickinfo"

                url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={google_api_key}&cx={google_api_cx}"

                response = requests.get(url)
                results = response.json()
                pattern = r"https://www\.espncricinfo\.com/cricketers/([^&]+)"

                for item in results.get('items', []):
                    title = item['title']
                    link = item['link']
                    match = re.search(pattern, link)

                    if match:
                        print(title)
                        player_id = int(match.group(1).split('-')[-1])
                        print(f"Scraped ESPN player ID from Google search API for {player['PlayerName']}: {player_id}")
                        players_df.at[index, 'PlayerID'] = player_id
                        break
        return players_df

    
    season = args.season
    league = args.ss_series_name
    schedule_df = getSchedule(season=season)
    squad_df = getActivePlayerInfo(season=season)
    existing_squad = list(squad_df["PlayerID"])
    team_df = getActiveTeam(season=season)
    all_players = getAllPlayers()
    logger.info("Got all data from API")
    match_ids_for_series = get_live_games_for_series(
        d11_series_id=args.d11_series_id)

    print(f"*****{match_ids_for_series}")
    #psl past matches
    # ids = [56882,57272,56884,56885,56886, 56887,56888, 56889, 56890,56891
    #     ,56892,56893,56894,56895,56896,56897,56898,56899,56900,56901,56902,56903,56904,56905,56906,56907,56908,56909,56910,56911] + match_ids_for_series
    #for normal operation i.e. run at 7 pm.
    #for wpl past matches
    # ids = list(range(58079,58091)) + match_ids_for_series
    # match_ids_for_series = list(range(77896,77930))
    # match_ids_for_series = [96786]
    if len(match_ids_for_series) == 0:
        raise NoLiveMatchesForSeries_Dream11(
            f"No Live matches on Dream11 for {args.d11_series_id}"
        )
    final_player_df = pd.DataFrame()
    final_slate_df = pd.DataFrame()
    final_game_slate_df = pd.DataFrame()
    final_toss_info_df = pd.DataFrame()
    main_folder = "cricket_games"
    for d11_match_id in match_ids_for_series:
        # check_if_latest_game(d11_match_id = d11_match_id)
        game_json = get_create_team_api(
            d11_series_id=args.d11_series_id, d11_match_id=d11_match_id
        )

        # Create the league folder if it doesn't exist
        league_folder = os.path.join(main_folder, args.ss_series_name.lower())
        if not os.path.exists(league_folder):
            os.makedirs(league_folder)

        with open(
            os.path.join(league_folder, f"{d11_match_id}.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(game_json, f, ensure_ascii=False, indent=4)

        fname = os.path.join(league_folder, f"{d11_match_id}.json")
        game_json = pd.read_json(fname)
            
        # Generating player data
        game_players_list = get_player_data_for_match(
            d11_match_id=d11_match_id, res=game_json
        )
        player_df = pd.DataFrame(game_players_list, columns=player_data_cols)
        player_df["Position"] = ["AR" if i ==
                                 "ALL" else i for i in player_df.Position]
        player_df["D11Name"] = player_df["PlayerName"].apply(
            lambda x: " ".join([i[0]
                               for i in x.split()[0:-1]]) + " " + x.split()[-1]
        )
        # name inconsistency between d11 and espn
        player_df["D11Name"] = player_df["D11Name"].apply(lambda x: "Y Khan" if x == "Y Khan-I" else x)
        final_player_df = pd.concat(
            [final_player_df, player_df], ignore_index=True)
        # Generating slate data
        slate_list = get_slate_data(res=game_json)
        slate_df = pd.DataFrame(slate_list, columns=slate_df_cols)
        final_slate_df = pd.concat(
            [final_slate_df, slate_df], ignore_index=True)
        # Generating game slate data
        game_slate_list = get_game_slate_data(res=game_json, team_df=team_df)
        game_slate_df = pd.DataFrame(
            game_slate_list, columns=game_slate_df_cols)
        final_game_slate_df = pd.concat(
            [final_game_slate_df, game_slate_df], ignore_index=True
        )
        toss_info = get_toss_info(
            res=game_json, team_df=team_df, schedule_df=schedule_df
        )
        if type(toss_info) == list:
            print(toss_info, "func call")
            toss_info_df = pd.DataFrame(
                [toss_info],
                columns=[
                    "GameID",
                    "Date",
                    "Team",
                    "TeamID",
                    "Opponent",
                    "OpponentID",
                    "TossWinner",
                    "TossDecision",
                ],
            )
            final_toss_info_df = pd.concat(
                [final_toss_info_df, toss_info_df], ignore_index=True
            )
        else:
            pass

    logger.info("Got all data from Dream11 API")
    final_toss_info_df.to_csv("new_toss_info.csv", index=False)
    final_game_slate_df.to_csv("new_game_slate_2.csv", index=False)
    final_slate_df.sort_values(by=["DateTime"], inplace=True)
    final_slate_df.to_csv("new_2_slate.csv", index=False)
    final_slate_df["SlateID"] = final_slate_df["D11_MatchID"].apply(
        lambda x: "".join(
            final_slate_df[final_slate_df.D11_MatchID == x]
            .DateTime.values[0]
            .split("T")[0]
            .split("-")
        )
        + "11"
        + f"_{x}"
    )
    

    final_game_slate_df["SlateID"] = final_game_slate_df["D11_MatchID"].apply(
        lambda x: final_slate_df[final_slate_df.D11_MatchID ==
                                 x].SlateID.values[0]
    )
    final_player_df["SlateID"] = final_player_df["D11_MatchID"].apply(
        lambda x: final_slate_df[final_slate_df.D11_MatchID ==
                                 x].SlateID.values[0]
    )
    final_player_df["SlateGameID"] = final_player_df["D11_MatchID"].apply(
        lambda x: final_game_slate_df[
            final_game_slate_df.D11_MatchID == x
        ].SlateGameID.values[0]
    )
    final_player_df["GameID"] = final_player_df["D11_MatchID"].apply(
        lambda x: final_game_slate_df[
            final_game_slate_df.D11_MatchID == x
        ].GameID.values[0]
    )

    final_player_df["PlayerTeam"] = final_player_df["PlayerFullTeam"].apply(
        lambda x: team_df[team_df.TeamFullName == x].TeamName.values[0]
    )
    final_player_df["PlayerID"] = final_player_df["PlayerName"].apply(
        lambda x: name_matching(
            x,
            squad_df=squad_df,
            player_team=final_player_df[
                final_player_df.PlayerName == x
            ].PlayerTeam.values[0],
            series=args.ss_series_name,
        )
    )
    final_player_df = name_resloving_using_google_api(final_player_df)
    print(ids_not_mapped)

    final_slate_df["NumberOfGames"] = 1
    final_slate_df.rename(
        columns={"OperatorDate": "OperatorDay"}, inplace=True)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    todays_date = now.strftime("%Y-%m-%d")

    final_player_df["Season"] = season
    final_player_df["TeamID"] = final_player_df["PlayerTeam"].apply(
        lambda x: team_df[team_df.TeamName == x].TeamID.values[0]
    )
    final_player_df["OperatorPlayerID"] = final_player_df["PlayerID"].apply(
        lambda x: str(x) + "11"
    )
    final_player_df["Date"] = final_player_df["SlateGameID"].apply(
        lambda x: final_game_slate_df[final_game_slate_df.SlateGameID == x].Date.values[
            0
        ]
    )
    final_player_df["UpdatedDate"] = todays_date
    final_player_df["UpdatedTime"] = current_time
    final_player_df.rename(
        columns={
            "PlayerTeam": "Team",
            "D11Name": "OperatorPlayerName",
        },
        inplace=True,
    )
    game_player_mapper = final_player_df[
        ["PlayerID", "Dream11PlayerID", "OperatorPlayerName", "Team"]
    ]
    try:
        final_player_mapper = pd.read_csv("final_player_mapper.csv")
        final_player_mapper = pd.concat(
            [final_player_mapper, game_player_mapper], ignore_index=True
        )
        final_player_mapper.drop_duplicates(inplace=True)
        final_player_mapper.to_csv("final_player_mapper.csv", index=False)
    except:
        game_player_mapper.drop_duplicates(inplace=True)
        game_player_mapper.to_csv("final_player_mapper.csv", index=False)

    final_game_slate_df = final_game_slate_df[game_slate_df_cols_final]
    final_slate_df = final_slate_df[slate_df_cols_final]
    final_slate_df["OperatorTime"] = current_time
    final_player_df.to_csv(f"new_player_slate_{args.ss_series_name}.csv", index=False)
    final_slate_df.to_csv("new_slate.csv", index=False)
    final_game_slate_df.insert(0, "League", args.ss_series_name.upper())
    final_game_slate_df.to_csv(f"new_game_slate_{args.ss_series_name}.csv", index=False)
    final_game_slate_df.drop(columns=["League"], inplace=True)

    logger.info("All data processed")

    final_player_df.sort_values(by=["Date"], inplace=True)
    latest_game = final_player_df.GameID.values[0]
    sel_by_df = final_player_df[final_player_df.GameID == latest_game]
    sel_by_df.to_csv(f"./Results/{latest_game}_{now}.csv", index=False)
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
            unique_teams_in_game,latest_game_team1, latest_game_team2,final_game_impact_players = get_latest_game_info(game, args.ss_series_name.upper())

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
                        if final_game_impact_players.shape[0] != 0 and player in final_game_impact_players.PlayerID.values.tolist():
                            final_player_df.loc[(final_player_df.GameID == game) & (final_player_df.PlayerID == player), "OperatorMatchInfo"
                                            ] = final_game_impact_players.loc[(final_game_impact_players.PlayerID) == player]["Sub_status"].values[0]
                        else:
                            final_player_df.loc[(final_player_df.GameID == game) & (final_player_df.PlayerID == player), "OperatorMatchInfo"
                                            ] = "Played last match"
                    else:
                        pass
    final_player_df.to_csv(f"modified_{args.ss_series_name}.csv", index=False)
    final_player_df["InjuryStatus"] = None
    final_player_df["InjuryInfo"] = None
    excluded = get_records_from_sheet(args.ss_series_name.upper())
    #getting the impact players when the game is announced
    _,_,_,final_game_impact_players = get_latest_game_info(game, args.ss_series_name.upper())

    for index, row in final_player_df.iterrows():
        if row["OperatorMatchInfo"] == "Played last match" or row["OperatorMatchInfo"] == "Played last match(sub_out)":
            final_player_df.loc[
                final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"
            ] = "Probable"
        #managing the status of all substitute players and who played last match after announcement.
        elif row["OperatorMatchInfo"] == "Substitute":
            if final_game_impact_players.shape[0] != 0 and row["PlayerID"] in final_game_impact_players.loc[(final_game_impact_players.PlayerID == row["PlayerID"]) & (final_game_impact_players.Sub_status == "Played last match(sub_in)")].PlayerID.values.tolist():
                final_player_df.loc[
                final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"] = "Probable(sub)"
            else:
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
        if len(excluded) > 0:
            if row["PlayerID"] in excluded.PlayerID.values.tolist():
                final_player_df.loc[
                    final_player_df.PlayerID == row["PlayerID"], "InjuryStatus"
                ] = excluded[excluded.PlayerID == row["PlayerID"]].Status.values[0]

                final_player_df.loc[final_player_df.PlayerID == row["PlayerID"], "InjuryInfo"] = excluded[
                    excluded.PlayerID == row["PlayerID"]
                ].Info.values[0]

    map_df = final_player_df[final_player_df["PlayerID"] == -1]

    if map_df.shape[0] != 0:
        map_df['Birthday'] = None
        map_df['Nationality'] = None
        for index, row in map_df.iterrows():
            d11_player_id = row['Dream11PlayerID']
            d11_tour_id = args.d11_series_id
            d11_match_id = row['D11_MatchID']
            d11_player_name = row['PlayerName']
            tname = row['Team']

            birthday, nationality = get_player_info(d11_player_id, d11_tour_id, d11_match_id)

            map_df.at[index, 'Birthday'] = birthday
            map_df.at[index, 'Nationality'] = nationality

            espn_player_ids = get_espn_player_id(d11_player_name)

            for p_id in espn_player_ids:
                try:
                    espn_dob = get_espn_player_dob(p_id,d11_player_name)

                    if birthday and espn_dob:
                        # Convert dates to a datetime object
                        d11_dob = datetime.strptime(birthday, '%b %d, %Y')  # Assuming 'Oct 07, 1983' format
                        espn_dob = datetime(espn_dob['year'], espn_dob['month'], espn_dob['date'])
                        if d11_dob == espn_dob:
                            enter_extra_data(player_id=p_id, teamname=tname, season=season, league=league.upper())
                            final_player_df.loc[
                            final_player_df['Dream11PlayerID'] == d11_player_id, 'PlayerID'] = p_id

                except KeyError as e:
                    print(f"Error retrieving DOB for ESPN Player ID {p_id}: {e}")
                    continue  # Skip to the next ESPN player ID

    # If still some players are not mapped pass them to google api flow to get espn player id
    final_player_df_updated = get_espn_playerid_from_google_api(final_player_df)
    # If still some players have -1 PlayerID
    count = len(final_player_df_updated[final_player_df_updated['PlayerID'] == -1])

    if count == 0:
         # use enter_extra_data script to push in to team_squad table
        for pid, tname in zip(final_player_df_updated['PlayerID'], final_player_df_updated['Team']):
            # check if player already exists in respective league's DB for the given team
            exist_or_not = pd.read_sql_query(f"""select * from team_squad where "PlayerID" = {int(pid)};""", con = connectIPLRds())
            if exist_or_not.empty:
                print(f"Player {pid} doesn't exist in DB, adding to team_squad for team {tname}.")
                enter_extra_data(player_id=pid, teamname=tname, season=season, league=league)
            else:
                # print(f"Player {pid} already exists in team_squad for team {tname}, season {season}.")
                pass
    else:
        print("Google Api not working to map players")

    final_player_df = final_player_df[player_data_cols_final]
    final_player_df.to_csv("new_player_slate.csv", index=False)


    conn = connectIPLRds()
    cur = conn.cursor()
    if final_toss_info_df.shape[0] > 0:
        for gid in final_toss_info_df.GameID:
            push_into_database(
                slate_game_id=gid + "11",
                database_name=SERIES_DB_MAPPER[args.ss_series_name],
                table_name="toss_info",
                df=final_toss_info_df[final_toss_info_df.GameID == gid],
            )
    for sgid in final_game_slate_df.SlateGameID.unique():
        existing_game_slate = getGameSlate(season=season)
        gs_df = final_game_slate_df[final_game_slate_df.SlateGameID == sgid]
        pl_df = final_player_df[final_player_df.SlateGameID == sgid]

        if sgid in list(existing_game_slate.SlateGameID):
            print("{IF CONDITION SATISFIED}")

            slate_id = existing_game_slate[
                existing_game_slate.SlateGameID == sgid
            ].SlateID.values[0]
            gs_df["SlateID"] = slate_id
            pl_df["SlateID"] = slate_id
            changeGameStatus(slate_id=slate_id, cur=cur)
            changeOperatorDay(slate_id=slate_id, cur=cur, op_day=todays_date)
            changeOperatorTime(slate_id=slate_id, cur=cur,
                               op_time=current_time)
            push_into_database(
                df=gs_df,
                table_name="game_slate",
                slate_game_id=sgid,
                database_name=SERIES_DB_MAPPER[args.ss_series_name],
            )
            push_into_database(
                df=pl_df,
                table_name="player_slate",
                slate_game_id=sgid,
                database_name=SERIES_DB_MAPPER[args.ss_series_name],
            )
        else:
            print("{ELSE CONDITION SATISFIED}")
            date = final_game_slate_df[
                final_game_slate_df.SlateGameID == sgid
            ].Date.values[0]
            existing_games_for_date = existing_game_slate[
                existing_game_slate.Date == date
            ].shape[0]
            slate_id = (
                "".join(date.split("-")) + "11_" +
                f"{existing_games_for_date + 1}"
            )
            gs_df["SlateID"] = slate_id
            pl_df["SlateID"] = slate_id
            sl_df = final_slate_df[final_slate_df.Date == date].head(1)
            sl_df["SlateID"] = slate_id
            push_into_database(
                df=sl_df,
                table_name="slate",
                slate_id=slate_id,
                database_name=SERIES_DB_MAPPER[args.ss_series_name],
                slate_game_id=sgid,
            )
            print(f"======={slate_id,sgid}======")

            push_into_database(
                df=gs_df,
                table_name="game_slate",
                slate_game_id=sgid,
                database_name=SERIES_DB_MAPPER[args.ss_series_name],
            )
            push_into_database(
                df=pl_df,
                table_name="player_slate",
                slate_game_id=sgid,
                database_name=SERIES_DB_MAPPER[args.ss_series_name],
            )
        time.sleep(2)
    conn.commit()
    conn.close()
    logger.info(
        f"Data pushed to DATABASE {SERIES_DB_MAPPER[args.ss_series_name]}")
