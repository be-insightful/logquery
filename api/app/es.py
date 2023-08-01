from datetime import datetime, date

from elasticsearch import Elasticsearch
from app.models import Parameter, Condition, Period, LastData
from app.config import ES_Settings
from app.applog import logger


# get es config
es_config = ES_Settings()

# es instance generate
es = Elasticsearch(
    hosts=[es_config.host],
    http_auth=(es_config.appuser, es_config.password),
    schema="https",
)

# make period field of dict type
def get_period(period: Period) -> dict:
    if period.all is False:
        range = {
            "gte": period.startdate,
            "lte": period.enddate,
        }
        return range
    elif period.all is True:
        return None


# make condition field of dict type
def get_condition(condition: Condition) -> dict:
    if condition.all is False:
        for k, v in condition:
            if (v is not None) and (k == "contents"):
                # result = {
                #     "should": [
                #         {"wildcard": {"eventmsg.m.ngram": {"value": f"*{v}*"}}},
                #         {"wildcard": {"eventmsg.v.ngram": {"value": f"*{v}*"}}},
                #     ]
                # }

                result = {
                    "should": [
                        {"match_phrase": {"eventmsg.m.ngram": v}},
                        {"match_phrase": {"eventmsg.v.ngram": v}},
                    ]
                }

                return result
            elif (v is not None) and (k != "all"):
                # result = {"wildcard": {f"{k}.ngram": {"value": f"*{v}*"}}}
                result = {"match_phrase": {f"{k}.ngram": v}}
                return result
                # return {"match": {k: v}}
    elif condition.all is True:
        return None


# make query body
def get_query_body(parameter: Parameter) -> dict:
    # variables define
    must = []
    should = []
    sort = []
    range = {"udate": {}}
    filter = []
    must_not = []

    # convert parameter to field of dict type
    for key, value in parameter:

        if isinstance(value, Period):
            result_period = get_period(value)
            if result_period is not None:
                range["udate"].update(get_period(value))
            else:
                continue

        elif isinstance(value, Condition):
            result_condition = get_condition(value)
            if (result_condition is not None) and (
                "should" not in result_condition.keys()
            ):
                # filter.append(result_condition)
                must.append(result_condition)
            elif (result_condition is not None) and (
                "should" in result_condition.keys()
            ):
                should = result_condition["should"]
            else:
                pass

        elif (value is not None) and (
            (str(key) == "code")
            or (str(key) == "srctype")
        ):
            must.append(
                {"term": {key: {"value": value, "case_insensitive": True}}}
            )
        elif (value is not None) and (
            (str(key) == "accounttype")
            or (str(key) == "media")
            or (str(key) == "eventtype")
        ):
            if (str(value) == "All") or (str(value) == "all"):
                continue
            must.append(
                {"term": {key: {"value": value, "case_insensitive": True}}}
            )

        elif (key == "lastdata") and value is not None:
            if parameter.order == "desc":
                range["udate"]["lte"] = value.lastdatatime
            else:
                range["udate"]["gte"] = value.lastdatatime
            must_not.append({"match": {"_id": value.i_id}})

        elif (value is not None) and (key == "order"):
            sort.append({"udate": {"order": value}})

        # elif value is not None:
        #     filter.append({"match": {key: value}})

    # make query
    if len(range["udate"]) != 0:
        must.append({"range": range})

    query = {"bool": {"must": must}}

    if len(should) != 0:
        query["bool"]["must"].append(
            {"nested": {"path": "eventmsg", "query": {"bool": {"should": should}}}}
        )

    if len(filter) != 0:
        query["bool"].update({"filter": filter})

    if len(must_not) != 0:
        query["bool"].update({"must_not": must_not})

    body = {
        "_source": [
            "code",
            "srctype",
            "udate",
            "uid",
            "accounttype",
            "account",
            "media",
            "eventtype",
            "srcpath",
            "eventmsg",
        ],
        "size": 100,
        "query": query,
        "sort": sort,
    }
    return body


def get_index_list() -> list:
    """
    query index list
    """

    all_indexes = list(es.indices.get("es.database_name-*").keys())

    return all_indexes


def get_data_from_es(parameter: Parameter) -> dict:
    indexes = get_index_list()

    body = get_query_body(parameter=parameter)

    logger.info(f"index: {indexes[0]} ~ {indexes[-1]}")
    logger.info(f"body: {body}")

    result = es.search(index=indexes, body=body)

    docs = result["hits"]["hits"]
    result_value = {}
    datas = []
    for doc in docs:
        # datas.append(doc["_source"])
        data = doc["_source"]
        data.update({"i_id": doc["_id"]})
        datas.append(data)

    doc_count = result["hits"]["total"]["value"]
    logger.info(f"doc_count: {doc_count}")

    result_value["data"] = datas
    if doc_count == 0:
        result_value["lastpage"] = "There is no data retrieved."

    return result_value
