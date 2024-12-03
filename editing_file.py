#important libraries
import tkinter as tk #to create windows
from tkinter import ttk, messagebox # For special widgets and pop-up messages
from ttkwidgets.autocomplete import AutocompleteCombobox # To show suggestions when typing
from datetime import datetime # To get dates and times
import random #for random time
from PIL import Image, ImageTk #for image handling
from reportlab.lib.pagesizes import letter #for making pdf pages
import io #to handle files

import os
current_dir = os.path.dirname(os.path.abspath(__file__))

from reportlab.pdfgen import canvas as pdf_canvas
from data import data # type: ignore #this has all travel information

flight_routes = {"Aberdeen": {
        "Belfast": ["Air UK", "FlyBe"],
        "Birmingham": ["Loganair", "FlyBe"],
        "Bristol": ["Eastern Airways"],
        "Cardiff": ["Eastern Airways"],
        "Edinburgh": ["British Airways"],
        "Glasgow": ["FlyBe"],
        "London": ["British Airways", "Loganair"],
        "Manchester": ["FlyBe"]},
    "Belfast": {
        "Aberdeen": ["Air UK", "FlyBe"],
        "Birmingham": ["EasyJet", "FlyBe"],
        "Bristol": ["EasyJet"],
        "Cardiff": ["Eastern Airways"],
        "Edinburgh": ["EasyJet"],
        "Glasgow": ["British Airways"],
        "Liverpool": ["FlyBe"],
        "London": ["British Airways", "EasyJet"],
        "Manchester": ["EasyJet", "FlyBe"],
        "Newcastle upon Tyne": ["FlyBe"]},
    "Birmingham": {
        "Aberdeen": ["Loganair", "FlyBe"],
        "Belfast": ["EasyJet", "FlyBe"],
        "Edinburgh": ["Loganair", "British Airways"],
        "Glasgow": ["EasyJet", "FlyBe"],
        "London": ["British Airways"],
        "Manchester": ["FlyBe"],
        "Newcastle upon Tyne": ["EasyJet"]},
    "Bristol": {
        "Aberdeen": ["Eastern Airways"],
        "Belfast": ["EasyJet"],
        "Edinburgh": ["EasyJet"],
        "Glasgow": ["FlyBe"],
        "London": ["British Airways"],
        "Manchester": ["EasyJet"]},
    "Cardiff": {
        "Aberdeen": ["Eastern Airways"],
        "Belfast": ["Eastern Airways"],
        "Edinburgh": ["British Airways"],
        "Glasgow": ["FlyBe"],
        "London": ["British Airways"],
        "Manchester": ["EasyJet"]},
    "Edinburgh": {
        "Aberdeen": ["British Airways"],
        "Belfast": ["EasyJet"],
        "Birmingham": ["Loganair", "British Airways"],
        "Bristol": ["EasyJet"],
        "Cardiff": ["British Airways"],
        "Glasgow": ["FlyBe"],
        "London": ["British Airways", "Loganair"],
        "Manchester": ["FlyBe"],
        "Newcastle upon Tyne": ["EasyJet"]},
    "Glasgow": {
        "Aberdeen": ["FlyBe"],
        "Belfast": ["British Airways"],
        "Birmingham": ["EasyJet", "FlyBe"],
        "Bristol": ["FlyBe"],
        "Cardiff": ["FlyBe"],
        "Edinburgh": ["FlyBe"],
        "London": ["British Airways"],
        "Manchester": ["EasyJet"]},
    "Leeds": {
        "Belfast": ["FlyBe"],
        "London": ["British Airways"]},
    "Liverpool": {
        "Belfast": ["FlyBe"],
        "London": ["British Airways"]},
    "London": {
        "Aberdeen": ["British Airways", "Loganair"],
        "Belfast": ["British Airways", "EasyJet"],
        "Birmingham": ["British Airways"],
        "Bristol": ["British Airways"],
        "Cardiff": ["British Airways"],
        "Edinburgh": ["British Airways", "Loganair"],
        "Glasgow": ["British Airways"],
        "Leeds": ["British Airways"],
        "Liverpool": ["British Airways"],
        "Manchester": ["FlyBe", "British Airways"],
        "Newcastle upon Tyne": ["FlyBe"]},
    "Manchester": {
        "Aberdeen": ["FlyBe"],
        "Belfast": ["EasyJet", "FlyBe"],
        "Birmingham": ["FlyBe"],
        "Bristol": ["EasyJet"],
        "Cardiff": ["EasyJet"],
        "Edinburgh": ["FlyBe"],
        "Glasgow": ["EasyJet"],
        "London": ["FlyBe", "British Airways"],
        "Newcastle upon Tyne": ["EasyJet"]},
    "Newcastle upon Tyne": {
        "Belfast": ["FlyBe"],
        "Birmingham": ["EasyJet"],
        "Edinburgh": ["EasyJet"],
        "London": ["FlyBe"],
        "Manchester": ["EasyJet"]}}

train_routes = {"London": {
        "Manchester": ["Avanti West Coast", "CrossCountry"],
        "Birmingham": ["Avanti West Coast", "London Northwestern Railway"],
        "Edinburgh": ["LNER", "Avanti West Coast"],
        "Leeds": ["LNER", "Northern Trains"],
        "Bristol": ["Great Western Railway "],
        "Cardiff": ["Great Western Railway "],
        "Glasgow": ["Avanti West Coast", "LNER"],
        "Liverpool": ["Avanti West Coast", "London Northwestern Railway"],
        "Newcastle upon Tyne": ["LNER"],
    },
    "Manchester": {
        "London": ["Avanti West Coast", "CrossCountry"],
        "Edinburgh": ["TransPennine Express"],
        "Leeds": ["TransPennine Express", "Northern Trains"],
        "Birmingham": ["CrossCountry"],
        "Liverpool": ["Northern Trains", "TransPennine Express"],
        "Newcastle upon Tyne": ["CrossCountry"],
        "Glasgow": ["TransPennine Express"],
    },
    "Edinburgh": {
        "London": ["LNER", "Avanti West Coast"],
        "Manchester": ["TransPennine Express"],
        "Newcastle upon Tyne": ["LNER", "CrossCountry"],
        "Glasgow": ["ScotRail"],
        "Birmingham": ["CrossCountry"],
    },
    "Birmingham": {
        "London": ["Avanti West Coast", "London Northwestern Railway"],
        "Manchester": ["CrossCountry"],
        "Glasgow": ["Avanti West Coast"],
        "Edinburgh": ["CrossCountry"],
        "Cardiff": ["CrossCountry"],
        "Bristol": ["CrossCountry"],
        "Leeds": ["CrossCountry"],
    },
    "Leeds": {
        "London": ["LNER", "Northern Trains"],
        "Manchester": ["TransPennine Express", "Northern Trains"],
        "Edinburgh": ["LNER"],
        "Birmingham": ["CrossCountry"],
        "Newcastle upon Tyne": ["LNER"],
    },
    "Bristol": {
        "London": ["Great Western Railway "],
        "Cardiff": ["Great Western Railway "],
        "Birmingham": ["CrossCountry"],
        "Manchester": ["CrossCountry"],
        "Leeds": ["CrossCountry"],
    },
    "Cardiff": {
        "London": ["Great Western Railway "],
        "Bristol": ["Great Western Railway "],
        "Birmingham": ["CrossCountry"],
        "Manchester": ["CrossCountry"],
    },
    "Glasgow": {
        "London": ["Avanti West Coast", "LNER"],
        "Manchester": ["TransPennine Express"],
        "Edinburgh": ["ScotRail"],
        "Birmingham": ["Avanti West Coast"],
        "Newcastle upon Tyne": ["LNER"],
    },
    "Newcastle upon Tyne": {
        "London": ["LNER"],
        "Manchester": ["CrossCountry"],
        "Edinburgh": ["LNER", "CrossCountry"],
        "Glasgow": ["LNER"],
        "Leeds": ["LNER"],
    },
    "Liverpool": {
        "London": ["Avanti West Coast"],
        "Manchester": ["Northern Trains", "TransPennine Express"],
        "Birmingham": ["London Northwestern Railway"],
    }
}

