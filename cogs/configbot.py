import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button, Select
from views.modals import AddAdminModal
from utils.embed_manager import EmbedManager

embed_manager = EmbedManager()

class ConfigBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="configbot", description="Gerencie as configurações do bot")
    async def configbot(self, interaction: discord.Interaction):
        if not self.is_admin(interaction.user.id):
            await interaction.response.send_message("Você não tem permissão para executar este comando.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Configuração do Bot",
            description="Escolha uma das opções abaixo para gerenciar o bot.",
            color=discord.Color.blue()
        )

        # Botões de funcionalidades gerais
        view = View()

        # Botão para gerenciar administradores
        button_manage_admin = Button(label="Gerenciar Administradores", style=discord.ButtonStyle.primary)
        button_manage_admin.callback = self.manage_admins
        view.add_item(button_manage_admin)

        # Botão para conectar o bot em uma call
        button_connect_call = Button(label="Conectar Bot em Call", style=discord.ButtonStyle.secondary)
        button_connect_call.callback = self.connect_call
        view.add_item(button_connect_call)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    def is_admin(self, user_id):
        config = embed_manager.load_config()
        admins = config.get("admins", [])
        return str(user_id) in admins

    async def manage_admins(self, interaction: discord.Interaction):
        config = embed_manager.load_config()
        admins = config.get("admins", [])
        
        # Se não houver administradores, retorne
        if not admins:
            await interaction.response.send_message("Não há administradores cadastrados.", ephemeral=True)
            return
        
        # Gerar a lista de administradores com seus IDs e nomes
        admin_info = ""
        for admin in admins:
            user = await self.bot.fetch_user(int(admin))  # Obter o nome do usuário pelo ID
            admin_info += f"{user.name} ({admin})\n" if user else f"{admin} - [Membro não encontrado]\n"

        embed = discord.Embed(
            title="Administradores do Bot",
            description=f"Lista de Administradores:\n{admin_info}\n\nEscolha uma opção:",
            color=discord.Color.green()
        )

        # Botões para adicionar ou remover administradores
        view = View()

        button_add_admin = Button(label="Adicionar Administrador", style=discord.ButtonStyle.primary)
        button_add_admin.callback = self.add_admin
        view.add_item(button_add_admin)

        button_remove_admin = Button(label="Remover Administrador", style=discord.ButtonStyle.danger)
        button_remove_admin.callback = self.remove_admin
        view.add_item(button_remove_admin)

        # Botão de voltar
        button_back = Button(label="Voltar", style=discord.ButtonStyle.secondary)
        button_back.callback = self.go_back
        view.add_item(button_back)

        await interaction.response.edit_message(embed=embed, view=view)

    async def add_admin(self, interaction: discord.Interaction):
        # Abre o modal para adicionar um administrador
        modal = AddAdminModal()
        await interaction.response.send_modal(modal)

    async def remove_admin(self, interaction: discord.Interaction):
        config = embed_manager.load_config()
        admins = config.get("admins", [])
        
        # Se não houver administradores, retorne
        if not admins:
            await interaction.response.send_message("Não há administradores cadastrados para remover.", ephemeral=True)
            return

        # Criar opções para o Select Menu com nomes e IDs
        options = []
        for admin in admins:
            user = await self.bot.fetch_user(int(admin))  
            if user:
                options.append(discord.SelectOption(label=f"{user.name} ({admin})", value=admin))
            else:
                options.append(discord.SelectOption(label=f"{admin} - [Membro não encontrado]", value=admin))
        
        if not options:
            await interaction.response.send_message("Não há administradores válidos para remover.", ephemeral=True)
            return

        select = discord.ui.Select(placeholder="Selecione um administrador para remover", options=options)
        select.callback = self.remove_admin_action
        view = View()
        view.add_item(select)

        await interaction.response.send_message(embed=discord.Embed(
            title="Remover Administrador",
            description="Escolha um administrador para remover."
        ), view=view, ephemeral=True)

    async def remove_admin_action(self, interaction: discord.Interaction):
        selected_admin = interaction.data["values"][0]  
        config = embed_manager.load_config() 
        admins = config.get("admins", []) 

        if selected_admin in admins:
            admins.remove(selected_admin)  
          
            print(f"Administradores após remoção: {admins}")

            config["admins"] = admins  
            
            print(f"Administradores após remoção: {admins}")

            # Salva as novas configurações no arquivo
            embed_manager.save_config()  

            # Envia a confirmação de remoção
            await interaction.response.send_message(f"Administrador {selected_admin} removido com sucesso!", ephemeral=True)
        else:
            await interaction.response.send_message("O administrador selecionado não foi encontrado.", ephemeral=True)


    async def go_back(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Configuração do Bot",
            description="Escolha uma das opções abaixo para gerenciar o bot.",
            color=discord.Color.blue()
        )
        view = View()
        # Botões de funcionalidades gerais
        button_manage_admin = Button(label="Gerenciar Administradores", style=discord.ButtonStyle.primary)
        button_manage_admin.callback = self.manage_admins
        view.add_item(button_manage_admin)

        # Botão para conectar o bot em uma call
        button_connect_call = Button(label="Conectar Bot em Call", style=discord.ButtonStyle.secondary)
        button_connect_call.callback = self.connect_call
        view.add_item(button_connect_call)

        await interaction.response.edit_message(embed=embed, view=view)

    async def connect_call(self, interaction: discord.Interaction):
        # Pega todos os canais de voz do servidor
        guild = interaction.guild
        voice_channels = [channel for channel in guild.voice_channels]

        if not voice_channels:
            await interaction.response.send_message("Não há canais de voz disponíveis no servidor.", ephemeral=True)
            return

        # Cria o Select Menu para o usuário escolher um canal de voz
        options = [discord.SelectOption(label=channel.name, value=str(channel.id)) for channel in voice_channels]
        select = Select(placeholder="Escolha o canal de voz para conectar", options=options)
        select.callback = self.select_channel_callback
        view = View()
        view.add_item(select)

        await interaction.response.send_message("Escolha um canal para conectar o bot:", view=view, ephemeral=True)

    async def select_channel_callback(self, interaction: discord.Interaction):
        # Pega o canal selecionado pelo usuário
        channel_id = interaction.data["values"][0]
        channel = self.bot.get_channel(int(channel_id))

        # Verifica se o canal é de voz e se o bot tem permissão para se mutar
        if isinstance(channel, discord.VoiceChannel):
            voice_client = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

            if voice_client:
                if voice_client.channel.id != channel.id:
                    await voice_client.move_to(channel)
                    await interaction.response.send_message(f"Bot movido para o canal {channel.name}.", ephemeral=True)
                else:
                    await interaction.response.send_message(f"O bot já está no canal {channel.name}.", ephemeral=True)
            else:
                permissions = channel.permissions_for(interaction.guild.me)
                
                if not permissions.mute_members:
                    await interaction.response.send_message("O bot não tem permissão para se mutar neste canal.", ephemeral=True)
                    return

                voice_client = await channel.connect()

                voice_client.mute = True  
                voice_client.self_deaf = True  

                await interaction.response.send_message(f"Bot conectado ao canal {channel.name}", ephemeral=True)
        else:
            await interaction.response.send_message("Canal de voz inválido.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(ConfigBot(bot))
