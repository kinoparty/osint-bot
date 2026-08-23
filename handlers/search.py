from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from services.validator import validate_and_format_phone, validate_email_address

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 **Добро пожаловать в OSINT-агрегатор.**\n\n"
        "Отправьте мне:\n"
        "• 📱 **Номер телефона** (в любом формате)\n"
        "• ✉️ **Email адрес**\n"
        "• 📷 **Фотографию лица** для поиска по базам\n\n"
        "_Бот произведет поиск по реестрам Минюста, YouControl, базам тегов и утечек._",
        parse_mode="Markdown",
    )


@router.message(F.photo)
async def handle_photo(message: Message):
    photo = message.photo[-1]  # Берем фото в максимальном разрешении
    file_id = photo.file_id

    await message.answer(
        f"⏳ **Фото получено.**\n"
        f"ID файла: `{file_id}`\n"
        f"Запускаю реверсивный поиск по биометрии и поисковым системам...",
        parse_mode="Markdown",
    )
    # TODO: Передать file_id в очередь Celery (task_search_by_photo.delay(file_id))


@router.message(F.text)
async def handle_text_query(message: Message):
    text = message.text.strip()

    # 1. Проверка на номер телефона
    clean_phone = validate_and_format_phone(text)
    if clean_phone:
        await message.answer(
            f"🔍 **Поиск по номеру:** `{clean_phone}`\n\n"
            f"⏳ Опрашиваем:\n"
            f"• Getcontact (теги и имена)\n"
            f"• YouControl & Минюст (ФОП, суды, долги)\n"
            f"• Мессенджеры (Telegram, WhatsApp, Viber)\n\n"
            f"_Формирование отчета займет до 30 секунд..._",
            parse_mode="Markdown",
        )
        # TODO: Передать clean_phone в очередь Celery
        return

    # 2. Проверка на Email
    clean_email = validate_email_address(text)
    if clean_email:
        await message.answer(
            f"🔍 **Поиск по Email:** `{clean_email}`\n\n"
            f"⏳ Проверяем базы утечек паролей и регистрацию на 120+ платформах...",
            parse_mode="Markdown",
        )
        # TODO: Передать clean_email в очередь Celery
        return

    # 3. Нераспознанный ввод
    await message.answer(
        "❌ Не удалось определить тип данных.\n"
        "Пожалуйста, отправьте корректный номер телефона, email или фото лица."
    )