coach_routes = {
    "London": {
        "Manchester": ["National Express", "Megabus"],
        "Birmingham": ["National Express", "FlixBus"],
        "Edinburgh": ["National Express", "Megabus"],
        "Leeds": ["Megabus", "FlixBus"],
        "Bristol": ["National Express", "FlixBus"],
        "Cardiff": ["National Express", "Megabus"],
        "Glasgow": ["National Express"],
        "Liverpool": ["National Express", "Megabus"],
        "Newcastle upon Tyne": ["Megabus", "National Express"],
    },
    "Manchester": {
        "London": ["National Express", "Megabus"],
        "Edinburgh": ["Megabus"],
        "Leeds": ["National Express", "Megabus"],
        "Birmingham": ["FlixBus", "National Express"],
        "Liverpool": ["National Express"],
        "Newcastle upon Tyne": ["Megabus"],
        "Glasgow": ["National Express"],
    },
    "Edinburgh": {
        "London": ["National Express", "Megabus"],
        "Manchester": ["Megabus"],
        "Newcastle upon Tyne": ["National Express"],
        "Glasgow": ["Megabus", "National Express"],
        "Birmingham": ["National Express"],
    },
    "Birmingham": {
        "London": ["National Express", "FlixBus"],
        "Manchester": ["FlixBus", "National Express"],
        "Glasgow": ["National Express"],
        "Edinburgh": ["National Express"],
        "Cardiff": ["National Express"],
        "Bristol": ["FlixBus"],
        "Leeds": ["Megabus"],
    },
    "Leeds": {
        "London": ["Megabus", "FlixBus"],
        "Manchester": ["National Express", "Megabus"],
        "Edinburgh": ["National Express"],
        "Birmingham": ["Megabus"],
        "Newcastle upon Tyne": ["National Express"],
    },
    "Bristol": {
        "London": ["National Express", "FlixBus"],
        "Cardiff": ["National Express"],
        "Birmingham": ["FlixBus"],
        "Manchester": ["National Express"],
    },
    "Cardiff": {
        "London": ["National Express", "Megabus"],
        "Bristol": ["National Express"],
        "Birmingham": ["National Express"],
        "Manchester": ["National Express"],
    },
    "Glasgow": {
        "London": ["National Express"],
        "Manchester": ["National Express"],
        "Edinburgh": ["Megabus", "National Express"],
        "Birmingham": ["National Express"],
        "Newcastle upon Tyne": ["National Express"],
    },
    "Newcastle upon Tyne": {
        "London": ["Megabus", "National Express"],
        "Manchester": ["Megabus"],
        "Edinburgh": ["National Express"],
        "Glasgow": ["National Express"],
        "Leeds": ["National Express"],
    },
    "Liverpool": {
        "London": ["National Express", "Megabus"],
        "Manchester": ["National Express"],
        "Birmingham": ["National Express"],
    },
}

airport_names = {
    "Aberdeen": "Aberdeen International Airport ",
    "Belfast": "Belfast International Airport ",
    "Birmingham": "Birmingham Airport ",
    "Bristol": "Bristol Airport ",
    "Cardiff": "Cardiff Airport ",
    "Edinburgh": "Edinburgh Airport ",
    "Glasgow": "Glasgow Airport ",
    "Leeds": "Leeds Bradford Airport ",
    "Liverpool": "Liverpool John Lennon Airport ",
    "London": "London Heathrow Airport ",
    "Manchester": "Manchester Airport ",
    "Newcastle upon Tyne": "Newcastle International Airport "
}

train_stations = {
    "London": "London King's Cross Station",
    "Manchester": "Manchester Piccadilly Station",
    "Birmingham": "Birmingham New Street Station",
    "Edinburgh": "Edinburgh Waverley Station",
    "Leeds": "Leeds Railway Station",
    "Bristol": "Bristol Temple Meads Station",
    "Cardiff": "Cardiff Central Station",
    "Glasgow": "Glasgow Central Station",
    "Newcastle upon Tyne": "Newcastle Central Station",
    "Liverpool": "Liverpool Lime Street Station",
    "Aberdeen": "Aberdeen Railway Station",
    "Belfast": "Belfast Lanyon Place Station",
    "Bath": "Bath Spa Station",
    "Brighton and Hove": "Brighton Railway Station",
    "Cambridge": "Cambridge Railway Station",
    "Coventry": "Coventry Railway Station",
    "Derby": "Derby Railway Station",
    "Derry": "Londonderry Railway Station",
    "Dundee": "Dundee Railway Station",
    "Exeter": "Exeter St Davids Station",
    "Inverness": "Inverness Railway Station",
    "Leicester": "Leicester Railway Station",
    "Norwich": "Norwich Railway Station",
    "Nottingham": "Nottingham Railway Station",
    "Oxford": "Oxford Railway Station",
    "Peterborough": "Peterborough Railway Station",
    "Plymouth": "Plymouth Railway Station",
    "Portsmouth": "Portsmouth & Southsea Station",
    "Sheffield": "Sheffield Railway Station",
    "Southampton": "Southampton Central Station",
    "Stoke-on-Trent": "Stoke-on-Trent Railway Station",
    "Sunderland": "Sunderland Railway Station",
    "Wolverhampton": "Wolverhampton Railway Station",
    "York": "York Railway Station"
}

coach_stops = {
    "London": "Victoria Coach Station",
    "Manchester": "Manchester Chorlton Street Coach Station",
    "Birmingham": "Birmingham Coach Station (Digbeth)",
    "Edinburgh": "Edinburgh Bus Station",
    "Leeds": "Leeds Coach Station",
    "Bristol": "Bristol Bus and Coach Station",
    "Cardiff": "Cardiff Coach Station",
    "Glasgow": "Buchanan Bus Station",
    "Newcastle upon Tyne": "Newcastle Coach Station",
    "Liverpool": "Liverpool One Bus Station",
    "Aberdeen": "Aberdeen Bus Station",
    "Belfast": "Belfast Europa Bus Centre",
    "Brighton and Hove": "Pool Valley Coach Station",
    "Bath": "Bath Bus Station",
    "Cambridge": "Cambridge Parkside Coach Stop",
    "Coventry": "Coventry Pool Meadow Bus Station",
    "Derby": "Derby Bus Station",
    "Derry": "Foyle Street Bus Station",
    "Dundee": "Dundee Seagate Bus Station",
    "Exeter": "Exeter Bus Station",
    "Inverness": "Inverness Bus Station",
    "Leicester": "Leicester St Margaret's Bus Station",
    "Norwich": "Norwich Bus Station",
    "Nottingham": "Nottingham Broadmarsh Bus Station",
    "Oxford": "Oxford Gloucester Green Bus Station",
    "Peterborough": "Peterborough Queensgate Bus Station",
    "Plymouth": "Plymouth Coach Station",
    "Portsmouth": "Portsmouth Coach Station",
    "Sheffield": "Sheffield Interchange",
    "Southampton": "Southampton Coach Station",
    "Stoke-on-Trent": "Stoke-on-Trent Bus Station",
    "Sunderland": "Park Lane Interchange",
    "Wolverhampton": "Wolverhampton Bus Station",
    "York": "York Station Coach Stop",
}

