from fastapi import FastAPI
from fastapi import status
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings
from loguru import logger

from app.db.admin import attach_admin_panel


class ProjectSettings(BaseSettings):
    LOCAL_MODE: bool = False


def register_exception(application):
    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        # or logger.error(f'{exc}')
        logger.debug(f'{exc}')
        content = {'status_code': 422, 'message': exc_str, 'data': None}
        return JSONResponse(
            content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


def register_cors(application):
    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def init_web_application():
    project_settings = ProjectSettings()
    application = FastAPI(
        title="Spanish lesson api",
        openapi_url='/openapi.json',
        docs_url='/docs',
        redoc_url='/redoc'
    )

    if project_settings.LOCAL_MODE:
        register_exception(application)
        register_cors(application)

    from app.routes.lesson import router as lesson_router
    from app.routes.web import router as web_router

    application.include_router(lesson_router)
    application.include_router(web_router)
    # application.mount("/static", StaticFiles(directory="static"), name="static")
    application.mount("/storage", StaticFiles(directory="storage"))

    attach_admin_panel(application)

    return application


def run() -> FastAPI:
    application = init_web_application()
    return application


fastapi_app = run()
