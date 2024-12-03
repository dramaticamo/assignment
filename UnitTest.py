import unittest

def sort_seat_prices(prices, seats):
    """Sort seat prices in ascending order and sort seats accordingly."""
    sorted_prices, sorted_seats = zip(*sorted(zip(prices, seats)))
    return sorted_prices, sorted_seats

def calculate_total_price(prices):
    """Calculate total price by summing the prices."""
    return sum(prices)

def confirm_booking(from_city, to_city, travel_type, selected_seats, total_price):
    """Confirm the booking and return a booking summary."""
    booking_details = f"""
Booking Confirmed! 🎉
-----------------------
Travel Type: {travel_type}
From: {from_city}
To: {to_city}
Selected Seats: {', '.join(selected_seats)}
Total Price: £{total_price}
"""
    return booking_details.strip()

def generate_ticket_invoice(from_city, to_city, travel_type, selected_seats, total_price):
    """Generate a ticket invoice as text and PDF."""
    invoice_text = f"""
-------------------------
Ticket Invoice
-------------------------
From: {from_city}
To: {to_city}
Travel Type: {travel_type}
Selected Seats: {', '.join(selected_seats)}
Total Price: £{total_price}
Thank you for booking with Travel Planner!
-------------------------
"""
    return invoice_text.strip()

class TestTravelPlanner(unittest.TestCase):

    def test_sort_seat_prices(self):
        """Test if the seats are sorted based on the prices."""
        prices = [100, 50, 150, 120]
        seats = ["A1", "B1", "C1", "D1"]
        
        expected_prices = [50, 100, 120, 150]
        expected_seats = ["B1", "A1", "D1", "C1"]
        
        sorted_prices, sorted_seats = sort_seat_prices(prices, seats)
        
        self.assertEqual(list(sorted_prices), expected_prices)
        self.assertEqual(list(sorted_seats), expected_seats)

    def test_calculate_total_price(self):
        """Test if the total price is calculated correctly."""
        prices = [100, 50, 120]
        expected_total = 270
        
        total_price = calculate_total_price(prices)
        
        self.assertEqual(total_price, expected_total)

    def test_confirm_booking(self):
        """Test if the booking confirmation returns the correct summary."""
        from_city = "London"
        to_city = "Paris"
        travel_type = "Round-trip"
        selected_seats = ["A1", "B2"]
        total_price = 250
        
        expected_summary = """
Booking Confirmed! 🎉
-----------------------
Travel Type: Round-trip
From: London
To: Paris
Selected Seats: A1, B2
Total Price: £250
"""
        
        booking_summary = confirm_booking(from_city, to_city, travel_type, selected_seats, total_price)
        
        self.assertEqual(booking_summary.strip(), expected_summary.strip())

    def test_generate_ticket_invoice(self):
        """Test if the ticket invoice is generated correctly."""
        from_city = "London"
        to_city = "Paris"
        travel_type = "Round-trip"
        selected_seats = ["A1", "B2"]
        total_price = 250
        
        expected_invoice = """
-------------------------
Ticket Invoice
-------------------------
From: London
To: Paris
Travel Type: Round-trip
Selected Seats: A1, B2
Total Price: £250
Thank you for booking with Travel Planner!
-------------------------
"""
        
        invoice = generate_ticket_invoice(from_city, to_city, travel_type, selected_seats, total_price)
        
        self.assertEqual(invoice.strip(), expected_invoice.strip())

if __name__ == '__main__':
    unittest.main()