cities_in_uk = ["Aberdeen", "Bath", "Belfast", "Birmingham", "Brighton and Hove", 
    "Bristol", "Cambridge", "Cardiff", "Coventry", "Derby", "Derry", 
    "Dundee", "Edinburgh", "Exeter", "Glasgow", "Inverness", "Leeds", 
    "Leicester", "Liverpool", "London", "Manchester", "Newcastle upon Tyne", 
    "Norwich", "Nottingham", "Oxford", "Peterborough", "Plymouth", 
    "Portsmouth", "Sheffield", "Southampton", "Stoke-on-Trent", 
    "Sunderland", "Wolverhampton", "York"]

def start_application():
    """Start the main application."""
    try:
        global root
        root.destroy()  # Close the welcome window
        open_main_application()  # Open the main application
    except Exception as e:
        messagebox.showerror("Error Starting Application", f"An error occurred: {str(e)}")
        # Log the error
        with open("error_log.txt", "a") as error_file:
            error_file.write(f"{datetime.now()} - start_application: {str(e)}\n")

def open_main_application():
    try: #main application window
        def plan_trip():
            from_city = departure_city.get() #where u want to start
            to_city = destination_city.get() #where u want to go

            if not from_city or not to_city: #if nothing is chosen
                messagebox.showwarning("Invalid Selection", "Please select both a departure and arrival city.")
                return

            if from_city == to_city: #if start and end are the same 
                messagebox.showwarning("Invalid Selection", "Departure and arrival cities cannot be the same! ⚠️")
                return

            main_app.destroy() #close the window
            travel_method(from_city, to_city) #ask how they want to travel

        def update_destination_options(event):
            global selected_method
            from_city = departure_city.get()
            # Update the cities you can go to based on the selected travel method
            to_menu.config(completevalues=cities_in_uk) #show all citites

            # Show only routes for the selected travel method
            if selected_method.get() == "Flight ✈️" and from_city in flight_routes:
                to_menu.config(completevalues=list(flight_routes[from_city].keys()))
            elif selected_method.get() == "Train 🚅" and from_city in train_routes:
                to_menu.config(completevalues=list(train_routes[from_city].keys()))
            elif selected_method.get() == "Coach 🚌" and from_city in coach_routes:
                to_menu.config(completevalues=list(coach_routes[from_city].keys()))

        def create_window(title, size, bg_color): #create the application window
            app = tk.Tk() #new window
            app.title(title) #window name 
            app.geometry("2000x1000") #set size
            app.configure(bg=bg_color) #set background color
            return app

        main_app = create_window("Travel Planner", "2000x1000", "lightblue") #create the window

        departure_city = tk.StringVar() #pick the departure city
        destination_city = tk.StringVar() #pick the arrival city

        #label for title
        label = ttk.Label(
            main_app,
            text="Plan Your Journey!", #title text
            font=("Time New Roman", 40, "bold"),
            background="lightblue",
    )
        label.grid(row=0, column=0, columnspan=2, pady=(150, 80))

        #label for "from" field
        from_label = ttk.Label(
            main_app,
            text="From 🏖️",
            font=("Time New Roman", 30, "bold"),
            background="lightblue",
    )
        from_label.grid(row=1, column=0, sticky="e", padx=30, pady=(20, 40))

        #dropdown for "from" field
        from_menu = AutocompleteCombobox(
            main_app,
            textvariable=departure_city,
            completevalues=cities_in_uk,
            width=25,  # Increased width
            font=("Time New Roman", 22, "bold"),
    )
        from_menu.grid(row=1, column=1, sticky="w", padx=30, pady=(20, 40))

        #label for to field
        to_label = ttk.Label(
            main_app,
            text="To 🌍",
            font=("Time New Roman", 30, "bold"), 
            background="lightblue",
    )
        to_label.grid(row=2, column=0, sticky="e", padx=30, pady=(40, 30))

        #dropdown for to field
        to_menu = AutocompleteCombobox(
            main_app,
            textvariable=destination_city,
            completevalues=cities_in_uk,
            width=25,
            font=("Time New Roman", 22, "bold"),
    )
        to_menu.grid(row=2, column=1, sticky="w", padx=30, pady=(40, 30))

        #button to plan the trip
        plan_button = tk.Button(
        main_app,
        text="Find Your Routes 🚀",
        command=plan_trip,
        font=("Time New Roman", 25, "bold"), #set font
        bg="#006400",
        fg="white",
        padx=20,
        pady=10,
        relief="raised",
        bd=5,
        cursor="hand2"
    )
        plan_button.grid(row=5, column=0, columnspan=2, pady=(100, 40))

        main_app.grid_columnconfigure(0, weight=1)
        main_app.grid_columnconfigure(1, weight=1)

        main_app.mainloop() #run the app
    except Exception as e:
        messagebox.showerror("Error in Main Application", f"An error occurred: {str(e)}")
        with open("error_log.txt", "a") as error_file:
            error_file.write(f"{datetime.now()} - open_main_application: {str(e)}\n")

