import discord
import json

class EmbedManager:
    def __init__(self):
        self.config_path = 'config.json' 
        self.config = self.load_config()
        self.banner_url = self.config.get("banner_url", None)

    def load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar config: {str(e)}")
            return {}

    def save_config(self):
        # Salva as configurações no arquivo
        with open(self.config_path, "w") as file:
            json.dump(self.config, file, indent=4)  

    def create_embed(self, title, description, banner=None):
        embed_color_hex = self.config.get("embed_color", "#FF5733")
        try:
            embed_color = int(embed_color_hex.lstrip("#"), 16)
        except (ValueError, IndexError):
            embed_color = 0xFF5733  

        embed = discord.Embed(title=title, description=description, color=embed_color)

        if banner or self.banner_url:
            embed.set_image(url=banner or self.banner_url)

        return embed

    def get_banner(self):
        return self.banner_url  

    def set_banner(self, url):
        self.banner_url = url
        self.config['banner_url'] = url
        self.save_config()

    async def set_bot_presence(self, bot, presence_type, presence_text):
        if presence_type == "jogando":
            activity = discord.Game(name=presence_text)
        elif presence_type == "ouvindo":
            activity = discord.Activity(type=discord.ActivityType.listening, name=presence_text)
        elif presence_type == "transmitindo":
            activity = discord.Streaming(name=presence_text, url="https://twitch.tv/seu_canal")
        else:
            activity = None

        if activity:
            await bot.change_presence(activity=activity)

            self.config["bot_presence"] = {
                "text": presence_text,
                "type": presence_type
            }
            self.save_config()
