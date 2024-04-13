import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import csv
from datetime import datetime

# Function to load CSV data
def load_csv(file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

# Function to populate dropdown menu with dates
def populate_dropdown_dates(data, dropdown):
    dates = set(datetime.strptime(row['Date'], '%m/%d/%y').date() for row in data)
    dropdown['values'] = sorted(dates)

# Function to display statistics
def display_statistics():
    start_date_str = dropdown_start_date.get()
    end_date_str = dropdown_end_date.get()

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    num_goals_between_dates = 0
    goals_by_position = {}
    goals_by_club = {}
    goals_by_type = {}
    home_goals = 0
    away_goals = 0

    for row in csv_data:
        goal_date = datetime.strptime(row['Date'], '%m/%d/%y').date()
        if start_date <= goal_date <= end_date:
            num_goals_between_dates += 1

            # Goals by position
            position = row['Playing_Position'] if row['Playing_Position'] else 'Unknown'
            goals_by_position[position] = goals_by_position.get(position, 0) + 1

            # Goals by club
            club = row['Club'] if row['Club'] else 'Unknown'
            goals_by_club[club] = goals_by_club.get(club, 0) + 1

            # Goals by type
            goal_type = row['Type'] if row['Type'] else 'Unknown'
            goals_by_type[goal_type] = goals_by_type.get(goal_type, 0) + 1

            # Home and away goals
            venue = row['Venue']
            if venue == 'H':
                home_goals += 1
            elif venue == 'A':
                away_goals += 1

    # Display statistics
    display_text.delete('1.0', tk.END)  # Clear previous text
    display_text.insert(tk.END, f"Number of goals scored between {start_date_str} and {end_date_str}: {num_goals_between_dates}\n\n")
    display_text.insert(tk.END, f"GOALS SCORED IN EACH POSITION:\n")
    for position, goals in goals_by_position.items():
        display_text.insert(tk.END, f"{position}: {goals}\n")

    display_text.insert(tk.END, f"\nGOALS SCORED FOR EACH CLUB:\n")
    for club, goals in goals_by_club.items():
        display_text.insert(tk.END, f"{club}: {goals}\n")

    display_text.insert(tk.END, f"\nGOALS SCORED IN EACH TYPE:\n")
    for goal_type, goals in goals_by_type.items():
        display_text.insert(tk.END, f"{goal_type}: {goals}\n")

    display_text.insert(tk.END, f"\nHome Goals: {home_goals}\n")
    display_text.insert(tk.END, f"Away Goals: {away_goals}\n")

# Load CSV data
csv_data = load_csv('/Users/vishalkannan/Downloads/fbstats.csv')

# Create GUI
root = tk.Tk()
root.title('Cristiano Ronaldo Stats')

# Set window size and position
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry(f"{window_width}x{window_height}+0+0")

# Load and resize background image
bg_image = Image.open("/Users/vishalkannan/Downloads/Legends-Profile_Cristiano-Ronaldo1523460877263.jpg")
bg_image = bg_image.resize((window_width, window_height), Image.ANTIALIAS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Add background image to Label
background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create and populate dropdown menu with start date
start_date_label = tk.Label(root, text="Select Start Date (YYYY-MM-DD):", bg='red4', fg='white', font=("Arial", 14))
start_date_label.pack(pady=5)
dropdown_start_date = ttk.Combobox(root, state="readonly", font=("Arial", 14))
populate_dropdown_dates(csv_data, dropdown_start_date)
dropdown_start_date.pack(pady=5)

# Create and populate dropdown menu with end date
end_date_label = tk.Label(root, text="Select End Date (YYYY-MM-DD):", bg='red4', fg='white', font=("Arial", 14))
end_date_label.pack(pady=5)
dropdown_end_date = ttk.Combobox(root, state="readonly", font=("Arial", 14))
populate_dropdown_dates(csv_data, dropdown_end_date)
dropdown_end_date.pack(pady=5)

# Button to display statistics
display_button = tk.Button(root, text="Display Statistics", command=display_statistics, bg="blue", fg="white", font=("Arial", 14))
display_button.pack(pady=30)

# Text widget to display statistics
display_text = tk.Text(root, height=50, width=50, font=("Arial", 20))
display_text.pack(pady=10)

root.mainloop()
