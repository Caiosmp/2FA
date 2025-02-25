# bot.py

import discord
from discord.ext import commands
import asyncio
import logging
from utils.config_loader import load_config
from utils.embed_manager import EmbedManager

# Inicialização do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar a configuração do arquivo config.json
config = load_config()
if not config:
    raise ValueError("Não foi possível carregar a configuração.")

bot_token = config["bot_token"]
application_id = config["application_id"]
presence_text = config["bot_presence"]["text"]
presence_type = config["bot_presence"]["type"]
embed_manager = EmbedManager()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents, application_id=int(application_id))

# Função para carregar as extensões
async def load_extensions():
    initial_extensions = ['cogs.personalization', 'cogs.twofa', "cogs.configbot"]
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            logger.info(f"Extensão carregada: {extension}")
        except Exception as e:
            logger.error(f"Falha ao carregar extensão {extension}: {e}")

@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        logger.info(f"Slash commands sincronizados com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao sincronizar slash commands: {e}")

    logger.info(f"Bot {bot.user} está online!")
    await embed_manager.set_bot_presence(bot, presence_type, presence_text)

async def main():
    async with bot:
        await load_extensions()
        await bot.start(bot_token)

if __name__ == '__main__':
    asyncio.run(main())
