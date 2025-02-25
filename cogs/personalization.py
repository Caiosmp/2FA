import discord
from discord import app_commands
from discord.ext import commands
from utils.embed_manager import EmbedManager
from views.modals import (
    ChangeNameModal,
    ChangeEmbedColorModal,
    ChangeAvatarModal,
    ChangePresenceModal,
    ChangeBannerModal,
    Description
)

embed_manager = EmbedManager()

class Personalization(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin(self, user_id: str) -> bool:
        config_data = embed_manager.load_config()
        return str(user_id) in config_data.get("admins", [])

    @app_commands.command(name="personalizar", description="Personalize o bot")
    async def personalizar(self, interaction: discord.Interaction):
        # Verificar se o usuário é administrador
        if not self.is_admin(interaction.user.id):
            await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)
            return
        
        embed = embed_manager.create_embed(
            title="Personalizar Bot",
            description="Escolha uma opção para personalizar o bot"
        )
        view = discord.ui.View()

        # Botões para personalizar o bot
        button_name = discord.ui.Button(label="Mudar Nome", style=discord.ButtonStyle.primary)
        button_name.callback = lambda i: i.response.send_modal(ChangeNameModal(self.bot))
        view.add_item(button_name)

        button_color = discord.ui.Button(label="Mudar Cor da Embed", style=discord.ButtonStyle.secondary)
        button_color.callback = lambda i: i.response.send_modal(ChangeEmbedColorModal(self.bot))
        view.add_item(button_color)

        button_avatar = discord.ui.Button(label="Mudar Avatar", style=discord.ButtonStyle.success)
        button_avatar.callback = lambda i: i.response.send_modal(ChangeAvatarModal(self.bot))
        view.add_item(button_avatar)

        button_presence = discord.ui.Button(label="Mudar Presença", style=discord.ButtonStyle.primary)
        button_presence.callback = lambda i: i.response.send_modal(ChangePresenceModal(self.bot))
        view.add_item(button_presence)

        button_banner = discord.ui.Button(label="Adicionar/Alterar Banner", style=discord.ButtonStyle.primary)
        button_banner.callback = lambda i: i.response.send_modal(ChangeBannerModal(self.bot))
        view.add_item(button_banner)

        button_descricao = discord.ui.Button(label="Mudar Descrição", style=discord.ButtonStyle.primary)
        button_descricao.callback = lambda i: i.response.send_modal(Description(self.bot))
        view.add_item(button_descricao)

        # Botão para atualizar a embed com as configurações mais recentes
        button_update_embed = discord.ui.Button(label="Atualizar Embed", style=discord.ButtonStyle.primary)
        button_update_embed.callback = lambda i: self.update_embed(i)
        view.add_item(button_update_embed)

        # Envia a mensagem inicial com o embed e os botões
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    async def update_embed(self, interaction: discord.Interaction):
        # Atualiza o embed com o banner, descrição, cor, etc.
        embed = embed_manager.create_embed(
            title="Bot Personalizado",
            description=embed_manager.config.get("embed_description", "Descrição padrão do bot"),
            banner=embed_manager.get_banner()
        )

        # Envia a embed atualizada no mesmo canal onde o comando foi executado
        await interaction.channel.send(embed=embed)

        await interaction.response.send_message("Embed atualizada com sucesso!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Personalization(bot))
