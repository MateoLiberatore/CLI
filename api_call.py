import logging, requests, json, os
import pandas as pd
from date_managment import date_entry, period
from file_managment import reports_folder
from datetime import datetime





def single_day():
    
    crypto_name = input('Enter a crypto currency name: ')
    coin_name = crypto_name
    date = date_entry()

    # Construct the correct date format as per the API requirements
    formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%d-%m-%Y')

    base_url = f'https://api.coingecko.com/api/v3/coins/{id}/history?date={date}'
    url = base_url.format(id=coin_name, date=formatted_date)

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        api_date = data.get('market_data', {}).get('current_price', {}).get('date')

        df = pd.DataFrame([data])
        df['API_Date'] = api_date

        csv_filename = f'{coin_name}_{formatted_date}.xlsx'  
        df.to_csv(csv_filename, index=False)

        logging.info('Data saved to CSV successfully.')

        return df, crypto_name
    else:
        logging.warning(f'Error in the request: status code: {response.status_code}')




def to_today_report():
    coin_id = input("Enter a crypto coin name: ")
    start_date, end_date = period()

    days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days
    vs_currency = "usd"
    interval = "daily"
    precision = "4"

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={vs_currency}&days={days}&interval={interval}&precision={precision}"

    response = requests.get(url)

    if response.status_code == 200:
        crypto_data = response.json()
        prices = crypto_data.get("prices", [])

        data_list = []

        for price in prices:
            timestamp, price_value = price
            data_dict = {
                "crypto_name": coin_id,
                "timestamp": pd.to_datetime(timestamp, unit='ms'),
                "price": price_value,
                "json": json.dumps(crypto_data)  # Rest of the data in json format column
            }
            data_list.append(data_dict)

        crypto_df = pd.DataFrame(data_list) 

        # Create 'reports' directory if it doesn't exist
        reports_directory = reports_folder()
        if not os.path.exists(reports_directory):
            os.makedirs(reports_directory)

        crypto_df_filtered = crypto_df[(crypto_df['timestamp'] >= pd.to_datetime(start_date)) &
                                       (crypto_df['timestamp'] <= pd.to_datetime(end_date))]

        # Save the CSV file in the 'reports' directory
        csv_filename = f'{start_date}_{end_date}_{coin_id}_report.csv'
        csv_filepath = os.path.join(reports_directory, csv_filename)
        crypto_df_filtered.to_csv(csv_filepath, index=False)

        return crypto_df_filtered
    

def specific_period_report():
    
    coin_id = input("Enter a crypto coin name: ")
    print('Initial date:')
    start_date = date_entry()
    print('Ending date:')
    end_date = date_entry()

    start_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_obj = datetime.strptime(end_date, "%Y-%m-%d")

    start_to_UNIX = int(start_obj.timestamp())
    end_to_UNIX = int(end_obj.timestamp())
    vs_currency = "usd"
    precision = "4"

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id.lower()}/market_chart/range?vs_currency={vs_currency}&from={start_to_UNIX}&to={end_to_UNIX}&precision={precision}"

    response = requests.get(url)

    if response.status_code == 200:
        crypto_data = response.json()

        dates = [datetime.utcfromtimestamp(item[0] / 1000).strftime('%Y-%m-%d') for item in crypto_data['prices']]
        closing_prices = [item[1] for item in crypto_data['prices']]

        df = pd.DataFrame(list(zip(dates, closing_prices)), columns=['Date', 'Closing Price'])

        df = df.drop_duplicates(subset='Date', keep='last')

        start_date_str = start_obj.strftime('%Y-%m-%d')
        end_date_str = end_obj.strftime('%Y-%m-%d')

        reports_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'reports')
        os.makedirs(reports_dir, exist_ok=True) 


        csv_filename = os.path.join(reports_dir, f"{coin_id.lower()}_period_{start_date_str}_to_{end_date_str}_report.csv")
        df.to_csv(csv_filename, index=False)

        print(f"DataFrame saved to {csv_filename}")

    else:
        print(f"Error: {response.status_code}")



    
specific_period_report()