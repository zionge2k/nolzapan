from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "dev"
    TEST = "test"
    STAGING = "stage"
    PRODUCTION = "prod"

    def __str__(self):
        return str(self.value).upper()


class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    FATAL = "fatal"

    def __str__(self):
        return str(self.value).upper()


class Area(str, Enum):
    def __init__(self, code):
        self.code = code

    SEOUL = "서울"
    INCHEON = "인천"
    DAEJEON = "대전"
    DAEGU = "대구"
    GWANGJU = "광주"
    BUSAN = "부산"
    ULSAN = "울산"
    SEJONG = "세종특별자치시"
    GYEONGGI = "경기도"
    GANGWON = "강원특별자치도"
    CHUNGBUK = "충청북도"
    CHUNGNAM = "충청남도"
    GYEONGBUK = "경상북도"
    GYEONGNAM = "경상남도"
    JEONBUK = "전북특별자치도"
    JEONNAM = "전라남도"
    JEJU = "제주도"

    @classmethod
    def get_code(cls, area: "Area") -> str | None:
        code = {
            cls.SEOUL: "1",
            cls.INCHEON: "2",
            cls.DAEJEON: "3",
            cls.DAEGU: "4",
            cls.GWANGJU: "5",
            cls.BUSAN: "6",
            cls.ULSAN: "7",
            cls.SEJONG: "8",
            cls.GYEONGGI: "31",
            cls.GANGWON: "32",
            cls.CHUNGBUK: "33",
            cls.CHUNGNAM: "34",
            cls.GYEONGBUK: "35",
            cls.GYEONGNAM: "36",
            cls.JEONBUK: "37",
            cls.JEONNAM: "38",
            cls.JEJU: "39",
        }
        return code.get(area, None)
