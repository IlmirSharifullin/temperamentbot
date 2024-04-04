from aiogram import Router
from .start import router as start_router
from .temperament import router as temperament_router


router = Router(name='main')
router.include_routers(start_router, temperament_router)
