import pandas as pd
import tkinter as tk
from tkinter import ttk
import mysql.connector

def filter_data():
    club = club_var.get()
    playing_position = position_var.get()
    match_type = type_var.get()
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    
    query = "SELECT * FROM your_table WHERE 1=1"
    conditions = []
    if club:
        conditions.append(f"Club = '{club}'")
    if playing_position:
        conditions.append(f"Playing_Position = '{playing_position}'")
    if match_type:
        conditions.append(f"Type = '{match_type}'")
    if start_date and end_date:
        conditions.append(f"Date BETWEEN '{start_date}' AND '{end_date}'")
    
    if conditions:
        query += " AND " + " AND ".join(conditions)
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    filtered_df = pd.DataFrame(results, columns=['Date', 'Club', 'Playing_Position', 'Type'])
        
    goals_scored = filtered_df['Type'].count()
    result_label.config(text=f"Goals Scored: {goals_scored}")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="fbstats"
)

cursor = db.cursor()

root = tk.Tk()
root.title("Goals Scored Filter")

clubs = df['Club'].unique()
club_var = tk.StringVar()
club_label = ttk.Label(root, text="Club:")
club_label.grid(row=0, column=0)
club_dropdown = ttk.Combobox(root, textvariable=club_var, values=clubs)
club_dropdown.grid(row=0, column=1)

positions = df['Playing_Position'].unique()
position_var = tk.StringVar()
position_label = ttk.Label(root, text="Position:")
position_label.grid(row=1, column=0)
position_dropdown = ttk.Combobox(root, textvariable=position_var, values=positions)
position_dropdown.grid(row=1, column=1)

match_types = df['Type'].unique()
type_var = tk.StringVar()
type_label = ttk.Label(root, text="Match Type:")
type_label.grid(row=2, column=0)
type_dropdown = ttk.Combobox(root, textvariable=type_var, values=match_types)
type_dropdown.grid(row=2, column=1)

start_date_label = ttk.Label(root, text="Start Date (YYYY-MM-DD):")
start_date_label.grid(row=3, column=0)
start_date_entry = ttk.Entry(root)
start_date_entry.grid(row=3, column=1)

end_date_label = ttk.Label(root, text="End Date (YYYY-MM-DD):")
end_date_label.grid(row=4, column=0)
end_date_entry = ttk.Entry(root)
end_date_entry.grid(row=4, column=1)

filter_button = ttk.Button(root, text="Filter", command=filter_data)
filter_button.grid(row=5, column=0, columnspan=2)

result_label = ttk.Label(root, text="")
result_label.grid(row=6, column=0, columnspan=2)

root.mainloop()

cursor.close()
db.close()
