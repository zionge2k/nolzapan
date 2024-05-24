# NOLZAPAN

## Description

WIP

## Setup

`.env.example`를 참조하여 `.env` 파일을 생성한 후, 해당 파일에 환경 변수를 설정해주세요.

`NOLZA_DATA_API_TOKEN`에 공공데이터 포탈에서 발급받은 API 키를 입력해주세요.

## How to run

```bash
make build
make up
```

실행환경은 dockerize 되어있습니다. `make build`로 이미지를 빌드하고, `make up`으로 컨테이너를 실행할 수 있습니다.

컨테이너 실행 이후 `http://localhost:19000/docs`로 접속하시면 API 문서를 확인하실 수 있습니다.
