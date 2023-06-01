import requests
import pandas as pd
from bs4 import BeautifulSoup

#Python is best for web scrapping
def scrape_data(phone_number, email):
    platforms = {
        "WhatsApp": {
            "url": f"https://web.whatsapp.com/{phone_number}",
            "selectors": {
                "registered": ('div', {'class': '_1WZqU PNlAR'}),
                "name": ('span', {'class': '_1wjpf'}),
                "username": ('div', {'class': '_1fQZE'}),
                "profile_picture": ('div', {'class': '_2ruVH'}),
                "status": ('div', {'class': '_2hqOq _3xI7T'}),
                "last_seen": ('div', {'class': '_3H4MS'}),
                "upi_id": ('div', {'class': '_1MZWu'}),
                "profile_url": ('div', {'class': '_1zGQT'})
            }
        },
        "Facebook": {
            "url": f"https://www.facebook.com/{phone_number}",
            "selectors": {
                "registered": ('div', {'id': 'fbProfileCover'}),
                "name": ('span', {'class': 'fullname'}),
                "username": ('span', {'class': 'username'}),
                "profile_url": ('meta', {'property': 'og:url'})
            }
        },
        "Truecaller": {
            "url": f"https://www.truecaller.com/search/in/{phone_number}",
            "selectors": {
                "registered": ('a', {'class': 'profile-sidebar-title'}),
                "name": ('h1', {'class': 'profile-title'}),
                "email": ('a', {'class': 'email'})
            }
        },
        "Gpay": {
            "url": f"https://gpay.app.goo.gl/{phone_number}",
            "selectors": {
                "registered": ('div', {'class': 'DfTQ5d'}),
                "name": ('div', {'class': 'DfTQ5d'}),
                "upi_id": ('div', {'class': 'DfTQ5d'})
            }
        }
    }

    output = []
    for platform, data in platforms.items():
        url = data['url']
        selectors = data['selectors']

        response = requests.get(url) # Request to Platform URL
        soup = BeautifulSoup(response.content, 'html.parser')

        attributes = {} # Extraction 
        for attribute, selector in selectors.items():
            element = soup.find(*selector)
            attributes[attribute] = element.text if element else None

        
        output.append({"Platform": platform, **attributes})  # Append attributes

   
    df = pd.DataFrame(output) # Create a DataFrame

    return df

phone_number = "6395135030"
email_address = "ghgoyal121@gmail.com"
df = scrape_data(phone_number, email_address)
print(df)
