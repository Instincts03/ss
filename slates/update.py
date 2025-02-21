# importing the required libraries
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


# define the scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "sheetupdater-345419-ae12a5ce00a2.json", scope
)

def get_records_from_sheet(league):
    if league == "IPL":
        sheetName = "Player_updater"
    elif league == "VB":
        sheetName = "VB_Player_updater"
    elif league == "MLC":
        sheetName = "MLC_Player_updater"
    elif league == "LPL":
        sheetName = "LPL_Player_updater"
    elif league == "CPL":
        sheetName = "CPL_Player_updater"
    elif league == "ASIACUP":
        sheetName = "ASIACUP_Player_updater"
    elif league == "CWC":
        sheetName = "CWC_Player_updater"
    elif league == "WBBL":
        sheetName = "WBBL_Player_updater"
    elif league == "LLC":
        sheetName = "LLC_Player_updater"
    elif league == "INDVAUST20":
        sheetName = "INDVAUST20_Player_updater"
    elif league == "ABUDHABIT10":
       sheetName = "ABUDHABIT10_Player_updater"
    elif league == "BBL":
       sheetName = "BBL_Player_updater"
    elif league == "INDVSAT20":
       sheetName = "INDVSAT20_Player_updater"
    elif league == "ENGVWIT20":
       sheetName = "ENGVWIT20_Player_updater"
    elif league == "SAVIND-ODI":
       sheetName = "SAVIND_ODI_Player_updater"
    elif league == "NZVBAN_ODI":
       sheetName = "ENGVWIT20_Player_updater"
    elif league == "SUPER-SMASH-MEN" or league == "SUPER-SMASH-WOMEN":
        sheetName = "SUPER-SMASH_Player_updater"
    elif league == "SA20":
       sheetName = "SA20_Player_updater"
    elif league == "INDVAFG-T20":
       sheetName = "INDVAFG-T20_Player_updater"
    elif league == "NZVPAK-T20":
       sheetName = "NZVPAK-T20_Player_updater"
    elif league == "ILT20":
       sheetName = "ILT20_Player_updater"
    elif league == "BPL":
       sheetName = "BPL_Player_updater"
    elif league == "PSL":
       sheetName = "PSL_Player_updater"
    elif league == "WPL":
       sheetName = "WPL_Player_updater"
    elif league == "ENGVPAK-T20":
        sheetName = "ENGVPAK-T20_Player_updater"
    elif league == "WIVSA-T20":
        sheetName = "WIVSA-T20_Player_updater"
    elif league == "WCT20":
        sheetName = "WCT20_Player_updater"
    elif league == "SLVWI-WODI":
        sheetName = "SLVWI-WODI_Player_updater"
    elif league == "INDVSA-WODI":
        sheetName = "INDVSA-WODI_Player_updater"
    elif league == "ENGVNZ-WODI":
        sheetName = "ENGVNZ-WODI_Player_updater"
    elif league == "ZIMVIND-T20":
        sheetName = "ZIMVIND-T20_Player_updater"
    elif league == "WASIACUP":
        sheetName = "WASIACUP_Player_updater"
    elif league == "HUNDRED":
        sheetName = "HUNDRED_Player_updater"
    elif league == "WHUNDRED":
        sheetName = "WHUNDRED_Player_updater"
    elif league == "SLVIND-T20":
        sheetName = "SLVIND-T20_Player_updater"
    elif league == "SLVIND-ODI":
        sheetName = "SLVIND-ODI_Player_updater"
    elif league == "WCPL":
        sheetName = "WCPL_Player_updater"
    elif league == "AUSVSCOT-T20":
        sheetName = "AUSVSCOT-T20_Player_updater"
    elif league == "ENGVIRE-WODI":
        sheetName = "ENGVIRE-WODI_Player_updater"
    elif league == "AUSVENG-T20":
        sheetName = "AUSVENG-T20_Player_updater"
    elif league == "PAKVSA-WT20":
        sheetName = "PAKVSA-WT20_Player_updater"
    elif league == "AFGVSA-ODI":
        sheetName = "AFGVSA-ODI_Player_updater"
    elif league == "CWC-L2-ODI":
        sheetName = "CWC-L2-ODI_Player_updater"
    elif league == "AUSVENG-ODI":
        sheetName = "AUSVENG-ODI_Player_updater"
    elif league == "AUSVNZ-WT20":
        sheetName = "AUSVNZ-WT20_Player_updater"
    elif league == "CSA-T20":
        sheetName = "CSA-T20_Player_updater"
    elif league == "IREVSA-T20":
        sheetName = "IREVSA-T20_Player_updater"
    elif league == "WWC-T20":
        sheetName = "WWC-T20_Player_updater"
    elif league == "INDVBAN-T20":
        sheetName = "INDVBAN-T20_Player_updater"
    elif league == "SLVWI-T20":
        sheetName = "SLVWI-T20_Player_updater"
    elif league == "INDVNZ-WODI":
        sheetName = "INDVNZ-WODI_Player_updater"
    elif league == "WIVENG-ODI":
        sheetName = "WIVENG-ODI_Player_updater"
    elif league == "AUSVPAK-ODI":
        sheetName = "AUSVPAK-ODI_Player_updater"
    elif league == "AFGVBAN-ODI":
        sheetName = "AFGVBAN-ODI_Player_updater"
    else:
        sheetName = f"{league}_Player_updater"

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open(sheetName)

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)

    records_data = sheet_instance.get_all_records()
    print(records_data)
    if len(records_data) > 0:
        df = pd.DataFrame.from_dict(records_data)
        print(df)
        return df
    else:
        print("no data")
        return []
