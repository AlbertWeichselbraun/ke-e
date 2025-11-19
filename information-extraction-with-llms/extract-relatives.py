#!/usr/bin/env python3

from inscriptis import get_text
from json import loads, dumps
from pathlib import Path
import json
from groq import Groq

WIKI_CACHE_PATH = Path("./wikipages")
RESULT_PATH = Path("./results")
API_KEY = Path(".apikey").read_text(encoding="utf-8").strip()
MAX_CHARS = 20000  # Roughly 5000 tokens


PROMPT_TEMPLATE = """Extract all family members of {character_name} from the following wiki page:

# Wiki Page Content
{wikipage}

# Output Format
Return ONLY a JSON array (no extra text) of objects:
[
  {{"name": "<Full Name>", "relationship": "<Relationship to Character>"}}
]
"""


def call_groq(prompt):
    client = Groq(api_key=API_KEY)
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    return resp.choices[0].message.content


def extract_background_information(character_name: str, wikipage_html: str):
    prompt = PROMPT_TEMPLATE.format(
        character_name=character_name,
        wikipage=get_text(wikipage_html)[:MAX_CHARS],
    )
    raw = call_groq(prompt)

    try:
        data = json.loads(raw)
        # Accept either direct list or object containing list
        if isinstance(data, list):
            result = data
        else:
            result = (
                data.get("results") or data.get("family") or data.get("members") or data
            )
    except json.JSONDecodeError:
        result = {"raw": raw}

    RESULT_PATH.mkdir(exist_ok=True)
    out_file = RESULT_PATH / (character_name.replace(" ", "_") + ".json")
    out_file.write_text(dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {out_file}")


def main():
    RESULT_PATH.mkdir(exist_ok=True)
    for page in WIKI_CACHE_PATH.glob("*.json"):
        character = loads(page.read_text(encoding="utf-8"))
        extract_background_information(
            character_name=character["name"],
            wikipage_html=character["wiki_page"],
        )

if __name__ == "__main__":
    main()
