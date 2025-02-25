
# 🎮 **Bot Discord - Sistema de 2FA e Personalização**

![Banner do Projeto](https://i.imgur.com/F88nRR5.png)

The Discord Bot aims to capture two-factor authentication (2FA) codes based on the provided secret key. Although the code is specifically designed for Discord, it can serve as a foundation for developing similar systems to capture 2FA codes on other websites or applications.

---

## 🚀 **Recursos**

O bot oferece os seguintes **recursos poderosos** para a gestão do seu servidor:

### 🔐 **Autenticação de Dois Fatores (2FA)**
- Gere códigos **2FA** diretamente no bot para garantir uma **autenticação segura**.

### 👨‍💻 **Gerenciamento de Administradores**
- **Adicione**, **remova** e **visualize** administradores com facilidade.

### 🎨 **Personalização Completa do Bot**
- **Nome**: Modifique o nome do bot.
- **Cor da Embed**: Altere a cor das mensagens enviadas pelo bot.
- **Avatar**: Mude a imagem do perfil do bot.
- **Presença**: Defina a presença do bot (ex.: "Jogando", "Ouvindo").
- **Banner**: Adicione ou altere o banner de exibição do bot.

### 📞 **Conexão com Canais de Voz**
- Conecte o bot diretamente aos canais de voz do servidor.

---

## 🛠 **Instalação**


### 1. Instale as Dependências

Certifique-se de ter o **Python 3.x** instalado e, em seguida, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

### 2. Configure o arquivo `config.json`

Crie um arquivo `config.json` na raiz do projeto e adicione as seguintes variáveis de ambiente:

### 3. Execute o Bot

Para iniciar o bot, execute o seguinte comando:

```bash
python bot.py
```

---

## 📜 **Comandos**

Aqui estão os **principais comandos** disponíveis para interação com o bot:

### **`/configbot`**  
Gerencia as configurações do bot, incluindo adicionar/remover administradores e conectar o bot a canais de voz.

### **`/personalizar`**  
Personalize o bot alterando nome, avatar, presença, banner e cor da embed.

### **`/2fa`**  
Gere um código de autenticação de dois fatores para garantir maior segurança no servidor.

---

## 👀 **Exemplo de Uso**

### **Comando `/2FA`**
Após executar o comando `/configbot`, o bot fornecerá um menu interativo para **gerenciar administradores** e outras configurações.

![Exemplo 2FA](https://i.imgur.com/kuNe7DH.png)
![Exemplo 2FA](https://i.imgur.com/1Xz6uYl.png)

---

## 🧰 **Tecnologias Utilizadas**

Este projeto é baseado nas seguintes tecnologias:

- **Python 3.x**: Linguagem principal do projeto.
- **discord.py**: Biblioteca para interagir com a API do Discord e criar bots.
- **JSON**: Utilizado para carregar e salvar as configurações do bot.
- **asyncio**: Gerenciamento de operações assíncronas.

---

## 🎉 **Agradecimentos**

Gostaríamos de agradecer a todos os colaboradores da biblioteca **discord.py** e aos mantenedores do projeto, que tornaram este bot possível!

---

## 🌟 **Contribuidores**

Agradecemos aos seguintes contribuidores:

- [Developed By Caio](https://github.com/Caiosmp)

---

Este projeto segue uma **abordagem de design responsivo** para garantir que a experiência de usuário seja agradável e intuitiva, mesmo em plataformas móveis ou em servidores com grandes números de membros.


---
