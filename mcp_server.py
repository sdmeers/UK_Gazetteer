from fastmcp import FastMCP
from gazetteer_client import GazetteerClient
from typing import Optional, Dict

# Initialize FastMCP with a server name
mcp = FastMCP("Gazetteer MCP Server")

# Instantiate the client for our gazetteer API
gazetteer_client = GazetteerClient()

@mcp.tool
def get_lat_long(placename: str, county: Optional[str] = None) -> Optional[Dict[str, float]]:
    """
    Gets the latitude and longitude for a UK place name.

    Args:
        placename: The name of the place to look up.
        county: Optional: The county to filter the search by.

    Returns:
        A dictionary with 'latitude' and 'longitude' of the first match,
        or None if the place is not found.
    """
    print(f"MCP Tool: Looking up coordinates for '{placename}'...")
    
    try:
        results = gazetteer_client.get_long_lat(placename, county)
        
        if results:
            first_result = results[0]
            lat = first_result['lat']
            lng = first_result['lng']
            print(f"MCP Tool: Found '{first_result['placename']}'. Returning coordinates.")
            return {"latitude": lat, "longitude": lng}
        else:
            print("MCP Tool: Place not found.")
            return None
            
    except Exception as e:
        print(f"An error occurred while contacting the gazetteer API: {e}")
        return None

# Run the FastMCP server
if __name__ == "__main__":
    print("Starting Gazetteer MCP Server...")
    # You may need to specify a host and port, e.g., mcp.run(host="0.0.0.0", port=8001)
    mcp.run()
