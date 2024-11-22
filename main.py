# Import packages
import requests as rq
import pandas as pd
import re
import time

# Start timer
start = time.time()

# Set base URL
url = 'https://pokeapi.co/api/v2/pokemon/'

# Create empty list item to store response
extract = []

# Iterate whilst there is a 'next' URL
while url:
    response = rq.get(url)
    data = response.json()
    total = data.get("count")

    # First iteration
    if 'offset' not in url:
        start_id = 1
        end_id = 20
    # Consequent iterations - extract elements from URL to create 'fetching data from' message
    else:
        start_id = int(re.search('offset=([0-9]+)', url).group(1))+1
        end_id = int(start_id) + int(re.search("limit=([0-9]+)", url).group(1)) - 1

    # Message to show which results are being returned
    print(f"Fetching data from items #{start_id} to #{end_id} in a list of {total}...")

    # Loop through results to extract JSON elements
    for pokemon in data.get("results"):
        name = pokemon.get("name")
        detail_url = pokemon.get("url")
        print(f"Grabbing additional information for {name} at: {detail_url}")

        # Pull more detail from individual endpoint
        detail = rq.get(detail_url).json()
        base_experience = detail.get("base_experience")
        weight = detail.get("weight")
        height = detail.get("height")

        # Add all extracted elements to empty list
        extract.append({
            "name": name,
            "base_experience": base_experience,
            "weight": weight,
            "height": height
        })

    # Set URL to 'next' value for pagination
    url = data.get("next")

print("Creating dataframe!")

# Create dataframe
df = pd.DataFrame(extract)

# Output csv - next to script
df.to_csv(path_or_buf="./pokemon_dump.csv", mode="w", header=True, index=False)

# End timer
end = time.time()

# Calculate and print elapsed time
elapsed = round(end-start)
print(f"Script ran in {elapsed}s!")