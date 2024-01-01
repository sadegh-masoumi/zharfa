import logging
import json
import redis

from settings import REDIS_PORT, REDIS_HOST

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s"
)
logger = logging.getLogger("Cache 🗃️")


def calculate_center_and_radius(sw_lon, sw_lat, ne_lon, ne_lat):
    """
    Calculate the center and radius covering the bounding box defined by
    South-West (sw_lon, sw_lat) and North-East (ne_lon, ne_lat) coordinates.
    """
    center_lon = (sw_lon + ne_lon) / 2
    center_lat = (sw_lat + ne_lat) / 2

    radius_lon = abs(ne_lon - sw_lon) / 2
    radius_lat = abs(ne_lat - sw_lat) / 2
    radius = max(radius_lon, radius_lat) * 111  # Convert to kilometers (approximation)

    return center_lon, center_lat, radius


class Cache:
    obj = None

    def __new__(cls, *args, **kwargs):
        if Cache.obj is None:
            obj = super(Cache, cls).__new__(cls)
            Cache.obj = obj
            return obj
        return Cache.obj

    def __init__(self):
        logger.info("Connecting to Redis ... ⌛️")
        self.client = redis.Redis(port=REDIS_PORT, host=REDIS_HOST, db=0)
        logger.info("Connected to Redis ✅")

    @staticmethod
    def set_clusters(data: dict):
        validated_data = json.dumps(data)
        Cache.obj.client.set("data", validated_data)

    @staticmethod
    def get_all_clusters(key="data"):
        data = Cache.obj.client.get(key)
        return json.loads(data)

    @staticmethod
    def store_lat_long(key, long, lat):
        Cache.obj.client.geoadd("locations", (lat, long, key))

    @staticmethod
    def geo_search(sw_lon, sw_lat, ne_lon, ne_lat, unit="km"):
        center_lon, center_lat, radius = calculate_center_and_radius(
            sw_lon, sw_lat, ne_lon, ne_lat
        )
        return Cache.obj.client.georadius(
            "locations", center_lon, center_lat, radius, unit, withcoord=True
        )
