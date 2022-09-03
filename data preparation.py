import pandas as pd
imp_df = pd.read_csv('impression_data.csv')

# delete useless columns
del imp_df["dt"]
del imp_df["impressPosition"]
del imp_df["impressTime"]

# remove impressions that users have less than 10 times clicks
user_click = imp_df.groupby('userId')['isClick'].sum()
user_click_df = pd.DataFrame({'userId':user_click.index, 'isClick':user_click.values})
active_user = user_click_df.loc[user_click_df['isClick'] >= 10]
active_df = imp_df[imp_df['userId'].isin(active_user['userId'])]

# delete rows where mlogViewTime=0
active_df = active_df[active_df['mlogViewTime'] != 0]

# explode JSON file in 'detailMlogInfoList'
swipe_df = active_df[~active_df['detailMlogInfoList'].isna()]
swipe_df = swipe_df[swipe_df['detailMlogInfoList'] != '[]']
swipe_df = swipe_df[['userId','detailMlogInfoList']]
print(swipe_df)
swipe_df.to_csv('swipe.csv')
def CustomParser(data):
    import json
    j1 = data.replace("'", '"')
    j1 = json.loads(j1)
    return j1
swipe_df = pd.read_csv('swipe.csv',converters= {'detailMlogInfoList':CustomParser},header=0)
swipe_df = swipe_df.explode('detailMlogInfoList').reset_index(drop=True)

# delete useless columns in swipe_df and replace isZan
del swipe_df["Unnamed: 0"]
sorted_df = swipe_df['detailMlogInfoList'].apply(pd.Series)
sorted_df = sorted_df.reindex(sorted(sorted_df.columns), axis=1)
swipe_df[sorted(swipe_df['detailMlogInfoList'][0].keys())] = sorted_df
del swipe_df["detailMlogInfoList"]
del swipe_df["position"]
del swipe_df["logtime"]
swipe_df.rename(columns={"isZan":"isLike"}, inplace = True)
cols = ['isLike','isComment','isShare','isIntoPersonalHomepage','isViewComment']
swipe_df[cols] = swipe_df[cols].astype(int)
swipe_df['mlogViewTime'] = swipe_df['mlogViewTime'].astype(float)
swipe_df.describe()

# assign 0 or 1 to isClick of swipe_df
swipe_df['isClick'] = 0
for i in range(0,len(swipe_df['isClick'])):
    if swipe_df['isLike'].iloc[i]+swipe_df['isComment'].iloc[i]+swipe_df['isShare'].iloc[i]+swipe_df['isIntoPersonalHomepage'].iloc[i]+swipe_df['isViewComment'].iloc[i]>0:
        swipe_df['isClick'].iloc[i] = 1
    elif swipe_df['mlogViewTime'].iloc[i]> 25:
        swipe_df['isClick'].iloc[i] = 1
print(swipe_df.head())

# join two dataframes
del active_df["detailMlogInfoList"]
frames = [active_df, swipe_df]
df = pd.concat(frames)
df.reset_index(drop=True, inplace=True)
print('5-----------')
print(df.head(10))

df.to_csv('df.csv')