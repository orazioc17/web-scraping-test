# Python dependencies
import datetime
from os import close
import requests
import lxml.html as html
import json

# Constants created in another file
from constants import HOME_URL,XPATH_BITCOIN_PAGE, XPATH_NODES, VALUES_LIST


# Function to convert from list to string
def convert_array(array):
    return ''.join(array)


# Prints data obtained with format json
def print_json(data):
    print(f'Data obtained: {json.dumps(data, indent=4)}')


# Adds the data to the json file
def save_data(data, time):
    """Function to save the data in json format"""
    with open(f'{time}.json', 'a') as f:
        json.dump(data, f, indent=4)
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
    link_to_bitcoin_page = parse_home()
    data = parse_bitcoin(link_to_bitcoin_page)
    print_json(data)
    time = data['Obtained']
    save_data(data, time)


if __name__ == '__main__':
    run()