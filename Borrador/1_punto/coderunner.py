import pandas as pd

#Merge 3 dataframes into 1                
df = pd.read_csv("data\\User_track_data.csv")
df1 = pd.read_csv("data\\User_track_data_2.csv")
m1 = pd.merge(df,df1,how="outer") # m1 = df+df1
df2 = pd.read_csv("data\\User_track_data_3.csv")
mega_df = pd.merge(m1,df2,how="outer") # mega_df = df2+m1

print(mega_df.tail(5))
