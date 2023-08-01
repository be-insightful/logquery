import uvicorn
import logging

from pprint import pprint


log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["default"].update(
    {"fmt": "%(asctime)s - %(levelprefix)s %(message)s"}
)
log_config["formatters"]["access"].update(
    {
        "fmt": '%(asctime)s - %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
    }
)
logger = logging.getLogger("uvicorn")
