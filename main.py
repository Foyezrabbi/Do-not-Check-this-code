import requests, json, os
from bs4 import BeautifulSoup
import urllib.request

headers = {
    'authority': 'nhentai.net',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36 OPR/88.0.4412.85',
}

def panelGrabber(url, download_folder=None):
    with open("cookies.json", "r") as file:
        dumps = json.load(file)
        cookies = {
            "cf_clearance": dumps["cf_clearance"],
            "csrftoken": dumps["csrftoken"]
        }
        response = requests.get(url, cookies=cookies, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    get_panels = soup.find_all("a", {"class":"gallerythumb"})
    
    panel_links = []

    for i in get_panels:
        j = i["href"]
        panel_links.append(j)

    print(f"\nNow Downloading, {url}")

    for i in range(len(panel_links)):
        if download_folder == None:
            panelDownloader(f"https://nhentai.net{panel_links[i]}")
        else:
            panelDownloader(f"https://nhentai.net{panel_links[i]}", download_folder)
    if download_folder == None:
        print("Download Complete, Saved to Current Folder\n")
    else:
        print(f"Download Complete, Saved to {os.path.abspath(download_folder)}\n")

def panelDownloader(urls, download_folder=None):
    with open("cookies.json", "r") as file:
        dumps = json.load(file)
        cookies = {
            "cf_clearance": dumps["cf_clearance"],
            "csrftoken": dumps["csrftoken"]
        }
        response = requests.get(urls, cookies=cookies, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    get_img = soup.find_all("img")[1]
    get_src = get_img["src"]

    first_split = get_src.split(".")
    second_split = first_split[2].split("/")

    if download_folder == None:
        try:
            urllib.request.urlretrieve(get_src, f"./{second_split[2]}-{second_split[3]}.{first_split[3]}")
        except:
            print("\nSomething went wrong, Please try again")
    else:
        try:
            urllib.request.urlretrieve(get_src, f"{download_folder}/{second_split[2]}-{second_split[3]}.{first_split[3]}")
        except:
            print("\nSomething went wrong, Please try again")

    print(f"Download Complete, Panel Page: {second_split[3]}")

if __name__ == "__main__":
    try:
        os.system("cls")
        while True:
            link_input = input("Insert a nHentai manga link: ")
            download_folder = input("Insert a Download destination (optional): ")

            if download_folder == "":
                if "https://nhentai.net" in link_input:
                    panelGrabber(link_input)
                elif "nhentai.net" in link_input:
                    panelGrabber(f"https://{link_input}")
                elif "g/" in link_input:
                    panelGrabber(f"https://nhentai.net/{link_input}")
                else:
                    print("\nUnable to scrape the link, Please try again\n")
            else:
                if "https://nhentai.net" in link_input:
                    panelGrabber(link_input, download_folder)
                elif "nhentai.net" in link_input:
                    panelGrabber(f"https://{link_input}", download_folder)
                elif "g/" in link_input:
                    panelGrabber(f"https://nhentai.net/{link_input}", download_folder)
                else:
                    print("\nUnable to scrape the link, Please try again\n")
    except KeyboardInterrupt:
        print("\nThe program has been stopped")
