import requests
from datetime import date
'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''
API_GET_URL = "https://api.nasa.gov/planetary/apod?api_key=A34XmIKhgiFEERsIDpSUIxGuNThWYMsNCSARb9wV"

def main():
    # TODO: Add code to test the functions in this module
    get_apod_info("2023-04-23")
    return

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    date = f"{API_GET_URL}&date={apod_date}"
    resp_msg = requests.get(date)
    if resp_msg.status_code == requests.codes.ok:
        print('\n','Congratulations, the data has been fetched successfully', '\n')
        get_apod_image_url(resp_msg.json())
        return resp_msg.json()
    else:
        print('\n','Failure, No such data is available','\n')
        print('\n',f'Error Code : {resp_msg.status_code}, Reason For Error : {resp_msg.reason}', '\n')
    return   

def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """
    apod_url = apod_info_dict.values()
    apod_url = list(apod_url)
    return apod_url[-1]

if __name__ == '__main__':
    main()