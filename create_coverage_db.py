import sqlite3
from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parent

candidate_plans = [
    root / 'data' / 'plans.csv',
    root / 'plans.csv',
    root / 'plans_cleaned.csv',
]
candidate_claims = [
    root / 'data' / 'claims.csv',
    root / 'claims.csv',
    root / 'claims_cleaned.csv',
]

def resolve_existing(path_candidates):
    for path in path_candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"No input CSV found. Checked: {', '.join(str(p) for p in path_candidates)}")

plans_path = resolve_existing(candidate_plans)
claims_path = resolve_existing(candidate_claims)
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
