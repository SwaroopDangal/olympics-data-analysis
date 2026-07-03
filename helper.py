from typing_extensions import final

import numpy as np

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('region', as_index=False).sum()[['region','Gold','Silver','Bronze']].sort_values('Gold',ascending=False)
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze'] 

    medal_tally['Gold'] =medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    return medal_tally.reset_index(drop=True)

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def fetch_medal_tally(df,year, country):
    base_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

    if year == 'Overall' and country == 'Overall':
        x = base_df.groupby('region', as_index=False).sum()[['region','Gold','Silver','Bronze']].sort_values('Gold',ascending=False)
    elif year == 'Overall' and country != 'Overall':
        temp_df = base_df[base_df['region'] == country]
        x = temp_df.groupby('Year', as_index=False).sum()[['Year','Gold','Silver','Bronze']].sort_values('Year',ascending=True)
    elif year != 'Overall' and country == 'Overall':
        temp_df = base_df[base_df['Year'] == int(year)]
        x = temp_df.groupby('region', as_index=False).sum()[['region','Gold','Silver','Bronze']].sort_values('Gold',ascending=False)
    else:
        temp_df = base_df[(base_df['Year'] == int(year)) & (base_df['region'] == country)]
        x = temp_df.groupby('region', as_index=False).sum()[['region','Gold','Silver','Bronze']].sort_values('Gold',ascending=False)
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x.reset_index(drop=True)

def data_over_time(df,col):
    data_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    return data_over_time

def most_successfull_athletes(df,sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    
    x= temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name').rename(columns={'count':'No. of medals','Sport':'Sport','region':'Nation'})

    return x.reset_index(drop=True)

def year_wise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index().sort_values('Year').reset_index()

    return final_df


def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int')

    return pt

def most_successfull_athletes_country(df,country):
    temp_df = df.dropna(subset=['Medal'])

    
    temp_df = temp_df[temp_df['region'] == country]
    
    x= temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport']].drop_duplicates('Name').rename(columns={'count':'No. of medals','Sport':'Sport','region':'Nation'})

    return x.reset_index(drop=True)


def weight_height_scatter(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df
    

def men_v_women(df):
    athlete_df = df.drop_duplicates(subset=['Name','region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women,on='Year')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    return final