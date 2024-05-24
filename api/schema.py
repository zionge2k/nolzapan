"""
공통응답을 매번 생성하는 것은 비효율적이기 때문에 Generic과 TypeVar를 사용하여 정의하고
변경되는 내용에 대한 데이터클래스를 생성하고 생성된 공통응답에 끼워넣어 사용하도록 합니다.
"""

from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class DataGovKrResponseHeader(BaseModel):
    """
    공공API 공통 응답 헤더
    """

    resultCode: Annotated[str, Field(..., description="결과코드", examples=["0000"])]
    resultMsg: Annotated[str, Field(..., description="결과메시지", examples=["OK"])]


class ItemContent(BaseModel, Generic[T]):
    """
    공공API의 응답 item이 뭐가 들어갈지 모르기때문에 일단 제네릭으로 처리
    """

    item: list[T]


class DataGovKrResponseBody(BaseModel, Generic[T]):
    """
    공공API 공통 응답 바디
    """

    items: ItemContent[T]
    numOfRows: int
    pageNo: int
    totalCount: int


class DataGovKrContent(BaseModel, Generic[T]):
    """
    공공API 응답에 포함된 공통된 내용
    """

    header: DataGovKrResponseHeader
    body: DataGovKrResponseBody[T]


class DataGovKrResponse(BaseModel, Generic[T]):
    """
    공공API 공통 응답
    """

    response: DataGovKrContent[T]


class FestivalSchedule(BaseModel):
    """
    행사 일정 정보
    """

    # pylint: disable=C0301
    addr1: Annotated[
        str,
        Field(..., description="주소", examples=["경상남도 거창군 거창읍 수남로 2181"]),
    ]
    addr2: Annotated[str, Field(..., description="상세주소", examples=[""])]
    booktour: Annotated[str, Field(..., description="예약페이지", examples=[""])]
    cat1: Annotated[str, Field(..., description="대분류", examples=["A02"])]
    cat2: Annotated[str, Field(..., description="중분류", examples=["A0208"])]
    cat3: Annotated[str, Field(..., description="소분류", examples=["A02080200"])]
    contentid: Annotated[str, Field(..., description="콘텐츠ID", examples=["142069"])]
    contenttypeid: Annotated[
        str, Field(..., description="콘텐츠타입ID", examples=["15"])
    ]
    createdtime: Annotated[
        str, Field(..., description="등록일", examples=["20070709090000"])
    ]
    eventstartdate: Annotated[
        str, Field(..., description="행사시작일", examples=["20240726"])
    ]
    eventenddate: Annotated[
        str, Field(..., description="행사종료일", examples=["20240809"])
    ]
    firstimage: Annotated[
        str,
        Field(
            ...,
            description="대표이미지",
            examples=[
                "http://tong.visitkorea.or.kr/cms/resource/78/3302778_image2_1.jpg"
            ],
        ),
    ]
    firstimage2: Annotated[
        str,
        Field(
            ...,
            description="대표이미지2",
            examples=[
                "http://tong.visitkorea.or.kr/cms/resource/78/3302778_image3_1.jpg"
            ],
        ),
    ]
    cpyrhtDivCd: Annotated[
        str, Field(..., description="저작권구분코드", examples=["Type3"])
    ]
    mapx: Annotated[str, Field(..., description="경도", examples=["127.9108367626"])]
    mapy: Annotated[str, Field(..., description="위도", examples=["35.6737770003"])]
    mlevel: Annotated[str, Field(..., description="맵레벨", examples=["6"])]
    modifiedtime: Annotated[
        str, Field(..., description="수정일", examples=["20240522140439"])
    ]
    areacode: Annotated[str, Field(..., description="지역코드", examples=["36"])]
    sigungucode: Annotated[str, Field(..., description="시군구코드", examples=["2"])]
    tel: Annotated[str, Field(..., description="전화번호", examples=["055-945-8455~6"])]
    title: Annotated[str, Field(..., description="제목", examples=["거창국제연극제"])]
