# import os
# # os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "AF726FB2-01B3-483C-9449-C6EB84867B80"'""")
# # or: os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "Test press keys"'""")
# os.system("""osascript -e 'tell application "Keyboard Maestro Engine" to do script "AF726FB2-01B3-483C-9449-C6EB84867B80" with parameter "1234"'""")


# from ftplib import FTP
# from pathlib import Path
#
# file_path = Path('path')
#
# with FTP('host', 'user', 'pass') as ftp, open(file_path, 'rb') as file:
#     ftp.storbinary(f'STOR {file_path.name}', file)
#     print("File uploaded successfully!")
#

# ----------------------------------------------
# ----------------------------------------------

import gspread
import pandas as pd
import argparse

from datetime import datetime, timedelta

# datetime object containing current date and time
now = datetime.now()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scripts parameters')
    parser.add_argument('--minutes', required=True, type=int)
    parser.add_argument('--code', required=True, type=int)
    args = parser.parse_args()

    # print("now =", now)

    schedule_time = now + timedelta(minutes=args.minutes)
    # dd/mm/YY H:M:S
    # Time-string:
    time_string = "%Y-%m-%dT%H:%M:%S"
    schedule_time_str = schedule_time.strftime(time_string)
    # schedule_time_str = schedule_time.strftime("%d/%m/%Y %H:%M:%S")
# "YYYY-MM-DDTHH:mm:ss.sssZ"

    now_str = now.strftime(time_string)
    print("Scheduled time for releasing code:", schedule_time_str)

    # date = '2021-05-21 11:22:03'
    # datem = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    # print(datem.day)  # 25
    # print(datem.month)  # 5
    # print(datem.year)  # 2021
    # print(datem.hour)  # 11
    # print(datem.minute)  # 22
    # print(datem.second)  # 3

    gc = gspread.oauth()

    sh = gc.open("screen_time_codes").sheet1

    dataframe = pd.DataFrame(sh.get_all_records())
    dataframe.loc[len(dataframe.index)] = [args.code, schedule_time_str, "", now_str, ""]

    # print(dataframe)
    sh.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())
    print("Spreadsheet updated!")