#ask how user wants to travel
def travel_method(from_city, to_city):
    def confirm_method():
        if selected_method.get() == "": #if no method is chosen
            messagebox.showwarning("No Method Selected", "Please choose a travel method! 🚨")
            return
        #check for flights
        elif selected_method.get() == "Flight ✈️":
            if from_city not in flight_routes or to_city not in flight_routes.get(from_city, {}):
                messagebox.showwarning("No Flights", f"Sorry, there are no direct flights from {from_city} to {to_city}.")
                return
            else:
                airlines = ", ".join(flight_routes[from_city][to_city])
                travel_method_app.destroy() #close window
                flight_details(from_city, to_city, airlines) #show flight details
        elif selected_method.get() == "Train 🚅": #check for train
            if from_city not in train_routes or to_city not in train_routes.get(from_city, {}):
                messagebox.showwarning("No Trains", f"Sorry, there are no direct trains from {from_city} to {to_city}.")
                return
            else:
                operators = ", ".join(train_routes[from_city][to_city])
                travel_method_app.destroy() #close window
                train_details(from_city, to_city, operators)
        elif selected_method.get() == "Coach 🚌": #check for coaches
            if from_city not in coach_routes or to_city not in coach_routes.get(from_city, {}):
                messagebox.showwarning("No Coaches", f"Sorry, there are no direct coaches from {from_city} to {to_city}.")
                return
            else:
                operators = ", ".join(coach_routes[from_city][to_city])
                travel_method_app.destroy() #close window
                coach_details(from_city, to_city, operators) #show coach details

    def update_selection(method):
        #change button color base on selected method
        selected_method.set(method)
        flight_button.config(bg="white" if method != "Flight ✈️" else "lightgreen")
        coach_button.config(bg="white" if method != "Coach 🚌" else "lightgreen")
        train_button.config(bg="white" if method != "Train 🚅" else "lightgreen")

    #create a new window to pick travel method
    travel_method_app = tk.Tk()
    travel_method_app.title("Choose Travel Method") #window title
    travel_method_app.geometry("2000x1000") #set size
    travel_method_app.configure(bg="lightblue") #background color

    #label to show trip details
    label = tk.Label(travel_method_app, text=f"You are traveling from {from_city} to {to_city} 🏖️", font=("Time New Roman", 25, "bold"), bg="lightblue")
    label.grid(row=0, column=0, columnspan=3, pady=(70, 70))

    #ask the user for their preferred travel method
    method_label = tk.Label(travel_method_app, text="Which method of travel do you prefer?", font=("Time New Roman", 23, "bold"), bg="lightblue")
    method_label.grid(row=1, column=0, columnspan=3, pady=(30, 100))

    selected_method = tk.StringVar() #to store selected method
    selected_method.set("") #start with no method selected

    #button for flight
    flight_button = tk.Button(
        travel_method_app, text="Flight ✈️", font=("Time New Roman", 20, "bold"), bg="white",
        command=lambda: update_selection("Flight ✈️"), width=12, height=2 #select flight
    )
    flight_button.grid(row=2, column=0, padx=20, pady=(0, 40))

    #button for train
    train_button = tk.Button(
        travel_method_app, text="Train 🚅", font=("Time New Roman", 20, "bold"), bg="white",
        command=lambda: update_selection("Train 🚅"), width=12, height=2 #select train
    )
    train_button.grid(row=2, column=1, padx=20, pady=(0, 40))

    #button for coach
    coach_button = tk.Button(
        travel_method_app, text="Coach 🚌", font=("Time New Roman", 20, "bold"), bg="white",
        command=lambda: update_selection("Coach 🚌"), width=12, height=2 #select coach
    )
    coach_button.grid(row=2, column=2, padx=20, pady=(0, 40))

    # Confirm button to proceed with the selected method
    confirm_button = tk.Button(
    travel_method_app,
    text="Confirm Route ✅",
    font=("Time New Roman", 23, "bold"),
    command=confirm_method, #go to next step
    bg="dark green",
    fg="white" 
)
    confirm_button.grid(row=3, column=0, columnspan=3, pady=(100, 20))

    #centre the columns 
    travel_method_app.grid_columnconfigure(0, weight=1)
    travel_method_app.grid_columnconfigure(1, weight=1)
    travel_method_app.grid_columnconfigure(2, weight=1)

    travel_method_app.mainloop() #run the app

def coach_details(from_city, to_city, operators):
    # Function to handle time selection for a coach
    def select_time(operator, selected_time):
        coach_details_app.destroy() # Close the coach details window
        ticket_details(operator, selected_time, from_city, to_city) # Proceed to ticket details

    # Function to generate random times for coach availability
    def generate_random_times():
        morning_time = f"{random.randint(5, 10):02}:00 AM"
        afternoon_time = f"{random.randint(12, 15):02}:00 PM"
        evening_time = f"{random.randint(18, 22):02}:00 PM"
        return morning_time, afternoon_time, evening_time

    # Set up the main window for coach details
    coach_details_app = tk.Tk()
    coach_details_app.title("Coach Details")
    coach_details_app.geometry("2000x1000")
    coach_details_app.configure(bg="lightblue") #set background color

    # Get the stops for departure and arrival
    from_stop = coach_stops.get(from_city, "Unknown Stop")
    to_stop = coach_stops.get(to_city, "Unknown Stop")
    today_date = datetime.now().strftime("%Y-%m-%d") #get today's date

    #header label
    header_label = tk.Label(coach_details_app, text="Coach Details 🚌", font=("Time New Roman", 32, "bold"), bg="lightblue")
    header_label.pack(pady=30) #add padding to the top

    # Information frame showing details like date, departure, and arrival stops
    info_frame = tk.Frame(coach_details_app, bg="lightblue", pady=40)
    info_frame.pack(fill="x") #expand horizontally
    tk.Label(info_frame, text=f"Date 📅: {today_date}", font=("Time New Roman", 20, "bold"), bg="lightblue").pack(anchor="w", padx=(50, 30), pady=(10, 20))
    tk.Label(info_frame, text=f"Departure Stop: {from_stop}", font=("Time New Roman", 20, "bold"), bg="lightblue").pack(anchor="w", padx=(50, 30), pady=(10, 20))
    tk.Label(info_frame, text=f"Arrival Stop: {to_stop}", font=("Time New Roman", 20, "bold"), bg="lightblue").pack(anchor="w", padx=(50, 30), pady=(10, 20))

    # Frame for listing available coaches
    coaches_frame = tk.Frame(coach_details_app, bg="white", pady=10)
    coaches_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Label for available coaches
    tk.Label(coaches_frame, text="Available Coaches 🚍", font=("Time New Roman", 23, "bold"), bg="white").pack(anchor="w", pady=10)

    # Create buttons for each operator and its respective times
    for operator in operators.split(", "):
        # Generate random times for each operator
        morning_time, afternoon_time, evening_time = generate_random_times()

        # Frame for each operator
        operator_frame = tk.Frame(coaches_frame, bg="lightgray", pady=10, padx=10, bd=1, relief="solid")
        operator_frame.pack(fill="x", pady=10)

        # Label for the operator name
        tk.Label(operator_frame, text=f"Coach Operator 🚌: {operator}", font=("Time New Roman", 20, "bold"), bg="lightgray").pack(anchor="w")

        # Frame for time buttons
        times_frame = tk.Frame(operator_frame, bg="lightgray")
        times_frame.pack(pady=10)

        # Create buttons for each time (Morning, Afternoon, Evening)
        tk.Button(times_frame, text=f"Morning: {morning_time}", font=("Time New Roman", 18, "bold"), bg="white", 
                  command=lambda o=operator, t=morning_time: select_time(o, t)).grid(row=0, column=0, padx=5)
        tk.Button(times_frame, text=f"Afternoon: {afternoon_time}", font=("Time New Roman", 18, "bold"), bg="white", 
                  command=lambda o=operator, t=afternoon_time: select_time(o, t)).grid(row=0, column=1, padx=5)
        tk.Button(times_frame, text=f"Evening: {evening_time}", font=("Time New Roman", 18, "bold"), bg="white", 
                  command=lambda o=operator, t=evening_time: select_time(o, t)).grid(row=0, column=2, padx=5)

    #start tkinter main loop
    coach_details_app.mainloop()

