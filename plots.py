import matplotlib.pyplot as plt
import pandas as pd
from file_managment import find_file, scan_files
 

def plot():

    file_names_to_search = scan_files() 
    
    if len(file_names_to_search) > 1:
        

    else: 
        print("Archivo encontrado:", file_names_to_search)
        df = pd.read_csv(file_names_to_search)


        bitcoin_data = df[df['crypto_name'] == 'bitcoin']

        plt.figure(figsize=(10, 6))
        plt.plot(bitcoin_data['timestamp'], bitcoin_data['price'], marker='o', color='b')

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(f'{crypto_currency} Price Over Time')
        plt.xticks(rotation=45)

        plt.savefig('bitcoin_price.pdf')

        plt.tight_layout()
        plt.show()