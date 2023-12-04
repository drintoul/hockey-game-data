def get_games(**kwargs):
    """Retrieve details for each NHL game from `start` date through (including) `end` date
    """

    from datetime import datetime
    import pandas as pd
    import time

    # Fetch variables and set defaults if variable not provided
    start = kwargs.get('start', 1917)
    end = kwargs.get('end', datetime.now().year)

    # Error checking inputs
    if start < 1917:
        start = 1917

    if end > datetime.now().year:
        end = datetime.now().year

    if start > end:
        start, end = end, start

    # Build empty DataFrame
    data = pd.DataFrame()

    for year in range(start, end + 1):

        print (f'Now fetching year {year}')
        time.sleep(30) # sleep 30 seconds to not get rate limited

        try:

            # Read first table into temporary DataFrame, Concatenate with accumlation DataFrame
            dfs = pd.read_html(f'https://www.hockey-reference.com/leagues/NHL_{year}_games.html')
            df = dfs[0]
            print (df.shape)
            df = df[~data['G'].isnull()] # Don't include games which were rescheduled
            data = pd.concat([data, df], axis=0)

        except Exception as e: # if error, continue to next year
            print (e)
            continue
    
    data.columns = ['Date', 'Visitor', 'Visitor Goals', 'Home', 'Home Goals', 'Extra', 'Attendance', 'Length', 'Notes']
    return data


def ml_prep(df):
    """Prepare DataFrame for Machine Learning by datatype conversions and filtering where Attendance or Time of Game was not recorded
    Also drop games which were 'special', i.e., Outdoor or International games
    """
    
    df['Date'] = pd.to_datetime(df['Date'])

    df = df[df['Attendance'] != 'Not Recorded']
    df = df[df['Length'] != 'Not Recorded']

    try:
        df = df[df['Notes'].isnull()]
        df.drop(columns=['Notes'], inplace=True)
    except:
        pass

    # Feature engineering
    if df['Length'].dtype == 'object':
        df['Length'] = df['Length'].apply(lambda x: int(x[0])*60 + int(x[2:]))

    df['Home Win'] = df['Home Goals'] > df['Visitor Goals']
    df['Extra Time'] = df['Extra'] != 'Regular'

    df['Goal Diff'] = abs(df['Visitor Goals'] - df['Home Goals'])
    df['Total Goals'] = abs(df['Visitor Goals'] + df['Home Goals'])

    df['Close Game'] = df['Goal Diff'] < df['Goal Diff'].mean()
    df['Blowout Game'] = df['Goal Diff'] > (df['Goal Diff'].mean() + df['Goal Diff'].std())
    df['High Scoring'] = df['Total Goals'] > (df['Total Goals'].mean() + df['Total Goals'].std())
    df['Low Scoring'] = df['Total Goals'] < (df['Total Goals'].mean() - df['Total Goals'].std())
    
    df['Long Game'] = df['Length'] > (df['Length'].mean() + df['Length'].std())
    df['Short Game'] = df['Length'] < (df['Length'].mean() - df['Length'].std())

    return df
