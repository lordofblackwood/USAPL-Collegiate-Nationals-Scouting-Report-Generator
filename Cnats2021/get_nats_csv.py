import gspread
import pandas as pd

gc = gspread.service_account()

#open sheet
sheet_id = "1lyTAwz_9JU-kRDNC_v7I2RpRXIrI1lXoAknRnzkAClU"
sheet = gc.open_by_key(sheet_id)

#select worksheet
worksheet = sheet.get_worksheet(0)

#download values into a dataframe
df = pd.DataFrame(worksheet.get_all_records())

#save dataframe as a csv, using the spreadsheet name
filename =  'cnat_2021.csv'
df.to_csv(filename, index=False)
