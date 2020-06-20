from flask import Flask
from .QueryEngine import QueryEngine
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Maps names to Strava URLs
QUERY_MAP = {
    'Miles': "https://www.strava.com/athletes/336687/segments/leader",
    'Lee': "https://www.strava.com/athletes/15315238/segments/leader",
}

# Cache that stores recently-fetched results
results_cache = {}


def refresh_cache():
    print("Refreshing cache")
    for name in QUERY_MAP.keys():
        koms = engine.query(name)
        results_cache[name] = koms


# Engine for querying Strava
engine = QueryEngine(QUERY_MAP)
# initially populate the cache
refresh_cache()


def query_and_add_name_to_cache(name):
    results_cache[name] = engine.query(name)


# Schedule a cache refresh every 30 minutes so Strava
# doesn't block whatever random linux box this is running on.
# Don't query on pageload because Strava is so so so slow
scheduler = BackgroundScheduler()
scheduler.add_job(func=refresh_cache, trigger="interval", seconds=1800)
scheduler.start()


@app.route('/koms')
def koms():
    results = {}
    for name in QUERY_MAP.keys():
        # cache miss -- query
        if name not in results_cache.keys():
            query_and_add_name_to_cache(name)

        results[name] = results_cache[name]
    return results
