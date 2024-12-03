#important libraries
import tkinter as tk #to create windows
from tkinter import ttk, messagebox # For special widgets and pop-up messages
from ttkwidgets.autocomplete import AutocompleteCombobox # To show suggestions when typing
from datetime import datetime # To get dates and times
import random #for random time
from PIL import Image, ImageTk #for image handling
from reportlab.lib.pagesizes import letter #for making pdf pages
import io #to handle files

import os #this lets us find files on the computer and work with them
# to know where our program is saved
current_dir = os.path.dirname(os.path.abspath(__file__))

from reportlab.pdfgen import canvas as pdf_canvas #this helps us draw and write in the PDF.
from data import data # type: ignore #this has all travel information

#for file handling 
flight_routes = data["flight_routes"]
train_routes = data["train_routes"]
coach_routes = data["coach_routes"]
airport_names = data["airport_names"]
train_stations = data["train_stations"]
coach_stops = data["coach_stops"]
cities_in_uk = data["cities_in_uk"]

#start application
def start_application():
    """Start the main application."""
    try:
        global root
        root.destroy()  # Close the welcome window
        open_main_application()  # Open the main application
    except Exception as e:
        # If something goes wrong, show an error message with what happened
        messagebox.showerror("Error Starting Application", f"An error occurred: {str(e)}")
        # Log the error
        with open("error_log.txt", "a") as error_file:
            # Write the error details in a file so we know what went wrong later
            error_file.write(f"{datetime.now()} - start_application: {str(e)}\n")

def open_main_application():
    try: #Start the main part of the app
        def plan_trip(): #for planning the trip
            from_city = departure_city.get() #where u want to start
            to_city = destination_city.get() #where u want to go

            # If no city is selected for either "From" or "To", show a warning
            if not from_city or not to_city: #if nothing is chosen
                messagebox.showwarning("Invalid Selection", "Please select both a departure and arrival city.")
                return # Stop the function here if cities are missing

            if from_city == to_city: #if start and end are the same 
                #shows warning
                messagebox.showwarning("Invalid Selection", "Departure and arrival cities cannot be the same! ⚠️")
                return # Stop the function if the cities are the same

            main_app.destroy() #close the window
            travel_method(from_city, to_city) #ask how they want to travel

        #This function updates the "To" city options based on the selected travel method (flight, train, etc.)
        def update_destination_options(event):
            global selected_method
            from_city = departure_city.get() # Get the selected "From" city
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
        
        # Create the main window for the app
        main_app = create_window("Travel Planner", "2000x1000", "lightblue") #create the window

        departure_city = tk.StringVar() #pick the departure city
        destination_city = tk.StringVar() #pick the arrival city

        #label for title
        label = ttk.Label(
            main_app,
            text="Plan Your Journey!", #title of the text
            font=("Time New Roman", 40, "bold"),
            background="lightblue",
    )
        label.grid(row=0, column=0, columnspan=2, pady=(150, 80))

        #label for "from" field
        from_label = ttk.Label(
            main_app,
            text="From 🏖️", # Label to show "From"
            font=("Time New Roman", 30, "bold"),
            background="lightblue",
    )
        from_label.grid(row=1, column=0, sticky="e", padx=30, pady=(20, 40))

        #dropdown for "from" field
        from_menu = AutocompleteCombobox(
            main_app,
            textvariable=departure_city,
            completevalues=cities_in_uk, #show all cities
            width=25,  # Increased width
            font=("Time New Roman", 22, "bold"),
    )
        from_menu.grid(row=1, column=1, sticky="w", padx=30, pady=(20, 40))

        #label for to field
        to_label = ttk.Label(
            main_app,
            text="To 🌍", #label to show "to"
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
        command=plan_trip, # When clicked, it will run the plan_trip function
        font=("Time New Roman", 25, "bold"), #set font
        bg="#006400", #background color
        fg="white", #foreground color
        padx=20,
        pady=10,
        relief="raised", #make the button looks 3D
        bd=5,
        cursor="hand2" # Change the cursor to a hand when hovering over the button
    )
        plan_button.grid(row=5, column=0, columnspan=2, pady=(100, 40))

        # Configure the window to adjust layout
        main_app.grid_columnconfigure(0, weight=1)
        main_app.grid_columnconfigure(1, weight=1)

        # Run the app so the user can interact with it
        main_app.mainloop() #run the app

    #use try-except blocks for error handling
    except Exception as e:
        messagebox.showerror("Error in Main Application", f"An error occurred: {str(e)}")
        with open("error_log.txt", "a") as error_file:
            error_file.write(f"{datetime.now()} - open_main_application: {str(e)}\n")

