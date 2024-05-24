from datetime import date, timedelta

from aiohttp import ClientSession, ClientTimeout
from fastapi import APIRouter, Query, status

from api import schema
from api.external.tour import TourInfo
from api.settings import env

router = APIRouter()


@router.get(
    "/tour",
    response_model=schema.DataGovKrResponse[schema.FestivalSchedule],
    status_code=status.HTTP_200_OK,
)
async def get_tour_info(
    eventStartDate: date = Query(
        ...,
        description="축제 시작일자",
        alias="begin_date",
        example=str(date.today()),
    ),
    eventEndDate: date = Query(
        ...,
        description="축제 종료일자",
        alias="end_date",
        example=str(date.today() + timedelta(days=90)),
    ),
    pageNo: int = Query(
        1,
        description="페이지 번호",
        alias="page_no",
        example=1,
    ),
    numOfRows: int = Query(
        10,
        description="한 페이지 결과 수",
        alias="num_of_rows",
        example=10,
    ),
) -> schema.DataGovKrResponse[schema.FestivalSchedule]:
    """
    TODO:   현재 공공데이터 포털로부터 받은 정보 그대로 반환하고 있음
            필요한경우 서비스 성격에 맞게 필요한 정보만 추출하여 반환하도록 수정 필요

    NOTE:   필요한경우 서비스레이어 분리
    """
    async with ClientSession(timeout=ClientTimeout(5)) as session:
        async with TourInfo(env.data_api_token, session) as tour:
            result = await tour.get_festival_schedule(
                eventStartDate=eventStartDate,
                eventEndDate=eventEndDate,
                pageNo=pageNo,
                numOfRows=numOfRows,
            )
            return result
