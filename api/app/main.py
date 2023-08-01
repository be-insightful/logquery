import secrets
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.applog import logger, log_config
from app.config import User_Settings
from app.models import Parameter
from app.es import get_data_from_es

app = FastAPI()

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    info = User_Settings()

    correct_username = secrets.compare_digest(credentials.username, info.uname)
    correct_password = secrets.compare_digest(credentials.password, info.pw)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect id or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.post("/v1/search")
async def search(
    parameter: Parameter, username: str = Depends(get_current_username)
):
    logger.info(f"request: {parameter.json()}")
    result = get_data_from_es(parameter)

    return result


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_config=log_config,
    )