#ask how user wants to travel
def travel_method(from_city, to_city):
    #checks if the user has selected a method and confirms their choice
    def confirm_method():
        # If no method is chosen, show a warning message
        if selected_method.get() == "":
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

    #how many passengers
    passenger_frame = tk.Frame(content_frame, bg="lightblue")
    passenger_frame.grid(row=0, column=0, padx=10, pady=20, sticky="w")

    #number of passengers
    tk.Label(passenger_frame, text="Number of Passengers:", font=("Time New Roman", 26, "bold"), bg="lightblue").grid(row=0, column=0, sticky="w")
    # Button to decrease the number of passengers (decrement)
    decrement_button = tk.Button(passenger_frame, text="-", font=("Time New Roman", 22, "bold"), command=decrement_passengers, width=3)
    decrement_button.grid(row=0, column=1, padx=10)

    # Create a variable for passenger count and display it (default is 1)
    passenger_count_var = tk.IntVar(value=1)
    passenger_count_label = tk.Label(passenger_frame, textvariable=passenger_count_var, font=("Time New Roman", 22, "bold"), width=5, height=1, bg="white", relief="solid")
    passenger_count_label.grid(row=0, column=2, padx=10)

    # Button to increase the number of passengers (increment)
    increment_button = tk.Button(passenger_frame, text="+", font=("Time New Roman", 22, "bold"), command=increment_passengers, width=3)
    increment_button.grid(row=0, column=3, padx=10)

    # Create a frame to select the type of passengers (e.g. Adult or Kid)
    type_frame = tk.Frame(content_frame, bg="lightblue")
    type_frame.grid(row=1, column=0, padx=20, pady=20, sticky="w")

    # Label to ask for the type of passengers
    tk.Label(type_frame, text="Type of Passengers:", font=("Time New Roman", 26, "bold"), bg="lightblue").grid(row=0, column=0, sticky="w")

    # Button for Adult passenger selection
    passenger_type_var = tk.StringVar(value="Adult") # Default to Adult
    adult_button = tk.Button(type_frame, text="Adult 👨", font=("Time New Roman", 20, "bold"), bg="lightgreen", command=lambda: set_passenger_type("Adult"))
    adult_button.grid(row=0, column=1, padx=10)

    # Button for Kid passenger selection
    kid_button = tk.Button(type_frame, text="Kid 🧒", font=("Time New Roman", 20, "bold"), bg="white", command=lambda: set_passenger_type("Kid"))
    kid_button.grid(row=0, column=2, padx=10)

    # Create a frame for the class selection (e.g. Economy or Business)
    class_frame = tk.Frame(content_frame, bg="lightblue")
    class_frame.grid(row=2, column=0, padx=20, pady=20, sticky="w")

    # Label for class selection
    tk.Label(class_frame, text="Class:", font=("Time New Roman", 26, "bold"), bg="lightblue").grid(row=0, column=0, sticky="w")

    # Button for Business class selection
    travel_class_var = tk.StringVar(value="Economy") #default to economy
    business_button = tk.Button(class_frame, text="Business", font=("Time New Roman", 20, "bold"), bg="white", command=lambda: set_travel_class("Business"))
    business_button.grid(row=0, column=1, padx=10)

    # Button for Economy class selection
    economy_button = tk.Button(class_frame, text="Economy", font=("Time New Roman", 20, "bold"), bg="lightgreen", command=lambda: set_travel_class("Economy"))
    economy_button.grid(row=0, column=2, padx=10)

    # Next button to move to the next step
    next_button = tk.Button(
        ticket_details_window,
        text="Next ➡️",
        font=("Time New Roman", 16, "bold"),
        bg="#006400", # Dark green background
        fg="white",
        command=go_to_next, # Function to run when clicked
        relief="raised",
        bd=5
    )
    next_button.place(relx=0.9, rely=0.9, anchor="center") # Position the button at the bottom right corner

    # Run the window's main loop to show the window
    ticket_details_window.mainloop()

