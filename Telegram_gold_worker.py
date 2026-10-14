import os
import asyncio
import logging
from datetime import date

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


async def analyze_gold():
    def run_original_engine():
        config = DEFAULT_CONFIG.copy()
        graph = TradingAgentsGraph(debug=False, config=config)

        # Kansta3mlo moteur TradingAgents l'asli
        _, decision = graph.propagate(
            "XAUUSD",
            date.today().isoformat()
        )
        return str(decision)

    return await asyncio.to_thread(run_original_engine)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🥇 TradingAgents Gold Bot\n\n"
        "/signal - Analyse Gold\n"
        "Had bot kaysta3mel moteur TradingAgents l'asli."
    )


async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if str(chat_id) != CHAT_ID:
        await update.message.reply_text("⛔ Unauthorized.")
        return

    message = await update.message.reply_text(
        "⏳ TradingAgents kay7لل Gold... tsenna chwia."
    )

    try:
        result = await analyze_gold()
        output = f"🥇 GOLD — XAUUSD\n\n{result}"

        for start in range(0, len(output), 4000):
            await context.bot.send_message(
                chat_id=chat_id,
                text=output[start:start + 4000]
            )

        await message.delete()

    except Exception:
        logger.exception("Gold analysis failed")
        await message.edit_text(
            "❌ L'analyse failed. Chouf Railway logs."
        )


def main():
    app = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))

    logger.info("Telegram Gold worker started.")
    app.run_polling()


if __name__ == "__main__":
    main()