def train_details(from_city, to_city, operators):
    # Function to handle time selection for a train
    def select_time(operator, selected_time):
        train_details_app.destroy() # Close the train details window
        ticket_details(operator, selected_time, from_city, to_city) # Proceed to ticket details

    # Function to generate random times
    def generate_random_times():
        morning_time = f"{random.randint(5, 10):02}:00 AM"
        afternoon_time = f"{random.randint(12, 15):02}:00 PM"
        evening_time = f"{random.randint(18, 22):02}:00 PM"
        return morning_time, afternoon_time, evening_time

    # Set up the main window for train details
    train_details_app = tk.Tk()
    train_details_app.title("Train Details")
    train_details_app.geometry("2000x1000")
    train_details_app.configure(bg="lightblue")

    # Get the stations for departure and arrival
    from_station = train_stations.get(from_city, "Unknown Station")
    to_station = train_stations.get(to_city, "Unknown Station")
    today_date = datetime.now().strftime("%Y-%m-%d") #today's date

    #header label 
    header_label = tk.Label(train_details_app, text="Train Details 🚆", font=("Time New Roman", 32, "bold"), bg="lightblue")
    header_label.pack(pady=30)

    info_frame = tk.Frame(train_details_app, bg="lightblue", pady=10)
    info_frame.pack(fill="x") #expand horizontally
    tk.Label(info_frame, text=f"Date 📅: {today_date}", font=("Time New Roman", 20, "bold"), bg="lightblue").pack(anchor="w", padx=(50, 30), pady=(10, 20))
    tk.Label(info_frame, text=f"Departure Station: {from_station}", font=("Time New Roman", 20, "bold"), bg="lightblue").pack(anchor="w", padx=(50, 30), pady=(10, 20))
    tk.Label(info_frame, text=f"Arrival Station: {to_station}", font=("Time New Roman", 20, "bold"), bg="lightblue").pack(anchor="w", padx=(50, 30), pady=(10, 20))

    #frame for listing available trains
    trains_frame = tk.Frame(train_details_app, bg="white", pady=10)
    trains_frame.pack(fill="both", expand=True, padx=20, pady=10)

    tk.Label(trains_frame, text="Available Trains 🚆", font=("Time New Roman", 23, "bold"), bg="white").pack(anchor="w", pady=10)

    # Create buttons for each operator
    for operator in operators.split(", "):
        # Generate random times for each operator
        morning_time, afternoon_time, evening_time = generate_random_times()

        operator_frame = tk.Frame(trains_frame, bg="lightgray", pady=10, padx=10, bd=1, relief="solid")
        operator_frame.pack(fill="x", pady=10)

        tk.Label(operator_frame, text=f"Train Operator 🚄: {operator}", font=("Time New Roman", 20, "bold"), bg="lightgray").pack(anchor="w")

        times_frame = tk.Frame(operator_frame, bg="lightgray")
        times_frame.pack(pady=10)

        tk.Button(times_frame, text=f"Morning: {morning_time}", font=("Time New Roman", 18, "bold"), bg="white", 
                  command=lambda o=operator, t=morning_time: select_time(o, t)).grid(row=0, column=0, padx=5)
        tk.Button(times_frame, text=f"Afternoon: {afternoon_time}", font=("Time New Roman", 18, "bold"), bg="white", 
                  command=lambda o=operator, t=afternoon_time: select_time(o, t)).grid(row=0, column=1, padx=5)
        tk.Button(times_frame, text=f"Evening: {evening_time}", font=("Time New Roman", 18, "bold"), bg="white", 
                  command=lambda o=operator, t=evening_time: select_time(o, t)).grid(row=0, column=2, padx=5)

    train_details_app.mainloop()

def flight_details(from_city, to_city, airlines):
    # Function to handle time selection for a flight
    def select_time(airline, selected_time):
        flight_details_app.destroy() # Close the flight details window
        ticket_details(airline, selected_time, from_city, to_city)

    # Function to generate random times
    def generate_random_times():
        morning_time = f"{random.randint(5, 10):02}:00 AM"
        afternoon_time = f"{random.randint(12, 15):02}:00 PM"
        evening_time = f"{random.randint(18, 22):02}:00 PM"
        return morning_time, afternoon_time, evening_time

    # Set up the main window for flight details
    flight_details_app = tk.Tk()
    flight_details_app.title("Flight Details")
    flight_details_app.geometry("2000x1000")
    flight_details_app.configure(bg="lightblue")

    # Get the airports for departure and arrival
    from_airport = airport_names.get(from_city, "Unknown Airport")
    to_airport = airport_names.get(to_city, "Unknown Airport")
    today_date = datetime.now().strftime("%Y-%m-%d")

    header_label = tk.Label(flight_details_app, text="Flight Details 🛫", font=("Time New Roman", 32, "bold"), bg="lightblue")
    header_label.pack(pady=30)

    info_frame = tk.Frame(flight_details_app, bg="lightblue", pady=10)
    info_frame.pack(fill="x")
    tk.Label(info_frame, text=f"Date 📅: {today_date}", font=("Time New Roman", 20, "bold"), bg="lightblue").pack(anchor="w", padx=(50, 30), pady=(10, 20))
    tk.Label(info_frame, text=f"Departure Airport: {from_airport}", font=("Time New Roman", 20, "bold"), bg="lightblue").pack(anchor="w", padx=(50, 30), pady=(10, 20))
    tk.Label(info_frame, text=f"Arrival Airport: {to_airport}", font=("Time New Roman", 20, "bold"), bg="lightblue").pack(anchor="w", padx=(50, 30), pady=(10, 20))

    flights_frame = tk.Frame(flight_details_app, bg="white", pady=10)
    flights_frame.pack(fill="both", expand=True, padx=20, pady=10)

    tk.Label(flights_frame, text="Available Flights", font=("Time New Roman", 23, "bold"), bg="white").pack(anchor="w", pady=10)

    # Create buttons for each airline 
    for airline in airlines.split(", "):
        # Generate random times
        morning_time, afternoon_time, evening_time = generate_random_times()

        airline_frame = tk.Frame(flights_frame, bg="lightgray", pady=10, padx=10, bd=1, relief="solid")
        airline_frame.pack(fill="x", pady=10)

        tk.Label(airline_frame, text=f"Airline ✈️: {airline}", font=("Time New Roman", 20, "bold"), bg="lightgray").pack(anchor="w")

        times_frame = tk.Frame(airline_frame, bg="lightgray")
        times_frame.pack(pady=10)

        tk.Button(times_frame, text=f"Morning: {morning_time}", font=("Time New Roman", 18, "bold"), bg="white", 
                  command=lambda a=airline, t=morning_time: select_time(a, t)).grid(row=0, column=0, padx=5)
        tk.Button(times_frame, text=f"Afternoon: {afternoon_time}", font=("Time New Roman", 18, "bold"), bg="white", 
                  command=lambda a=airline, t=afternoon_time: select_time(a, t)).grid(row=0, column=1, padx=5)
        tk.Button(times_frame, text=f"Evening: {evening_time}", font=("Time New Roman", 18, "bold"), bg="white", 
                  command=lambda a=airline, t=evening_time: select_time(a, t)).grid(row=0, column=2, padx=5)

    flight_details_app.mainloop()

