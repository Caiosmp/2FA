# utils/buttons.py

import discord
from views.modals import ChangeNameModal, ChangeEmbedColorModal, ChangeAvatarModal, ChangePresenceModal, ChangeBannerModal

class ButtonManager:
    def __init__(self):
        pass

    def create_personalization_buttons(self):
        view = discord.ui.View()

        # Botão para mudar o nome do bot
        button_name = discord.ui.Button(label="Mudar Nome", style=discord.ButtonStyle.primary)
        button_name.callback = lambda interaction: interaction.response.send_modal(ChangeNameModal())
        view.add_item(button_name)

        # Botão para mudar a cor da embed
        button_color = discord.ui.Button(label="Mudar Cor da Embed", style=discord.ButtonStyle.secondary)
        button_color.callback = lambda interaction: interaction.response.send_modal(ChangeEmbedColorModal())
        view.add_item(button_color)

        # Botão para mudar o avatar do bot
        button_avatar = discord.ui.Button(label="Mudar Avatar", style=discord.ButtonStyle.success)
        button_avatar.callback = lambda interaction: interaction.response.send_modal(ChangeAvatarModal())
        view.add_item(button_avatar)

        # Botão para mudar a presença do bot
        button_presence = discord.ui.Button(label="Mudar Presença", style=discord.ButtonStyle.primary)
        button_presence.callback = lambda interaction: interaction.response.send_modal(ChangePresenceModal())
        view.add_item(button_presence)

        # Botão para adicionar/alterar o banner da embed
        button_banner = discord.ui.Button(label="Adicionar/Alterar Banner", style=discord.ButtonStyle.primary)
        button_banner.callback = lambda interaction: interaction.response.send_modal(ChangeBannerModal())
        view.add_item(button_banner)

        return view
