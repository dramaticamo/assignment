# APP NAME
**"Travel Planner"**

# GitHub Repository
The source code for this project is available on GitHub: https://github.com/xxyy

## Identification
- **Name: Aung Myo Oo** 
- **P-number: P-462183** 
- **Course code: IY499** 

## Declaration of Own Work
I confirm that this assignment is my own work.
Where I have referred to academic sources, I have provided in-text citations and included the sources in the final reference list.

## Introduction
The **Travel Planner** app is designed to help users easily plan and book their trips. With a simple and friendly interface, users can choose their travel route, pick seats, and confirm bookings. The app shows seat prices, allowing users to select the best options. After booking, users get a detailed ticket with all the information, including a unique QR code for easy access. The ticket can be saved as a **PDF** or **text** file. Built with **Tkinter**, **ReportLab**, and **QRcode**, the Travel Planner makes booking trips quick, easy, and hassle-free.

## Installation
To run this application, you will need Python 3.x installed. Then, install the required dependencies using the requirements.txt file with the following command:
```bash
pip install -r requirements.txt
```

## How to Use
- Start by opening the "Travel Planner" application. Once it has loaded, click the "Start" button to begin planning your trip.
- You will be prompted to select your travel type. Choose your departure city and destination city based on your travel needs.
- After you've made your selection, click "Find Your Routes" to view the available routes for your chosen cities.
- After that, you will see options for flights, trains, and coaches. Click on the type of transportation you wish to use, 
- then click "Confirm Routes" to go to the next step.
- Next, you will reach the details section, where you can view the ticket purchase date, departure and arrival locations, operator name, and choose your preferred travel time (morning, afternoon, or evening).
- You can also select the number of passengers (minimum 1, maximum 3), choose whether they are adults or kids (with kids receiving a 40% discount), and select either business class or economy class.
- Then, you can select your preferred seats. If you chose business class on the previous page, you cannot select economy class, and vice versa.
- Afterward, you will see the ticket price. If you are satisfied, click "Confirm Booking" to proceed.
- The ticket invoice will appear next, where you can review all the details of your booking.
- You can view or save your ticket invoice in either PDF or text format for easy access. Click "Save as PDF" if you want to save it in PDF format.
- You can also see the QR code in the PDF view. You can either save or take a screenshot of the QR code. Remember to scan it at the departure location.
- The process is very simple and user-friendly, making trip planning easy!

### Running the Application
To start the Travel Planner, run the "main.py" file:
```bash
python main.py
```

### Running Unit Tests
To test the functionalities of the program, run the unit tests with the following command:
```bash
python UnitTest.py
```

## Application Elements
- Seat Selection: Users can select seats with different prices.
- Booking Confirmation: The application confirms the user's booking and displays a summary.
- Ticket Generation: Users can save or view their ticket in text or PDF format.

## Libraries Used
The following libraries are used in this project:

- Tkinter: Used to build the graphical user interface.
- ReportLab: For generating PDF invoices.
- qrcode: To create QR codes for tickets.
- Pillow (PIL): For handling images.

## Project Structure
- `ErrorHandling/`: Contains classes for managing errors during seat selection or booking.
- `FileHandling/`: Handles the saving and loading of ticket data and user configurations.
- `SortingAlgorithm/`: Sorts seat prices and manages seat selection based on availability.
- `images/`: Stores images used for the GUI (e.g., background, logos).
- `levels/`: Contains different levels or stages for booking.
- `menu/`: Handles the main menu and user input for trip planning.
- `screen/`: Manages how the application displays information to the user.
- `UnitTest.py`: Contains unit tests for the Travel Planner functionality (e.g., seat sorting, price calculation).

## Unit Tests (optional)
The project includes a unit test suite in the `UnitTest.py` file. These tests cover various aspects of the game, including game loop calculations, collision detection, score calculation, and more.

To run the unit tests, navigate to the project directory and execute the following command:

```python
python UnitTest.py
```

This will run all the test cases defined in the `UnitTest.py` file."#assignment" 
