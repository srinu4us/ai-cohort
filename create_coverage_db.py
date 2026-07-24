import sqlite3
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parent
plans_path = root / 'Plans_cleaned.csv'
claims_path = root / 'Data' / 'Claims_cleaned.csv'
db_path = root / 'coverage.db'

if db_path.exists():
    db_path.unlink()

plans = pd.read_csv(plans_path)
claims = pd.read_csv(claims_path)

conn = sqlite3.connect(db_path)
plans.to_sql('plans', conn, if_exists='replace', index=False)
claims.to_sql('claims', conn, if_exists='replace', index=False)
conn.commit()

print('created', db_path)
print(conn.execute("select name from sqlite_master where type='table' order by name").fetchall())
print(conn.execute('select count(*) from plans').fetchone())
print(conn.execute('select count(*) from claims').fetchone())

conn.close()
