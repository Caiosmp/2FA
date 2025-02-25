# utils/config_loader.py

import json

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Arquivo config.json não encontrado.")
        return None
    except json.JSONDecodeError as e:
        print(f"Erro ao ler o arquivo JSON: {str(e)}")
        return None
