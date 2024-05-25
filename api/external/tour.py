from datetime import date, datetime, timedelta
from enum import Enum
from typing import Optional

from aiohttp import ClientSession
from pytz import timezone

from api.schema import DataGovKrResponse, FestivalSchedule

KST = timezone("Asia/Seoul")


class ResponseType(str, Enum):
    XML = "xml"
    JSON = "json"


class DataGoKr:
    api_key: str = ""
    response_type: ResponseType = ResponseType.JSON
    metadata: dict[str, any] = {
        "MobileOS": "ETC",
        "MobileApp": "NOLZAPAN",
    }
    headers: dict[str, str] = {
        "Content-Type": "application/json",
    }

    def __init__(
        self,
        api_key: str,
        session: ClientSession,
    ) -> None:
        self.session = session
        self.api_key = api_key

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    def response_as_json(self):
        self.response_type = ResponseType.JSON
        return self

    def response_as_xml(self):
        self.response_type = ResponseType.XML
        return self


class TourInfo(DataGoKr):
    ENDPOINT = "http://apis.data.go.kr/B551011/KorService1"

    async def get_festival_schedule(
        self,
        eventStartDate: date = datetime.now(tz=KST).date(),
        eventEndDate: date = datetime.now(tz=KST).date() + timedelta(days=90),
        pageNo: int = 1,
        numOfRows: int = 1,
        # TODO: 지역코드별 필터링기능 추가
        **_kwargs,
    ) -> DataGovKrResponse[FestivalSchedule]:
        API_PATH = "searchFestival1"
        params = {
            "eventStartDate": eventStartDate.strftime("%Y%m%d"),
            "eventEndDate": eventEndDate.strftime("%Y%m%d"),
            "pageNo": pageNo,
            "numOfRows": numOfRows,
            "_type": self.response_type.value,
            "ServiceKey": self.api_key,
        }
        params.update(self.metadata)
        params.update(_kwargs)
        response = await self.session.get(
            f"{self.ENDPOINT}/{API_PATH}",
            params=params,
            headers=self.headers,
        )
        content = await response.json()
        print(f"{content = }")
        return DataGovKrResponse(**content)

    async def get_area_code(
            self,
            numOfRows: int = 10,
            pageNo: int = 1,
            areaCode: Optional[str] = "",
            **_kwargs,
        ):
        """
        다른 API 호출에 필요한 지역코드를 받아옵니다.

        TODO: 지역코드를 가져오는 API 구현
        """
        API_PATH = "areaCode1"
        params = {
            "numOfRows": numOfRows,
            "pageNo": pageNo,
            "areaCode": areaCode,
            "_type": self.response_type.value,
            "ServiceKey": self.api_key,
        } 
        params.update(self.metadata)
        params.update(_kwargs)
        response = await self.session.get(
            f"{self.ENDPOINT}/{API_PATH}",
            params=params,
            headers=self.headers,
        )
        content = await response.json()
        print(f"{content = }")
        return DataGovKrResponse(**content)


    async def search_by_keyword(self, keyword: str):
        """
        키워드로 관련된 정보를 검색합니다.

        NOTE: 필요한경우 구현
        """

    async def search_by_location(self, location: any):
        """
        클라이언트로부터 전달받은 좌표정보를 사용하여 위치정보기반 지역별 축제정보를 검색합니다.

        NOTE: 필요한경우 구현
        """


class PictureInfo(DataGoKr):
    ENDPOINT: str = "http://apis.data.go.kr/B551011/PhotoGalleryService1"
