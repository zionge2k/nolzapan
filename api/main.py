import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse

from api.enums import Environment
from api.routes import router
from api.settings import SERVICE_INFO, env

BEGIN_TIMESTAMP = time.time()
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        yield
    finally:
        pass


app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    title=SERVICE_INFO["title"],
    version=SERVICE_INFO["version"],
    docs_url="/docs" if env.environment == Environment.TEST else None,
)

if env.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=env.cors_origins.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logging.info("CORS enabled")

app.include_router(router=router)


@app.get(
    "/status",
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
async def get_status():
    return {
        "status": True,
        "uptime": time.time() - BEGIN_TIMESTAMP,
    }


def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _end_point, method_item in app.openapi_schema.get("paths", {}).items():
            for _method, param in method_item.items():
                responses = param.get("responses")
                if "422" in responses:
                    del responses["422"]
    return app.openapi_schema


app.openapi = custom_openapi
