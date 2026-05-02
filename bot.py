import asyncio
import os
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# === SOZLAMALAR ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Bot va Dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# === SYSTEM PROMPT ===
SYSTEM_PROMPT = """Siz O'zbekiston Respublikasi qonunchiligi bo'yicha malakali huquqiy maslahatchi assistantsiz.

Qoidalaringiz:
1. Faqat O'zbekiston qonunchiligiga asoslangan holda javob bering
2. Javoblaringiz ODDIY va TUSHUNARLI tilda bo'lsin — yuridik jargoнsiz
3. Foydalanuvchining ANIQ HOLATIDAN kelib chiqib, amaliy maslahat bering
4. Tegishli qonun moddalari yoki me'yoriy hujjatlarni keltiring (agar bilsangiz)
5. Agar savol sizning vakolatingizdan tashqarida bo'lsa, professional huquqshunos/advokat bilan maslahatlashishni tavsiya qiling
6. Javob oxirida qisqa XULOSA yozing
7. Hech qachon noto'g'ri ma'lumot bermang — bilmasangiz, shuni ayting

Javob formati:
📋 **Holat tahlili:** (foydalanuvchi holatini tushuntiring)
⚖️ **Qonuniy asos:** (tegishli qonun/modda)
✅ **Amaliy maslahat:** (nima qilish kerak, qadamba-qadam)
📌 **Xulosa:** (qisqa yakuniy fikr)

Eslatma: Bu maslahat umumiy ma'lumot uchun. Murakkab holatlarda rasmiy advokat bilan maslahatlashing."""


# === HANDLERLAR ===

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Assalomu alaykum!\n\n"
        "Men O'zbekiston qonunchiligi bo'yicha huquqiy maslahat beruvchi botman.\n\n"
        "📝 Savolingizni yozing — holatингizdan kelib chiqib javob beraman.\n\n"
        "⚠️ Eslatma: Bu bot umumiy huquqiy ma'lumot beradi. "
        "Murakkab holatlarda rasmiy advokat bilan maslahatlashing."
    )


@dp.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "🆘 **Yordam**\n\n"
        "Men quyidagi sohalarda yordam bera olaman:\n\n"
        "👨‍👩‍👧 Oila huquqi (ajralish, alimentlar, meros)\n"
        "🏠 Mulk huquqi (sotish, ijarа, ro'yxatga olish)\n"
        "💼 Mehnat huquqi (ishdan bo'shatish, maosh, ta'til)\n"
        "🏢 Tadbirkorlik (IP, MChJ, soliqlar)\n"
        "🚗 Ma'muriy (jarima, litsenziya)\n"
        "👮 Jinoyat huquqi (umumiy ma'lumot)\n\n"
        "Savolingizni batafsil yozing — aniq javob beraman!"
    )


@dp.message()
async def question_handler(message: Message):
    user_question = message.text

    # Typing animatsiyasi
    await bot.send_chat_action(message.chat.id, "typing")

    try:
        # Gemini ga so'rov
        full_prompt = f"{SYSTEM_PROMPT}\n\nFoydalanuvchi savoli: {user_question}"
        response = model.generate_content(full_prompt)
        answer = response.text

        await message.answer(answer, parse_mode="Markdown")

    except Exception as e:
        await message.answer(
            "❌ Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.\n"
            f"Xato: {str(e)}"
        )


# === ISHGA TUSHIRISH ===
async def main():
    print("✅ Bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
