import json
from pydantic import BaseSettings


class ES_Settings(BaseSettings):
    host: str = "https://instance_id.region.es.amazonaws.com"
    appuser: str = "esuser"
    password: str = "password"


class Athena_Settings(BaseSettings):
    access_key_id: str = "access_key_id"
    secret_access_key: str = "secret_access_key"
    region_name: str = "region_name"
    endpoint_url: str = "https://anthena_instance_id.athena.region.vpce.amazonaws.com"
    database: str = "database_name"
    outpath: str = "out_path"


class S3_Settings(BaseSettings):
    access_key_id: str = "access_key_id"
    secret_access_key: str = "secret_access_key"
    region_name: str = "region_name"
    bucket: str = "bucket_name"


class User_Settings(BaseSettings):
    uname: str = "uname"
    pw: str = "password"
