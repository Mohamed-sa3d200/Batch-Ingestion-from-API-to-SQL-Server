import requests
import time
from config import *

def fetch_with_retry(url):

    for attempt in range(MAX_RETRIES):

        try:
            r = requests.get(
                url,
                timeout=10
            )

            r.raise_for_status()

            return r.json()

        except Exception:

            time.sleep(2)

    raise Exception("API Failed")



def fetch_paginated_data():

    all_records=[]

    page=1

    while True:

        url = (
            f"{API_URL}"
            f"?_page={page}"
            f"&_limit={PAGE_SIZE}"
        )

        data = fetch_with_retry(url)

        if not data:
            break

        all_records.extend(data)

        page +=1

    return all_records