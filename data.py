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
            data = pd.concat([data, df], axis=0)

        except Exception as e: # if error, continue to next year
            print (e)
            continue

    return data
