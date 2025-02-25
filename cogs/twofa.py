import discord
from discord import app_commands
from discord.ext import commands
from views.modals import TwoFAModal
from utils.embed_manager import EmbedManager
from utils.config_loader import load_config

embed_manager = EmbedManager()

class TwoFA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_message = None  

    def is_admin(self, user_id: str) -> bool:
        config_data = load_config()
        return str(user_id) in config_data.get("admins", [])

    # Função para criar a View com o botão 2FA (View persistente)
    def create_view(self):
        view = discord.ui.View(timeout=None)
        button = discord.ui.Button(label="2FA", style=discord.ButtonStyle.primary)
        button.callback = self.button_callback
        view.add_item(button)
        return view

    # Callback do botão 2FA para abrir o modal
    async def button_callback(self, interaction: discord.Interaction):
        modal = TwoFAModal(self.bot) 
        await interaction.response.send_modal(modal)

    # Comando de slash para gerar o código 2FA
    @app_commands.command(name="2fa", description="Gere seu código 2FA")
    async def generate_2fa(self, interaction: discord.Interaction):
        if not self.is_admin(interaction.user.id):
            await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)
            return
        
        await self.send_2fa_embed(interaction)

    # Função para enviar o embed e o botão 2FA
    async def send_2fa_embed(self, interaction: discord.Interaction):
        config_data = load_config()
        text_embed = config_data.get("embed_description", "Clique no botão abaixo para capturar seu 2FA.")
        embed = embed_manager.create_embed(
            title="Código 2FA",
            description=text_embed,
            banner=embed_manager.get_banner()
        )

        view = self.create_view()
        self.embed_message = await interaction.response.send_message(embed=embed, view=view, ephemeral=False)

    # Função para atualizar a embed do 2FA (exemplo: quando o banner é alterado)
    async def update_2fa_embed(self):
        if self.embed_message:
            # Atualiza a embed com as configurações mais recentes
            embed = embed_manager.create_embed(
                title="Código 2FA",
                description=embed_manager.config.get("embed_description", "Clique no botão abaixo para capturar seu 2FA."),
                banner=embed_manager.get_banner()
            )
            # Atualiza a embed no canal onde o comando foi executado
            await self.embed_message.edit(embed=embed)

    async def update_config_and_embed(self):
        # Realiza a alteração nas configurações
        embed_manager.set_banner("novo_banner_url")  #
        await self.update_2fa_embed()  

async def setup(bot):
    await bot.add_cog(TwoFA(bot))
