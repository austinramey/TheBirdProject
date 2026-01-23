from ast import List
import http.client
import string
import requests

apiKey = "7gbjkc0cts6j"


class HotspotInfo:
    countryCode = "US"
    localeCode = "US-TX"

    def __init__(self, locationCode, coord1, coord2, commonName):
        self.locationCode = locationCode
        self.coord1 = coord1
        self.coord2 = coord2
        self.commonName = commonName


def main():
    print(f"Api key is: {apiKey}")
    hotspotInfo = {}

    # url = "https://api.ebird.org/v2/ref/region/list/subnational2/US-TX-439"
    url = "https://api.ebird.org/v2/ref/hotspot/US-TX-439"

    payload = {}
    headers = {"X-eBirdApiToken": apiKey}

    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    locationsList = response.text.split("\n")
    for i, n in enumerate(locationsList):
        # print(f"{i}: {n}")

        if n != "":
            locationInfo = n.split(",")
            hotspotInfo[locationInfo[0]] = HotspotInfo(
                locationInfo[0], locationInfo[4], locationInfo[5], locationInfo[6]
            )
            print(f"{i}: {locationInfo}")

    for key, value in hotspotInfo.items():
        if ((float(value.coord1) > 32.822076) & (float(value.coord1) < 32.870591)) & (
            (float(value.coord2) < -97.506151) & (float(value.coord1) > -97.439976)
        ):
            print(f"{key}: {value.commonName} | {value.locationCode}")


if __name__ == "__main__":
    main()
