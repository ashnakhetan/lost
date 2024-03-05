import os
from util import gpt_extract_locations
from util import search_image_url
from firebase import connect_db
from firebase import save_attraction_db

scraped_data = 'output.txt'
openai_api_key = os.environ.get('OPENAI_API_KEY')
bing_api_key = os.environ.get('BING_API_KEY')

def main():
    # get and crop the images

    # run the ocr scraper on them; save txt into scraped_data

    # make the gpt query
    locations = gpt_extract_locations(scraped_data, openai_api_key).split('\n')
    print(locations)

    connect_db()
    for location in locations:
        # find images from google
        img_url = search_image_url(location, bing_api_key)

        # add destination, location, image to database
        save_attraction_db(location, img_url)
        print("done")

if __name__ == '__main__':
    main()