def ticket_details(operator, time, from_city, to_city):
    # Function to increase the passenger count (up to 3)
    def increment_passengers():
        current = int(passenger_count_var.get()) # Get the current passenger count
        if current < 3: # Max limit is 3 passengers
            current += 1
            passenger_count_var.set(current) # Update the value displayed

    # Function to decrease the passenger count (minimum 1)
    def decrement_passengers():
        current = int(passenger_count_var.get()) # Get the current passenger count
        if current > 1: # Minimum limit is 1 passenger
            current -= 1
            passenger_count_var.set(current)

    # Function to set the passenger type (Adult or Kid)
    def set_passenger_type(passenger_type):
        passenger_type_var.set(passenger_type)
        # Highlight the selected button and reset the other
        if passenger_type == "Adult":
            adult_button.config(bg="lightgreen")
            kid_button.config(bg="white")
        else:
            adult_button.config(bg="white")
            kid_button.config(bg="lightgreen")

    # Function to set the travel class (Economy or Business)
    def set_travel_class(travel_class):
        travel_class_var.set(travel_class)
        # Highlight the selected button and reset the other
        if travel_class == "Business":
            business_button.config(bg="lightgreen")
            economy_button.config(bg="white")
        else:
            business_button.config(bg="white")
            economy_button.config(bg="lightgreen")

    # Function to proceed to the next step (seat selection)
    def go_to_next():
        selected_seats = []  # Initialize an empty list for selected seats
        ticket_details_to_seat_selection(ticket_details_window, from_city, to_city, operator, time, travel_class_var, selected_seats)


    # Set up the main window for ticket details
    ticket_details_window = tk.Tk()
    ticket_details_window.title("Ticket Details")
    ticket_details_window.geometry("2000x1000")
    ticket_details_window.configure(bg="lightblue")

    # Add a title for the page
    tk.Label(ticket_details_window, text="Ticket Details 🎫", font=("Time New Roman", 36, "bold"), bg="lightblue").pack(pady=15)

    # Display travel details (from, to, operator, departure time)
    tk.Label(ticket_details_window, text=f"From: {from_city} ➡ To: {to_city}", font=("Time New Roman", 28, "bold"), bg="lightblue").pack(pady=15)
    tk.Label(ticket_details_window, text=f"Operator: {operator}", font=("Time New Roman", 28, "bold"), bg="lightblue").pack(pady=15)
    tk.Label(ticket_details_window, text=f"Departure Time: {time}", font=("Time New Roman", 28, "bold"), bg="lightblue").pack(pady=(15, 10))

    #Create a content frame to hold passenger options
    content_frame = tk.Frame(ticket_details_window, bg="lightblue")
    content_frame.pack(pady=20)

    passenger_frame = tk.Frame(content_frame, bg="lightblue")
    passenger_frame.grid(row=0, column=0, padx=10, pady=20, sticky="w")

    tk.Label(passenger_frame, text="Number of Passengers:", font=("Time New Roman", 26, "bold"), bg="lightblue").grid(row=0, column=0, sticky="w")
    decrement_button = tk.Button(passenger_frame, text="-", font=("Time New Roman", 22, "bold"), command=decrement_passengers, width=3)
    decrement_button.grid(row=0, column=1, padx=10)

    passenger_count_var = tk.IntVar(value=1)
    passenger_count_label = tk.Label(passenger_frame, textvariable=passenger_count_var, font=("Time New Roman", 22, "bold"), width=5, height=1, bg="white", relief="solid")
    passenger_count_label.grid(row=0, column=2, padx=10)

    increment_button = tk.Button(passenger_frame, text="+", font=("Time New Roman", 22, "bold"), command=increment_passengers, width=3)
    increment_button.grid(row=0, column=3, padx=10)

    type_frame = tk.Frame(content_frame, bg="lightblue")
    type_frame.grid(row=1, column=0, padx=20, pady=20, sticky="w")

    tk.Label(type_frame, text="Type of Passengers:", font=("Time New Roman", 26, "bold"), bg="lightblue").grid(row=0, column=0, sticky="w")

    passenger_type_var = tk.StringVar(value="Adult")
    adult_button = tk.Button(type_frame, text="Adult 👨", font=("Time New Roman", 20, "bold"), bg="lightgreen", command=lambda: set_passenger_type("Adult"))
    adult_button.grid(row=0, column=1, padx=10)

    kid_button = tk.Button(type_frame, text="Kid 🧒", font=("Time New Roman", 20, "bold"), bg="white", command=lambda: set_passenger_type("Kid"))
    kid_button.grid(row=0, column=2, padx=10)

    class_frame = tk.Frame(content_frame, bg="lightblue")
    class_frame.grid(row=2, column=0, padx=20, pady=20, sticky="w")

    tk.Label(class_frame, text="Class:", font=("Time New Roman", 26, "bold"), bg="lightblue").grid(row=0, column=0, sticky="w")

    travel_class_var = tk.StringVar(value="Economy")
    business_button = tk.Button(class_frame, text="Business", font=("Time New Roman", 20, "bold"), bg="white", command=lambda: set_travel_class("Business"))
    business_button.grid(row=0, column=1, padx=10)

    economy_button = tk.Button(class_frame, text="Economy", font=("Time New Roman", 20, "bold"), bg="lightgreen", command=lambda: set_travel_class("Economy"))
    economy_button.grid(row=0, column=2, padx=10)

    next_button = tk.Button(
        ticket_details_window,
        text="Next ➡️",
        font=("Time New Roman", 16, "bold"),
        bg="#006400",
        fg="white",
        command=go_to_next,
        relief="raised",
        bd=5
    )
    next_button.place(relx=0.9, rely=0.9, anchor="center")

    ticket_details_window.mainloop()

def resize_background(event=None):
    """Dynamically resize the background image to fit the window."""
    global bg_photo
    new_width = root.winfo_width()
    new_height = root.winfo_height()

    resized_image = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(resized_image)

    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

def ticket_details_to_seat_selection(previous_window, from_city, to_city, operator, time, travel_class_var, selected_seats):
    # Close the previous window
    previous_window.destroy()

    # Create a new Tk instance for seat selection
    seat_selection_window = tk.Tk()
    seat_selection_window.title("Seat Selection")
    seat_selection_window.geometry("2000x1000")
    seat_selection_window.configure(bg="lightblue")

    travel_class = travel_class_var.get()

    def toggle_seat(seat_button, seat_number):
        """Toggle seat selection with restrictions based on class."""
        if travel_class == "Economy" and seat_number.startswith(("A", "B")):
            messagebox.showwarning("Class Restriction", "Economy Class can only select seats from C1 to F9.")
            return
        elif travel_class == "Business" and not seat_number.startswith(("A", "B")):
            messagebox.showwarning("Class Restriction", "Business Class can only select seats from A1 to B9.")
            return

        if seat_number in selected_seats:
            selected_seats.remove(seat_number)
            seat_button.config(
                bg="grey" if seat_number.startswith(("A", "B")) else "white",
                fg="white" if seat_number.startswith(("A", "B")) else "black"
            )
        else:
            if len(selected_seats) < max_seats:
                selected_seats.append(seat_number)
                seat_button.config(bg="lightgreen", fg="black")  # Highlight selected seat
            else:
                messagebox.showwarning("Seat Limit Reached", f"You can only select up to {max_seats} seats.")

    def confirm_selection():
        """Confirm seat selection and proceed to price details."""
        if not selected_seats:
            messagebox.showwarning("No Seats Selected", "Please select at least one seat.")
            return

        business_seats = [seat for seat in selected_seats if seat.startswith(("A", "B"))]
        economy_seats = [seat for seat in selected_seats if not seat.startswith(("A", "B"))]

        seat_selection_window.destroy()
        display_price_details(operator, from_city, to_city, selected_seats, business_seats, economy_seats, time)

    # Add UI elements here (seat grid, legend, etc.)
    tk.Label(seat_selection_window, text="Select Your Seats", font=("Time New Roman", 28, "bold"), bg="lightblue").pack(pady=20)

    seat_frame = tk.Frame(seat_selection_window, bg="white")
    seat_frame.pack(pady=20)

    rows_business = ["A", "B"]
    rows_economy = ["C", "D", "E", "F"]
    columns_per_side = 4
    max_seats = 3

    for idx, row in enumerate(rows_business + [""] + rows_economy):
        if row == "":
            tk.Label(seat_frame, text=" ", bg="white").grid(row=idx, columnspan=2 * columns_per_side + 1, pady=20)
            continue

        for col in range(2 * columns_per_side + 1):
            if col == columns_per_side:
                tk.Label(seat_frame, text="  ", bg="white").grid(row=idx, column=col, padx=10)
                continue

            if col < columns_per_side:
                seat_number = f"{row}{col + 1}"
            else:
                seat_number = f"{row}{col - columns_per_side + 5}"

            if row in rows_business:
                bg_color = "grey"
                font_color = "white"
            else:
                bg_color = "white"
                font_color = "black"

            seat_button = tk.Button(
                seat_frame,
                text=seat_number,
                font=("Time New Roman", 14),
                bg=bg_color,
                fg=font_color,  # Set font color
                width=5,
                height=2
            )
            seat_button.config(
                command=lambda btn=seat_button, num=seat_number: toggle_seat(btn, num)
            )
            seat_button.grid(row=idx, column=col, padx=5, pady=5)

    legend_frame = tk.Frame(seat_selection_window, bg="lightblue")
    legend_frame.pack(pady=10)

    tk.Label(
        legend_frame,
        text="Business Class:",
        font=("Time New Roman", 16, "bold"),
        bg="lightblue"
    ).grid(row=0, column=0, padx=10)
    tk.Label(
        legend_frame,
        bg="grey",
        width=3,
        height=1
    ).grid(row=0, column=1, padx=10)

    tk.Label(
        legend_frame,
        text="Economy Class:",
        font=("Time New Roman", 16, "bold"),
        bg="lightblue"
    ).grid(row=0, column=2, padx=10)
    tk.Label(
        legend_frame,
        bg="white",
        width=3,
        height=1,
        relief="solid"
    ).grid(row=0, column=3, padx=10)

    confirm_button = tk.Button(
        seat_selection_window,
        text="Confirm Seats",
        font=("Time New Roman", 20, "bold"),
        bg="#006400",
        fg="white",
        command=confirm_selection
    )
    confirm_button.pack(pady=30)

    seat_selection_window.mainloop()

