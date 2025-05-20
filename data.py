# data.py
# Responsável pela leitura e validação dos dados de usuários do arquivo CSV

import csv
from models import User

class DataManager:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.users = []
        self.load_users()
    
    def load_users(self):
        """Carrega os usuários do arquivo CSV"""
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                # Pula o cabeçalho se existir
                header = next(csv_reader, None)
                
                # Determina os índices das colunas (assumindo id, nome, email)
                id_idx, name_idx, email_idx = 0, 1, 2
                
                for row in csv_reader:
                    if len(row) >= 3:  # Verifica se a linha tem dados suficientes
                        user_id = row[id_idx]
                        name = row[name_idx]
                        email = row[email_idx]
                        
                        # Cria um novo usuário e adiciona à lista
                        user = User(user_id, name, email)
                        self.users.append(user)
            return True, f"Carregados {len(self.users)} usuários com sucesso"
        except FileNotFoundError:
            return False, f"Arquivo {self.csv_file_path} não encontrado"
        except Exception as e:
            return False, f"Erro ao carregar usuários: {str(e)}"
    
    def get_all_users(self):
        """Retorna todos os usuários carregados"""
        return self.users
    
    def get_user_by_id(self, user_id):
        """Busca um usuário pelo ID"""
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def get_user_by_name(self, name):
        """Busca um usuário pelo nome (pode retornar múltiplos usuários)"""
        matching_users = [user for user in self.users if user.name.lower() == name.lower()]
        return matching_users
    
    def get_user_by_email(self, email):
        """Busca um usuário pelo email"""
        for user in self.users:
            if user.email.lower() == email.lower():
                return user
        return None
    
    def create_sample_csv(self):
        """Cria um arquivo CSV de exemplo com alguns usuários"""
        try:
            with open(self.csv_file_path, 'w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                # Escreve o cabeçalho
                csv_writer.writerow(['id', 'nome', 'email'])
                # Escreve alguns usuários de exemplo
                csv_writer.writerow(['1', 'João Silva', 'joao@exemplo.com'])
                csv_writer.writerow(['2', 'Maria Santos', 'maria@exemplo.com'])
                csv_writer.writerow(['3', 'Pedro Oliveira', 'pedro@exemplo.com'])
                csv_writer.writerow(['4', 'Ana Souza', 'ana@exemplo.com'])
                csv_writer.writerow(['5', 'Carlos Ferreira', 'carlos@exemplo.com'])
            return True, f"Arquivo CSV de exemplo criado em {self.csv_file_path}"
        except Exception as e:
            return False, f"Erro ao criar arquivo CSV de exemplo: {str(e)}"