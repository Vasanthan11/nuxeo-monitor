import sqlite3
import pandas as pd


def save_ads_to_db(all_ads):

    # NO DATA
    if len(all_ads) == 0:

        print("No ads to save to database.")
        return

    # CONNECT DATABASE
    conn = sqlite3.connect("nuxeo_ads.db")

    # CREATE DATAFRAME
    df = pd.DataFrame(all_ads)

    # SAVE TABLE
    df.to_sql(
        "ads",
        conn,
        if_exists="append",
        index=False
    )

    # COMMIT CHANGES
    conn.commit()

    # CLOSE DATABASE
    conn.close()

    print("Ads saved to database.")