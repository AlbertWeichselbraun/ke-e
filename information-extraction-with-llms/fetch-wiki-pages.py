#!/usr/bin/env python3

import rdflib
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import quote
from json import dumps
import time

WIKI_URL_TEMPLATE = "https://harrypotter.fandom.com/wiki/{formatted_name}"
WIKI_CACHE_PATH = Path("./wikipages")


def get_characters(ontology_file):
    """Extract all characters from the graph."""
    g = rdflib.Graph()
    g.parse(ontology_file, format="turtle")

    ex = rdflib.Namespace("http://weichselbraun.net/kee/2025/harry-potter#")

    # Query for all instances of Character class
    query = """
    PREFIX ex: <http://weichselbraun.net/kee/2025/harry-potter#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?character ?label
    WHERE {
        ?character a ex:Character .
        ?character rdfs:label ?label .
    }
    """
    results = g.query(query)
    return [(str(row.character), str(row.label)) for row in results]


def fetch_wiki_page(character_name):
    """Fetch the Harry Potter wiki page for a character."""
    # Format the character name for the URL
    formatted_name = character_name.replace(" ", "_")
    url = WIKI_URL_TEMPLATE.format(formatted_name=quote(formatted_name))

    with urlopen(url) as response:
        if response.status == 200:
            content = response.read().decode("utf-8")
            return content


def main():
    # Load the turtle file
    turtle_file = "harry-potter.ttl"

    # Get all characters
    characters = get_characters(ontology_file=turtle_file)
    print(f"Found {len(characters)} characters\n")

    # Fetch and cache wiki pages
    WIKI_CACHE_PATH.mkdir(exist_ok=True)
    for uri, label in characters:
        print(f"Character: {label}")
        print(f"URI: {uri}")

        content = fetch_wiki_page(label)
        if content:
            print(
                f"Fetched wiki page for {label} (length: {len(content)} characters)\n"
            )
            with open(WIKI_CACHE_PATH / (label + ".json"), "w", encoding="utf-8") as f:
                f.write(
                    dumps({"name": label, "uri": uri, "wiki_page": content}, indent=2)
                )
        else:
            print(f"Failed to fetch wiki page for {label}\n")
        # Be respectful to the server - add a small delay
        time.sleep(1)


if __name__ == "__main__":
    main()