def calculate_price(seat_class, passenger_type, travel_type, time_of_travel):
    import random

    # Base prices for each travel type and seat class
    base_prices = {
        "Flight": {"Economy": 500.99, "Business": 1000.99},
        "Train": {"Economy": 300.99, "Business": 500.99},
        "Coach": {"Economy": 150.99, "Business": 200.99},
    }

    # Fetch the base price
    base_price = base_prices.get(travel_type, {}).get(seat_class, 0)

    # Apply time multiplier
    time_multipliers = {
        "Morning": 2.0,   # High demand
        "Afternoon": 1.5, # Moderate demand
        "Evening": 2.5,   # Peak demand
    }
    base_price *= time_multipliers.get(time_of_travel, 1.0)

    # Apply fixed class adjustment
    class_adjustments = {"Economy": 100, "Business": 200}
    base_price += class_adjustments.get(seat_class, 0)

    # Add random variation for realism
    tax_variation = random.uniform(5.00, 30.00)  # Fix: Correct range for random variation
    base_price += tax_variation

    # Apply kid discount
    if passenger_type == "Kid":
        base_price *= 0.6  # Kids pay 60% of the adult price (40% discount)

    # Add a minimum price threshold
    minimum_price = 60
    base_price = max(base_price, minimum_price)

    # Return the final price rounded to 2 decimals
    return round(base_price, 2)

def display_price_details(travel_type, from_city, to_city, selected_seats, business_seats, economy_seats, travel_time):
    price_details_window = tk.Tk()
    price_details_window.title("Price Details")
    price_details_window.geometry("2000x1000")
    price_details_window.configure(bg="#DFF6FF")

    tk.Label(
        price_details_window,
        text="Price Details",
        font=("Time New Roman", 32, "bold"),
        bg="#DFF6FF",
    ).pack(pady=10)

    travel_info_frame = tk.Frame(price_details_window, bg="#DFF6FF")
    travel_info_frame.pack(pady=10)

    tk.Label(
        travel_info_frame,
        text=f"Name: {travel_type}",
        font=("Time New Roman", 20, "bold"),
        bg="#DFF6FF",
    ).grid(row=0, column=0, padx=40, sticky="w")
    tk.Label(
        travel_info_frame,
        text=f"From: {from_city} ➡ To: {to_city}",
        font=("Time New Roman", 20, "bold"),
        bg="#DFF6FF",
    ).grid(row=1, column=0, padx=10, pady=20, sticky="w")

    table_frame = tk.Frame(price_details_window, bg="white", relief="solid", bd=2)
    table_frame.pack(pady=20, padx=50)

    # Header Row
    tk.Label(
        table_frame,
        text="Class",
        font=("Time New Roman", 18, "bold"),
        bg="#E3F2FD",
        width=20,
        relief="ridge",
    ).grid(row=0, column=0)
    tk.Label(
        table_frame,
        text="Seat Number",
        font=("Time New Roman", 18, "bold"),
        bg="#E3F2FD",
        width=20,
        relief="ridge",
    ).grid(row=0, column=1)
    tk.Label(
        table_frame,
        text="Cost (£)",
        font=("Time New Roman", 18, "bold"),
        bg="#E3F2FD",
        width=20,
        relief="ridge",
    ).grid(row=0, column=2)

    # Calculate individual seat costs dynamically
    total_cost = 0
    for i, seat in enumerate(selected_seats):
        seat_class = "Business" if seat.startswith(("A", "B")) else "Economy"
        passenger_type = "Adult"  # Assuming Adult; adjust if you track this info
        travel_time = "Morning"  # Set default; update if you pass this dynamically

        # Calculate dynamic price using the calculate_price function
        cost = calculate_price(seat_class, passenger_type, travel_type, travel_time)
        total_cost += cost

        # Add each seat's details to the table
        tk.Label(
            table_frame,
            text=seat_class,
            font=("Time New Roman", 16, "bold"),
            bg="white",
            width=20,
        ).grid(row=i + 1, column=0)
        tk.Label(
            table_frame,
            text=seat,
            font=("Time New Roman", 16, "bold"),
            bg="white",
            width=20,
        ).grid(row=i + 1, column=1)
        tk.Label(
            table_frame,
            text=f"£{cost:.2f}",
            font=("Time New Roman", 16, "bold"),
            bg="white",
            width=20,
        ).grid(row=i + 1, column=2)

    summary_frame = tk.Frame(price_details_window, bg="#DFF6FF")
    summary_frame.pack(pady=20)

    tk.Label(
        summary_frame,
        text=f"Total Price: £{total_cost:.2f}",
        font=("Time New Roman", 24, "bold"),
        bg="#DFF6FF",
        fg="green",
    ).grid(row=2, column=0, padx=20, pady=20, sticky="w")

    confirm_button = tk.Button(
        price_details_window,
        text="Confirm Booking ✅",
        font=("Time New Roman", 20, "bold"),
        bg="#28A745",
        fg="white",
        width=20,
        height=2,
        command=lambda: confirm_booking(
            from_city, to_city, travel_type, selected_seats, total_cost
        ),
    )
    confirm_button.pack(pady=30)

    price_details_window.mainloop()

def sort_seat_prices(prices, selected_seats):
    """Sort seat prices in ascending order and sort seats accordingly."""
    n = len(prices)
    for i in range(n):
        for j in range(0, n - i - 1):
            if prices[j] > prices[j + 1]:
                # Swap the prices and the corresponding seats
                prices[j], prices[j + 1] = prices[j + 1], prices[j]
                selected_seats[j], selected_seats[j + 1] = selected_seats[j + 1], selected_seats[j]
    return selected_seats, prices

def confirm_booking(from_city, to_city, travel_type, selected_seats, total_price):
    """Handle booking confirmation and display the ticket invoice."""
    booking_details = f"""
    Booking Confirmed! 🎉
    -----------------------
    Travel Type: {travel_type}
    From: {from_city}
    To: {to_city}
    Selected Seats: {', '.join(selected_seats)}
    Total Price: £{total_price}
    """

    messagebox.showinfo("Booking Confirmed ✅", booking_details)

    with io.open("ticket_invoice.txt", "w", encoding="utf-8") as file:
        file.write(booking_details + "\n")
    
    display_ticket_invoice(from_city, to_city, travel_type, selected_seats, total_price)

