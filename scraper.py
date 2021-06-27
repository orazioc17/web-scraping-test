# Python dependencies
import pathlib
import datetime
from os import close, path
import os
import requests
import lxml.html as html
import json

# Constants created in another file
from constants import HOME_URL,XPATH_BITCOIN_PAGE, XPATH_NODES, VALUES_LIST, SAVED_JSON, TEMPORARY_JSON


# Function to convert from list to string
def convert_array(array):
    return ''.join(array)


# Prints data obtained with format json
def print_json(data):
    print(f'Data obtained: {json.dumps(data, indent=4)}')


def save_data(data, time):
    """"Overwrite json if exists or create it"""
    actual_dir = os.listdir(pathlib.Path.cwd())

    # Gets the actual json if it exists, then write the old data with the new data
    # In another file, delete the older and rename the new, so it "overwrite" the original file
    if SAVED_JSON in actual_dir:
        with open(SAVED_JSON, 'r') as f:

            saved_data = json.load(f)
            f.close()

            data_to_save = saved_data
            data_to_save['values'].append({f'{time}': data})

            with open(TEMPORARY_JSON, 'w') as file:
                json.dump(data_to_save, file, indent=4)
                file.close()

                os.remove(SAVED_JSON)
                os.rename(TEMPORARY_JSON, SAVED_JSON)
            
    else:
        with open(SAVED_JSON, 'w') as f:
            data_to_save = {}
            data_to_save['asset'] = 'BTC'
            data_to_save['values'] = []
            data_to_save['values'].append({f'{time}': data})
            json.dump(data_to_save, f, indent=4)
            f.close()


# Obtaining every value from bitcoing page
def parse_bitcoin(link):
    """Scraping the requested data"""
    response = requests.get(link)
    try:
        if response.status_code == 200:
            bitcoin_page = response.content.decode('utf-8')
            parsed = html.fromstring(bitcoin_page)
            data = dict()
            data['Obtained'] = datetime.datetime.now().strftime('Day: %d-%m-%Y Hour: %H:%M:%S')
            # Using Values list to create every value in the dictionary
            for index, value in enumerate(VALUES_LIST):
                # Converting from lists to string every text found and inserting them into the dict
                data[value] = convert_array(parsed.xpath(XPATH_NODES[index]))
            # Saving the time this  data was obtained
            data['Obtained'] = datetime.datetime.now().strftime('Day: %d-%m-%Y Hour: %H:%M:%S')
            return data
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    """Function to obtain Bitcoin page link"""
    response = requests.get(HOME_URL)
    try:
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            link = convert_array(parsed.xpath(XPATH_BITCOIN_PAGE))
            # Adding the bitcoin path to the home url
            bitcoin_link = HOME_URL + link
            return bitcoin_link
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    """Controls the flow of the program"""
    link_to_bitcoin_page = parse_home()
    data = parse_bitcoin(link_to_bitcoin_page)
    print_json(data)
    time = data['Obtained']
    save_data(data, time)


if __name__ == '__main__':
    run()