#resize the background image when the window size changes
def resize_background(event=None):
    """Dynamically resize the background image to fit the window."""
    global bg_photo # Declare bg_photo globally to update it
    new_width = root.winfo_width() # Get the new width of the window
    new_height = root.winfo_height() # Get the new height of the window

     # Resize the background image to match the new window size
    resized_image = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(resized_image) # Convert the resized image to Tkinter format

    # Update the canvas to display the resized background image
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Function to move from ticket details to seat selection window
def ticket_details_to_seat_selection(previous_window, from_city, to_city, operator, time, travel_class_var, selected_seats):
    # Close the previous window
    previous_window.destroy()

    # Create a new Tk instance for seat selection
    seat_selection_window = tk.Tk()
    seat_selection_window.title("Seat Selection") # Set the title of the window
    seat_selection_window.geometry("2000x1000") # Set window size
    seat_selection_window.configure(bg="lightblue") # Set background color to light blue

    # Get the selected travel class
    travel_class = travel_class_var.get()

    # Function to handle seat toggling
    def toggle_seat(seat_button, seat_number):
        """Toggle seat selection with restrictions based on class."""
        # If the user selects an invalid seat for their travel class, show a warning
        if travel_class == "Economy" and seat_number.startswith(("A", "B")):
            messagebox.showwarning("Class Restriction", "Economy Class can only select seats from C1 to F9.")
            return
        elif travel_class == "Business" and not seat_number.startswith(("A", "B")):
            messagebox.showwarning("Class Restriction", "Business Class can only select seats from A1 to B9.")
            return

        # Toggle the seat's selection
        if seat_number in selected_seats:
            selected_seats.remove(seat_number) #deselect seat
            seat_button.config(
                bg="grey" if seat_number.startswith(("A", "B")) else "white",
                fg="white" if seat_number.startswith(("A", "B")) else "black"
            )
        else:
            # If the user hasn't reached the maximum seat limit, select the seat
            if len(selected_seats) < max_seats:
                selected_seats.append(seat_number) # Add seat to selected list
                seat_button.config(bg="lightgreen", fg="black")  # Highlight selected seat
            else:
                messagebox.showwarning("Seat Limit Reached", f"You can only select up to {max_seats} seats.")

    # Function to confirm the seat selection and proceed to price details
    def confirm_selection():
        """Confirm seat selection and proceed to price details."""
        if not selected_seats: # If no seats are selected, show a warning
            messagebox.showwarning("No Seats Selected", "Please select at least one seat.")
            return

        # Split the selected seats into Business and Economy categories
        business_seats = [seat for seat in selected_seats if seat.startswith(("A", "B"))]
        economy_seats = [seat for seat in selected_seats if not seat.startswith(("A", "B"))]

        seat_selection_window.destroy() # Close the seat selection window
        # Proceed to display the price details with the selected seats
        display_price_details(operator, from_city, to_city, selected_seats, business_seats, economy_seats, time)

    # Display the seat selection title
    tk.Label(seat_selection_window, text="Select Your Seats", font=("Time New Roman", 28, "bold"), bg="lightblue").pack(pady=20)

    # Create a frame for the seat grid
    seat_frame = tk.Frame(seat_selection_window, bg="white")
    seat_frame.pack(pady=20)

    # Define the rows for Business and Economy class
    rows_business = ["A", "B"] # Business class rows
    rows_economy = ["C", "D", "E", "F"] # Business class rows
    columns_per_side = 4 # Number of columns per row
    max_seats = 3 # Maximum number of seats that can be selected

    # Create the seat grid: Business class, empty space, then Economy class
    for idx, row in enumerate(rows_business + [""] + rows_economy):
        if row == "": # Add space between Business and Economy sections
            tk.Label(seat_frame, text=" ", bg="white").grid(row=idx, columnspan=2 * columns_per_side + 1, pady=20)
            continue

        # Create seats in each row
        for col in range(2 * columns_per_side + 1):
            if col == columns_per_side: # Empty space between the two sides of seats
                tk.Label(seat_frame, text="  ", bg="white").grid(row=idx, column=col, padx=10)
                continue

            # Assign seat numbers based on row and column
            if col < columns_per_side:
                seat_number = f"{row}{col + 1}"
            else:
                seat_number = f"{row}{col - columns_per_side + 5}"

            # Set seat color based on its class (Business or Economy)
            if row in rows_business:
                bg_color = "grey" # Business seats are grey
                font_color = "white"
            else:
                bg_color = "white" # Economy seats are white
                font_color = "black"

            # Create a button for each seat
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
                command=lambda btn=seat_button, num=seat_number: toggle_seat(btn, num) # Handle seat toggle
            )
            seat_button.grid(row=idx, column=col, padx=5, pady=5)

    # Create a frame for the seat selection legend (Business and Economy class labels)
    legend_frame = tk.Frame(seat_selection_window, bg="lightblue")
    legend_frame.pack(pady=10)

    # Business Class label
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

    # Economy Class label
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

    # Confirm button to proceed with the seat selection
    confirm_button = tk.Button(
        seat_selection_window,
        text="Confirm Seats",
        font=("Time New Roman", 20, "bold"),
        bg="#006400", # Dark green background
        fg="white",
        command=confirm_selection # Proceed to next step
    )
    confirm_button.pack(pady=30)

    # Run the seat selection window
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

