from fastapi import APIRouter

from opal.common.logger import logger
from opal.common.schemas.data import DataUpdate
from opal.server.config import DATA_CONFIG_ROUTE, DataSourceConfig
from opal.server.data.data_update_publisher import DataUpdatePublisher


def init_data_updates_router(data_update_publisher: DataUpdatePublisher, data_sources_config: DataSourceConfig):
    router = APIRouter()

    @router.get(DATA_CONFIG_ROUTE)
    async def get_default_data_config():
        logger.info("Serving source configuration")
        return data_sources_config


    @router.post(DATA_CONFIG_ROUTE)
    async def publish_data_update_event(update:DataUpdate):
        logger.info("Publishing received update event")
        await data_update_publisher.publish_data_updates()

    return router