def display_ticket_invoice(from_city, to_city, travel_type, selected_seats, total_price):
    """Display the ticket invoice and save as text or PDF."""

    # Generate booking details
    booking_id = f"INV-{random.randint(1000, 9999)}-{random.randint(100, 999)}"
    booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # File names for PDF and text
    pdf_filename = f"ticket_invoice_{booking_id}.pdf"
    text_filename = f"ticket_invoice_{booking_id}.txt"

    # Invoice text to display and save
    invoice_text = f"""
    -------------------------
    Ticket Invoice
    -------------------------
    Booking ID: {booking_id}
    Booking Date: {booking_date}

    From: {from_city}
    To: {to_city}
    Travel Type: {travel_type}

    Selected Seats: {', '.join(selected_seats)}
    Total Price: £{total_price}

    Thank you for booking with Travel Planner!
    -------------------------
    """

    # Save the invoice as a text file
    with open(text_filename, "w", encoding="utf-8") as file:
        file.write(invoice_text)

    # Generate the PDF
    import qrcode
    from io import BytesIO
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas as pdf_canvas  # Alias to avoid conflict
    from reportlab.lib import colors  # For colors like colors.lightblue, colors.beige
    from reportlab.platypus import Table, TableStyle  # For creating and styling tables
    from PIL import Image
    import os

    def save_pdf_with_qr():
        logo_path = os.path.join(current_dir, "travel_planner_logo.jpg")

        # Create PDF canvas
        c = pdf_canvas.Canvas(pdf_filename, pagesize=letter)
        page_width, page_height = letter

        # Add a title
        title_text = "Thank You for choosing Travel Planner"
        c.setFont("Helvetica-Bold", 20)
        title_width = c.stringWidth(title_text, "Helvetica-Bold", 20)
        c.drawString((page_width - title_width) / 2, page_height - 50, title_text)

        # Add the logo
        logo_width = page_width * 0.2  # Smaller size
        logo_height = logo_width
        logo_y_position = page_height - logo_height - 120
        c.drawImage(
            logo_path,
            x=50,  # Left-aligned
            y=logo_y_position,
            width=logo_width,
            height=logo_height,
            preserveAspectRatio=True,
            mask="auto",
        )

        # Define table width based on page width
        table_width = page_width * 0.8

        # Prepare "Travel Details" data
        travel_details_data = [
            ["Travel Details", ""],
            ["From", from_city],
            ["To", to_city],
            ["Travel Type", travel_type],
            ["Seats", ", ".join(selected_seats)],
            ["Date", booking_date],
            ["Total Price (£)", f" £ {total_price}"],
        ]

        # Create "Travel Details" table
        travel_table = Table(
            travel_details_data, colWidths=[table_width * 0.4, table_width * 0.6]
        )
        travel_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Draw the tables on the PDF
        y_position = page_height - logo_height - 300
        travel_table.wrapOn(c, page_width, page_height)
        travel_table.drawOn(c, (page_width - table_width) / 2, y_position)

        qr_data = f"Booking ID: {booking_id}\nFrom: {from_city}\nTo: {to_city}\nSeats: {', '.join(selected_seats)}\nTotal Price: £{total_price}"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        temp_qr_path = "temp_qr_code.png"
        qr_img.save(temp_qr_path)

        temp_qr_path = "temp_qr_code.png"
        qr_img.save(temp_qr_path)

        y_position -= 150 
        c.drawImage(temp_qr_path, (page_width - 100) / 2, y_position, width=100, height=100)

        y_position -= 50 
        c.setFont("Helvetica", 12)
        c.drawString(
            (page_width - 400) / 2,
            y_position,
            "This is your booking QR code. Please scan it at the departure."
        )

        c.save()
        os.remove(temp_qr_path)
        messagebox.showinfo("PDF Saved", f"Your ticket invoice has been saved as '{pdf_filename}'.")
        
    invoice_window = tk.Tk()
    invoice_window.title("Ticket Invoice")
    invoice_window.geometry("2000x1000")
    invoice_window.configure(bg="#F5F5F5")

    tk.Label(
        invoice_window,
        text="Ticket Invoice",
        font=("Time New Roman", 36, "bold"),
        bg="#F5F5F5",
        fg="black"
    ).pack(pady=20)

    invoice_frame = tk.Frame(invoice_window, bg="white", relief="solid", bd=2)
    invoice_frame.pack(pady=20, padx=100, fill="x")

    for idx, line in enumerate(invoice_text.strip().split("\n")):
        tk.Label(
            invoice_frame,
            text=line,
            font=("Time New Roman", 18),
            bg="white",
        ).grid(row=idx, column=0, sticky="w", padx=20, pady=5)

    save_pdf_button = tk.Button(
        invoice_window,
        text="Save as PDF 🖨️",
        font=("Time New Roman", 20, "bold"),
        bg="green",
        fg="white",
        command=save_pdf_with_qr
    )
    save_pdf_button.pack(pady=20)

    close_button = tk.Button(
        invoice_window,
        text="Close 🛑",
        font=("Time New Roman", 20, "bold"),
        bg="#DC3545",
        fg="white",
        command=invoice_window.destroy
    )
    close_button.pack(pady=10)

    invoice_window.mainloop()

root = tk.Tk()
root.title("Welcome to Travel Planner")
root.geometry("2000x1000") 

bg_image_path = os.path.join(current_dir, "welcome_bg.jpg")
bg_image = Image.open(bg_image_path)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, image=bg_photo, anchor="nw")

welcome_label = tk.Label(
    root,
    text="Welcome to Travel Planner! 🌍",
    font=("Time New Roman", 54, "bold"),
    bg="#87CEEB",
    fg="black",
    padx=20,
    pady=10
)
canvas_window_welcome = canvas.create_window(0, 0, anchor="center", window=welcome_label)

instruction_label = tk.Label(
    root,
    text="Click 'Start' when you are ready to plan your trip",
    font=("Time New Roman", 26, "bold"),
    bg="white",
    fg="black",
    padx=20,
    pady=10
)
canvas_window_instruction = canvas.create_window(0, 0, anchor="center", window=instruction_label)

start_button = tk.Button(
    root,
    text="Start 🚀",
    command=start_application,
    font=("Time New Roman", 30, "bold"),
    bg="#006400",
    fg="white",
    padx=20,
    pady=10,
    relief="raised",
    bd=5,
    cursor="hand2"
)
canvas_window_button = canvas.create_window(0, 0, anchor="center", window=start_button)

def reposition_widgets(event=None):
    """Reposition widgets dynamically based on the canvas size."""
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    canvas.coords(canvas_window_welcome, canvas_width // 2, canvas_height // 4)
    canvas.coords(canvas_window_instruction, canvas_width // 2, canvas_height // 2)
    canvas.coords(canvas_window_button, canvas_width // 2, (canvas_height // 4) * 3)

root.bind("<Configure>", lambda event: (resize_background(event), reposition_widgets(event)))

resize_background()
reposition_widgets()

try:
    root.mainloop()
except Exception as e:
    messagebox.showerror("Application Error", f"An unexpected error occurred: {str(e)}")
    # Log the error into a file
    with open("error_log.txt", "a") as error_file:
        error_file.write(f"{datetime.now()} - root.mainloop: {str(e)}\n")