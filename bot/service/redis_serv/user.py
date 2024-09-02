from bot.service.redis_serv.base import redis_pool


async def set_message_id_work(message_id: int):

    await redis_pool.set("message_id_work", message_id)

async def set_message_id_las_vegas(message_id: int):

    await redis_pool.set("message_id_las_vegas", message_id)

async def get_message_id_work():

    return (await redis_pool.get("message_id_work"))

async def get_message_id_las_vegas():

    return (await redis_pool.get("message_id_las_vegas"))