# This function helps to sort the seat prices from the cheapest to the most expensive
def sort_seat_prices(prices, selected_seats):
    """Sort seat prices in ascending order and sort seats accordingly."""
    n = len(prices) # We count how many prices we have
    for i in range(n): # Go through each price
        for j in range(0, n - i - 1): # Compare each price with the next one
            if prices[j] > prices[j + 1]: # If this price is bigger than the next one
                # Swap the prices and the corresponding seats
                prices[j], prices[j + 1] = prices[j + 1], prices[j]
                selected_seats[j], selected_seats[j + 1] = selected_seats[j + 1], selected_seats[j]
    return selected_seats, prices # Return the sorted list of seats and prices

# This function helps to confirm the booking and show the ticket details
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

    # Show a popup message that says the booking is confirmed
    messagebox.showinfo("Booking Confirmed ✅", booking_details)

    # Save the booking details in a file so we can see it later
    with io.open("ticket_invoice.txt", "w", encoding="utf-8") as file:
        file.write(booking_details + "\n")
    
    # Show the ticket in a special invoice page
    display_ticket_invoice(from_city, to_city, travel_type, selected_seats, total_price)

# This function shows the ticket and saves it as a PDF or text file
def display_ticket_invoice(from_city, to_city, travel_type, selected_seats, total_price):
    """Display the ticket invoice and save as text or PDF."""

    # Make a special number for the booking, like an ID
    booking_id = f"INV-{random.randint(1000, 9999)}-{random.randint(100, 999)}"
    booking_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # We create two names for the files (one for text and one for PDF)
    pdf_filename = f"ticket_invoice_{booking_id}.pdf"
    text_filename = f"ticket_invoice_{booking_id}.txt"

    # This is how the ticket will look like (all the details)
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

    # Save the ticket details in a text file
    with open(text_filename, "w", encoding="utf-8") as file:
        file.write(invoice_text)

    # Generate the PDF
    import qrcode # This will make a special QR code
    from io import BytesIO
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas as pdf_canvas  # Alias to avoid conflict
    from reportlab.lib import colors # Colors for styling
    from reportlab.platypus import Table, TableStyle  # To make tables look nice
    from PIL import Image
    import os

    def save_pdf_with_qr():
        #travel planner logo
        logo_path = os.path.join(current_dir, "travel_planner_logo.jpg")

        # Create the PDF where we will write the ticket
        c = pdf_canvas.Canvas(pdf_filename, pagesize=letter)
        page_width, page_height = letter

        # Write the title in big letters
        title_text = "Thank You for choosing Travel Planner"
        c.setFont("Helvetica-Bold", 20)
        title_width = c.stringWidth(title_text, "Helvetica-Bold", 20)
        c.drawString((page_width - title_width) / 2, page_height - 50, title_text)

        # Put the logo in the PDF
        logo_width = page_width * 0.2  # Make the logo small
        logo_height = logo_width
        logo_y_position = page_height - logo_height - 120
        c.drawImage(
            logo_path,
            x=50,  # Place the logo on the left
            y=logo_y_position,
            width=logo_width,
            height=logo_height,
            preserveAspectRatio=True,
            mask="auto",
        )

        # We want to show the travel details in a table format
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

        # This is how I make the table look good
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

        # Now let's draw the table in the PDF
        y_position = page_height - logo_height - 300
        travel_table.wrapOn(c, page_width, page_height)
        travel_table.drawOn(c, (page_width - table_width) / 2, y_position)

        # Now, let's create a QR code that you can scan!
        qr_data = f"Booking ID: {booking_id}\nFrom: {from_city}\nTo: {to_city}\nSeats: {', '.join(selected_seats)}\nTotal Price: £{total_price}"
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code as an image
        temp_qr_path = "temp_qr_code.png"
        qr_img.save(temp_qr_path)

        temp_qr_path = "temp_qr_code.png"
        qr_img.save(temp_qr_path)

        # Put the QR code into the PDF
        y_position -= 150 
        c.drawImage(temp_qr_path, (page_width - 100) / 2, y_position, width=100, height=100)

        # Add a little note under the QR code
        y_position -= 50 
        c.setFont("Helvetica", 12)
        c.drawString(
            (page_width - 400) / 2,
            y_position,
            "This is your booking QR code. Please scan it at the departure."
        )

        c.save() # Save the PDF
        os.remove(temp_qr_path) # don't need the QR code image anymore
        messagebox.showinfo("PDF Saved", f"Your ticket invoice has been saved as '{pdf_filename}'.")

    # Let's create a new window to show the ticket information  
    invoice_window = tk.Tk()
    invoice_window.title("Ticket Invoice")
    invoice_window.geometry("2000x1000")
    invoice_window.configure(bg="#F5F5F5")

    # Add the title "Ticket Invoice"
    tk.Label(
        invoice_window,
        text="Ticket Invoice",
        font=("Time New Roman", 36, "bold"),
        bg="#F5F5F5",
        fg="black"
    ).pack(pady=20)

    # Now, let's add the ticket details to the window
    invoice_frame = tk.Frame(invoice_window, bg="white", relief="solid", bd=2)
    invoice_frame.pack(pady=20, padx=100, fill="x")

    # Show each line of the ticket details
    for idx, line in enumerate(invoice_text.strip().split("\n")):
        tk.Label(
            invoice_frame,
            text=line,
            font=("Time New Roman", 18),
            bg="white",
        ).grid(row=idx, column=0, sticky="w", padx=20, pady=5)

    # Add the "Save as PDF" button
    save_pdf_button = tk.Button(
        invoice_window,
        text="Save as PDF 🖨️",
        font=("Time New Roman", 20, "bold"),
        bg="green",
        fg="white",
        command=save_pdf_with_qr
    )
    save_pdf_button.pack(pady=20)

    # Add the "Close" button
    close_button = tk.Button(
        invoice_window,
        text="Close 🛑",
        font=("Time New Roman", 20, "bold"),
        bg="#DC3545",
        fg="white",
        command=invoice_window.destroy
    )
    close_button.pack(pady=10)

    invoice_window.mainloop() # Keep the window open

