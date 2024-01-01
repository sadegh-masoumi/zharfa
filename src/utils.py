import logging
from communication.cache import Cache

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s"
)
logger = logging.getLogger("Start Up 🏁")


def start_up():
    import pandas as pd
    from sklearn.cluster import KMeans
    import numpy as np

    logger.info("Loading Gene file ...⌛️")

    df = pd.read_csv("./data/gene.csv")
    logger.info("Gene file loaded ✅")

    def get_labels(data_pc):
        model = KMeans(n_clusters=2, n_init=5)
        model.fit(data_pc)
        return np.array(model.labels_)

    res = dict()

    def hcd(df, id):
        if len(df) > 1:
            labels = get_labels(df[["PC1", "PC2", "PC3"]])
            one = df[labels == 1]
            zero = df[labels == 0]
            res[id] = zero.ID.values.tolist()
            res[id + 1] = one.ID.values.tolist()
            hcd(one, id + 2)
            hcd(one, id + 2)

    hcd(df, 0)

    logger.info("Cache On redis 🗂️")
    client = Cache()
    client.set_clusters(res)

    for ID, lat, long in df[["ID", "Lat", "Long"]].values:
        Cache.store_lat_long(key=ID, lat=lat, long=long)

    logger.info("Cached On redis ✅")
