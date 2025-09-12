import requests
from typing import Optional, Dict, Any, List

GAZETTEER_API_URL = "http://127.0.0.1:8000/lookup"

class GazetteerClient:
    """
    A client for the UK Gazetteer API.
    """
    def __init__(self, api_url: str = GAZETTEER_API_URL):
        self.api_url = api_url

    def get_long_lat(self, placename: str, county: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Looks up a UK place name and returns a list of matching locations
        with their latitude and longitude.

        Args:
            placename: The name of the place to look up.
            county: Optional: The county to filter the search by.

        Returns:
            A list of dictionaries, where each dictionary represents a found place
            and contains 'placename', 'lat', 'lng', and 'histcounty'.
            Returns an empty list if no match is found.
        
        Raises:
            requests.exceptions.RequestException: If there's a network-level error.
        """
        params = {"placename": placename}
        if county:
            params["county"] = county

        try:
            response = requests.get(self.api_url, params=params)
        
            # If the place is not found, the API returns a 404.
            # We'll return an empty list, which is a common practice.
            if response.status_code == 404:
                return []
                
            response.raise_for_status()  # Raise an exception for other bad status codes

            return response.json()
        except requests.exceptions.ConnectionError as e:
            print(f"Error: Connection to Gazetteer API failed at {self.api_url}. Is the server running?")
            raise e

# Example usage:
if __name__ == "__main__":
    # Make sure to install the new dependency:
    # pip install -r requirements.txt

    client = GazetteerClient()
    
    print("--- Looking up 'Alton' in 'Hampshire' ---")
    results = client.get_long_lat("Alton", "Hampshire")
    if results:
        # Using the first result
        first_result = results[0]
        lat = first_result['lat']
        lng = first_result['lng']
        print(f"Found: {first_result['placename']} -> Lat: {lat}, Lng: {lng}")
    else:
        print("Place not found.")

    print("\n--- Looking up 'Cambridge' ---")
    results_cambridge = client.get_long_lat("Cambridge")
    if results_cambridge:
        print(f"Found {len(results_cambridge)} matches for 'Cambridge'.")
        for place in results_cambridge:
            print(f"- {place['placename']}, {place['histcounty']}")
    else:
        print("No matches found for Cambridge.")
