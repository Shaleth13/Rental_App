import sqlite3
import pandas as pd
from nl_to_sql_parser import llm_like_nl_to_sql

conn = sqlite3.connect("../data/real_estate.db")

queries = [
    "Show all available apartments in Bradford with 2 bedrooms under 3000 rent",
    "What’s the occupancy rate of properties in Bradford last quarter?",
    "Who are the top 10 tenants by total rent paid?",
    "What’s the average rating of apartments vs houses?",
    "Which landlords generated the most revenue this year?",
    "List all currently available 2BHKs under $2500 in London."
]

for q in queries:
    sql_query = llm_like_nl_to_sql(q)
    print(f"\nNL Query: {q}\nGenerated SQL:\n{sql_query}\n")
    df = pd.read_sql_query(sql_query, conn)
    print("Results:\n", df)

conn.close()
