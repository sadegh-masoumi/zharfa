"""
Router Model
"""
from fastapi import APIRouter
from communication.cache import Cache
from src.model import HTreeFilter

router = APIRouter()


@router.get("/gene/htree")
def htree():
    data = Cache.get_all_clusters()

    res = {
        "data": data,
    }
    return res


@router.get("/gene/filter")
def htree_filter(data: HTreeFilter):
    ids = Cache.geo_search(*data.rectangle)
    ids = map(lambda x:int(float(x[0].decode())), ids)

    cluster = Cache.get_all_clusters()[str(data.cluster_id)]

    res = set(cluster).intersection(set(ids))
    return res
