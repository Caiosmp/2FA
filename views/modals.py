import discord
from discord.ui import Modal, TextInput, Select
import aiohttp
from utils.embed_manager import EmbedManager
import pyotp
import json

embed_manager = EmbedManager()

class ChangeNameModal(Modal):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(title="Mudar Nome do Bot")
        self.name_input = TextInput(label="Novo Nome", placeholder="Digite o novo nome do bot")
        self.add_item(self.name_input)

    async def on_submit(self, interaction: discord.Interaction):
        new_name = self.name_input.value.strip()
        if len(new_name) > 0:
            try:
                await interaction.client.user.edit(username=new_name)
                await interaction.response.send_message(f"Nome do bot alterado para: {new_name}", ephemeral=True)
            except discord.HTTPException as e:
                await interaction.response.send_message(f"Erro ao mudar o nome: {str(e)}", ephemeral=True)
        else:
            await interaction.response.send_message("O nome não pode ser vazio.", ephemeral=True)

class ChangeEmbedColorModal(Modal):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(title="Mudar Cor da Embed")
        self.color_input = TextInput(label="Nova Cor Hexadecimal", placeholder="Digite a nova cor (Ex: #FF5733)")
        self.add_item(self.color_input)

    async def on_submit(self, interaction: discord.Interaction):
        new_color = self.color_input.value.strip()
        if new_color.startswith("#") and len(new_color) == 7:
            embed_manager.config["embed_color"] = new_color
            embed_manager.save_config()
            await interaction.response.send_message(f"Cor da embed alterada para: {new_color}", ephemeral=True)
        else:
            await interaction.response.send_message("Formato de cor inválido. Use # seguido de 6 caracteres.", ephemeral=True)

class ChangeAvatarModal(Modal):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(title="Mudar Avatar do Bot")
        self.avatar_url = TextInput(label="URL do Novo Avatar", placeholder="Cole o link da imagem aqui (JPG, PNG, GIF)")
        self.add_item(self.avatar_url)

    async def on_submit(self, interaction: discord.Interaction):
        avatar_url = self.avatar_url.value.strip()
        if avatar_url.startswith("http"):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(avatar_url) as response:
                        if response.status == 200:
                            avatar = await response.read()
                            await interaction.client.user.edit(avatar=avatar)
                            await interaction.response.send_message("Avatar do bot alterado com sucesso!", ephemeral=True)
                        else:
                            await interaction.response.send_message("Não foi possível baixar a imagem. Verifique a URL.", ephemeral=True)
            except discord.HTTPException as e:
                await interaction.response.send_message(f"Erro ao alterar o avatar: {str(e)}", ephemeral=True)
        else:
            await interaction.response.send_message("URL inválida. Deve começar com 'http'.", ephemeral=True)

class ChangePresenceModal(Modal):
    def __init__(self, bot):
        super().__init__(title="Mudar Presença")
        self.bot = bot
        self.activity_type = TextInput(label="Tipo de Presença", placeholder="jogando, ouvindo, transmitindo")
        self.presence_input = TextInput(label="Frase da Presença", placeholder="Digite a nova frase para a presença")
        self.add_item(self.activity_type)
        self.add_item(self.presence_input)

    async def on_submit(self, interaction: discord.Interaction):
        presence_type = self.activity_type.value.strip().lower()
        new_presence = self.presence_input.value.strip()
        if len(new_presence) > 0:
            await embed_manager.set_bot_presence(interaction.client, presence_type, new_presence)
            await interaction.response.send_message(f"Presença alterada para: {new_presence}", ephemeral=True)
        else:
            await interaction.response.send_message("A frase da presença não pode ser vazia.", ephemeral=True)

class ChangeBannerModal(Modal):
    def __init__(self, bot):
        super().__init__(title="Adicionar/Alterar Banner")
        self.bot = bot  # Armazena o bot
        self.banner_url = TextInput(label="URL do Banner", placeholder="Digite o link da imagem (JPG, PNG, GIF) ou deixe vazio para remover")
        self.add_item(self.banner_url)

    async def on_submit(self, interaction: discord.Interaction):
        url = self.banner_url.value.strip()
        if url:
            embed_manager.set_banner(url)  # Atualiza o banner no arquivo de configuração
            await interaction.response.send_message(f"Banner atualizado com sucesso!", ephemeral=True)
        else:
            embed_manager.set_banner(None)  # Remove o banner
            await interaction.response.send_message(f"Banner removido com sucesso!", ephemeral=True)
        
        embed_manager.load_config() 
        if hasattr(self.bot, 'twofa_cog') and self.bot.twofa_cog.embed_message:
            await self.bot.twofa_cog.update_2fa_embed()

class TwoFAModal(Modal):
    def __init__(self, bot):  # Adicionando bot como argumento
        super().__init__(title="Insira sua chave 2FA")
        self.bot = bot  # Armazena o bot
        self.key_input = TextInput(label="Chave de segurança", placeholder="Digite sua chave 2FA aqui")
        self.add_item(self.key_input)

    async def on_submit(self, interaction: discord.Interaction):
        key = self.key_input.value.strip()
        if len(key) < 16:
            await interaction.response.send_message("Chave de segurança inválida. Verifique o formato e tente novamente.", ephemeral=True)
            return

        try:
            totp = pyotp.TOTP(key)
            code = totp.now()

            embed = discord.Embed(title="Seu Código 2FA", description=f"```\n{code}\n```", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Erro ao gerar o código 2FA: {str(e)}", ephemeral=True)


class Description(Modal):   
    def __init__(self, bot):
        self.bot = bot
        super().__init__(title="Mude a descrição da Embed")
        self.key_input = TextInput(label="Descrição", placeholder="Digite aqui o texto ou deixe vazio para remover", style=discord.TextStyle.long, required=False)
        self.add_item(self.key_input)

    async def on_submit(self, interaction: discord.Interaction):
        description_text = self.key_input.value.strip()
        if description_text:
            embed_manager.config["embed_description"] = description_text
            embed_manager.save_config()
            await interaction.response.send_message(f"Descrição foi alterada!", ephemeral=True)
        else:
            embed_manager.config["embed_description"] = None  # Remove a descrição
            embed_manager.save_config()
            await interaction.response.send_message(f"Descrição removida com sucesso!", ephemeral=True)

class AddAdminModal(Modal):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(title="Adicionar Administrador")
        self.user_input = TextInput(label="Nome de Usuário ou ID", placeholder="Digite o nome ou ID do usuário")
        self.add_item(self.user_input)

    async def on_submit(self, interaction: discord.Interaction):
        user_input = self.user_input.value.strip()

        if user_input:
            # Adiciona o usuário à lista de administradores
            self.add_admin_to_config(user_input)
            await interaction.response.send_message(f"{user_input} agora é um administrador!", ephemeral=True)
        else:
            await interaction.response.send_message("Nome de usuário ou ID inválido. Tente novamente.", ephemeral=True)

    def add_admin_to_config(self, user_input):
        # Adiciona o usuário à configuração ou banco de dados de administradores
        config = embed_manager.load_config()
        admins = config.get("admins", [])
        if user_input not in admins:
            admins.append(user_input)
            config["admins"] = admins
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
