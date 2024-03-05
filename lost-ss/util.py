import os
import openai
from openai import OpenAI
import requests

def list_files(directory):
    """List only files in the given directory."""
    try:
        file_list = [file for file in os.listdir(directory) 
                     if os.path.isfile(os.path.join(directory, file))]
        return file_list
    except Exception as e:
        return str(e)

def save_file_list_to_txt(directory, output_file):
    """Saves the list of files in the directory to a text file."""
    file_list = list_files(directory)
    with open(output_file, 'w') as file:
        for filename in file_list:
            file.write(directory + '/' + filename + '\n')


# queries gpt to create list of locations
def gpt_extract_locations(file_path, openai_api_key):
    with open(file_path, 'r') as file:
        content = file.read()

    client = OpenAI(api_key=openai_api_key) # should get key by default
    print("here")

    # Make the query to OpenAI
    response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Extract just the location/attraction names from this text. Please respond with just a newline-separated list of the names, with no additional wording. Limit your response to 100 tokens:\n\n" + content,
        }
    ],
    model="gpt-3.5-turbo",
    max_tokens=100,)

    print(response)

    return response.choices[0].message.content.strip()


# query Bing Image Search to get an image of a given location
def search_image_url(search_term, bing_api_key, count=1):
    assert bing_api_key, "Provide your Bing Search V7 subscription key"
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    headers = {"Ocp-Apim-Subscription-Key": bing_api_key}
    params = {"q": search_term, "license": "public", "imageType": "photo", "count": count}
    
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    # get the first result url
    first_result_url = search_results["value"][0]["contentUrl"]

    return first_result_url
    
    # download the image -- may not need
    # image_data = requests.get(first_result_url)
    # image_data.raise_for_status()

    # save the image
    # with open(search_term + ".jpg", "wb") as file:
    #     file.write(image_data.content)
    
    # print(f"Downloaded {search_term}.jpg")







directory_path = 'cropped_images'
output_file_name = 'cropped_images.txt'

save_file_list_to_txt(directory_path, output_file_name)