# Now, we create the main window where people can start the app
root = tk.Tk()
root.title("Welcome to Travel Planner")
root.geometry("2000x1000") # Big window size 

# Add a background image (a nice picture for the main page)
bg_image_path = os.path.join(current_dir, "welcome_bg.jpg")
bg_image = Image.open(bg_image_path)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Add the background image to the canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Show the welcome message
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

# Add a small instruction to tell people to click start
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

# Add a "Start" button that will start the app
start_button = tk.Button(
    root,
    text="Start 🚀",
    command=start_application, # This is the function that starts the app
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

# Move everything around when the window size changes
def reposition_widgets(event=None):
    """Reposition widgets dynamically based on the canvas size."""
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Reposition the welcome label, instruction, and button in the center
    canvas.coords(canvas_window_welcome, canvas_width // 2, canvas_height // 4)
    canvas.coords(canvas_window_instruction, canvas_width // 2, canvas_height // 2)
    canvas.coords(canvas_window_button, canvas_width // 2, (canvas_height // 4) * 3)

root.bind("<Configure>", lambda event: (resize_background(event), reposition_widgets(event)))

resize_background() # Resize the background image
reposition_widgets() # Reposition all widgets

# Start the main window loop
try:
    root.mainloop()
except Exception as e:
    # Show an error if something breaks
    messagebox.showerror("Application Error", f"An unexpected error occurred: {str(e)}")
    # Log the error into a file
    with open("error_log.txt", "a") as error_file:
        # Log the error
        error_file.write(f"{datetime.now()} - root.mainloop: {str(e)}\n")