from datetime import datetime
from datetime import timedelta

def date_entry():
    while True:
        date_input = input('Enter a valid date (YYYY-MM-DD): ')
        try:
            datetime.strptime(date_input, '%Y-%m-%d')
            return str(date_input)
        except ValueError:
            print('Invalid date format. Please enter a date in the format YYYY-MM-DD.')

def period():
    
    day_amount = int(input("Enter how many days long will be the period: "))
    start = datetime.now()
    end = start - timedelta(days=day_amount)

    start, end = min(start, end), max(start, end)

    # Convert the datetime objects to strings in the format '%Y-%m-%d'
    start_str = start.strftime('%Y-%m-%d')
    end_str = end.strftime('%Y-%m-%d')

    return start_str, end_str
