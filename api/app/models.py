from datetime import date, datetime

from typing import List, Optional
from pydantic import BaseModel, root_validator, ValidationError


class Condition(BaseModel):
    all: bool = True
    uid: Optional[str] = None
    account: Optional[str] = None
    srcpath: Optional[str] = None
    contents: Optional[str] = None

    @root_validator()
    def valid_condition(cls, values):
        all = values.get("all")
        uid = values.get("uid")
        account = values.get("account")
        srcpath = values.get("srcpath")
        contents = values.get("contents")

        if (
            (all == False)
            and (uid is None)
            and (account is None)
            and (srcpath is None)
            and (contents is None)
        ):
            raise ValueError(
                "There is no of (uid, account, srcpath, contents). Need 1 of (uid, account, srcpath, contents)"
            )
        elif (
            int(uid is not None)
            + int(account is not None)
            + int(srcpath is not None)
            + int(contents is not None)
        ) >= 2:
            raise ValueError("'only 1' of (uid, account, srcpath, contents)")
        else:
            return values


class Period(BaseModel):
    all: bool = True
    startdate: Optional[date] = None
    enddate: Optional[date] = None

    @root_validator()
    def valid_period(cls, values):
        all = values.get("all")
        startdate = values.get("startdate")
        enddate = values.get("enddate")
        if (all == False) and (startdate is None) and (enddate is None):
            raise ValidationError
        else:
            return values


class LastData(BaseModel):
    lastdatatime: datetime
    i_id: str


class Parameter(BaseModel):
    code: str
    srctype: str
    period: Optional[Period]
    accounttype: Optional[str]
    media: Optional[str]
    eventtype: Optional[str]
    condition: Optional[Condition]
    lastdata: Optional[LastData] = None
    order: str = "desc"

    class Config:
        extra = "forbid"


class Item(BaseModel):
    udate: datetime
    uid: str
    accounttype: str
    account: str
    media: str
    eventtype: str
    srcpath: str
    contents: str
    i_id: str


class Data(BaseModel):
    data: List[Item] = []
