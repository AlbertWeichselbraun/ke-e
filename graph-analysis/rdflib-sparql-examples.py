from rdflib import Graph

g = Graph()


print("Example 1: Query Wikidata for countries of the European Union")
QUERY = '''
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>

SELECT
  ?country ?countryLabel
WHERE {
  SERVICE <https://query.wikidata.org/sparql>
     {
        wd:Q458 wdt:P150 ?country .   # European Union  contains administrative territorial entity
        ?country rdfs:label ?countryLabel .
        FILTER (lang(?countryLabel) = "en")
     }
}
LIMIT 50
'''
for no, (country, country_label) in enumerate(g.query(QUERY), start=1):
    print(no, country, country_label)


print("\nExample 2: Query DBpedia for Swiss Cantons.")
QUERY = '''
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
SELECT DISTINCT ?canton_name ?canton_region_code
WHERE {
  SERVICE <https://dbpedia.org/sparql>
    {
       ?canton dbo:type dbr:Cantons_of_Switzerland;
               rdfs:label ?canton_name;
               dbo:isoCodeRegion ?canton_region_code.
        FILTER (lang(?canton_name) = 'de')
    }
}
LIMIT 50
'''
no = 1
for name, region_code in sorted(g.query(QUERY)):
    if not name.startswith('Kanton '):
        continue
    print(no, name, region_code)
    no += 1
