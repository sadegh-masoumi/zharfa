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
    # {"x": len([('12:00', 5), ('12:02', 5)])}
    # ["12:05":]
    # ["12:05", "12:06", "12:10", 4]

    ids = Cache.geo_search(*data.rectangle)
    ids = map(lambda x:int(float(x[0].decode())), ids)

    cluster = Cache.get_all_clusters()[str(data.cluster_id)]

    res = set(cluster).intersection(set(ids))
    return res
