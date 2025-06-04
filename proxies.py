import pandas as pd
import requests
from io import StringIO

def fetch_proxies():
    url = "https://vakhov.github.io/fresh-proxy-list/proxylist.csv"

    # Download the CSV content
    response = requests.get(url)
    response.raise_for_status()  # Raise error if download fails

    # Load CSV into DataFrame
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data, sep=';')

    # Filter for specific countries
    target_countries = ['United States', 'United Kingdom', 'Finland', 'Netherlands']
    filtered_df = df[df['country_name'].isin(target_countries)]

    # Extract (ip, port) pairs
    proxy_list = list(zip(filtered_df['ip'], filtered_df['port']))

    return proxy_list
