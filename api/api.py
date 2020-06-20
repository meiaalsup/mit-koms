from flask import Flask
from .QueryEngine import QueryEngine

app = Flask(__name__)

# Maps names to Strava URLs
QUERY_MAP = {
    'miles': "https://www.strava.com/athletes/336687/segments/leader",
    'lee': "https://www.strava.com/athletes/15315238/segments/leader",
    'jacob': "https://www.strava.com/athletes/22087315/segments/leader",
}

# Names to query and cache data for
NAMES = ['miles', 'lee', 'jacob']

# Cache that stores recently-fetched results
results_cache = {}

# Engine for querying Strava
engine = QueryEngine(QUERY_MAP)
# initially populate the cache
for name in NAMES:
    koms = engine.query(name)
    results_cache[name] = koms


def query_and_add_name_to_cache(name):
    results_cache[name] = engine.query(name)


@app.route('/koms')
def koms():
    results = {}
    for name in NAMES:
        # cache miss -- query
        if name not in results_cache.keys():
            query_and_add_name_to_cache(name)

        results[name] = results_cache[name]
    return results
