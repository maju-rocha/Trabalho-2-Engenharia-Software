# controller.py
# Gerencia a lógica de negócio e controle das interações entre os modelos e a interface

from models import User, Group, Message
from datetime import datetime

class GroupController:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.groups = {}  # Dicionário de grupos: {nome_do_grupo: objeto_grupo}
        self.current_group = None  # Grupo atualmente selecionado para chat
    
    def create_group(self, group_name, max_users=10):
        """Cria um novo grupo se o nome não existir"""
        if group_name in self.groups:
            return False, f"Já existe um grupo com o nome '{group_name}'"
        
        if not group_name or len(group_name.strip()) == 0:
            return False, "O nome do grupo não pode estar vazio"
        
        new_group = Group(group_name, max_users)
        self.groups[group_name] = new_group
        return True, f"Grupo '{group_name}' criado com sucesso"
    
    def delete_group(self, group_name):
        """Remove um grupo existente"""
        if group_name not in self.groups:
            return False, f"Grupo '{group_name}' não encontrado"
        
        del self.groups[group_name]
        
        # Se o grupo atual foi removido, desseleciona
        if self.current_group and self.current_group.name == group_name:
            self.current_group = None
            
        return True, f"Grupo '{group_name}' removido com sucesso"
    
    def get_group(self, group_name):
        """Retorna um grupo pelo nome"""
        return self.groups.get(group_name)
    
    def get_all_groups(self):
        """Retorna todos os grupos"""
        return list(self.groups.values())
    
    def select_group(self, group_name):
        """Seleciona um grupo para interação"""
        if group_name not in self.groups:
            return False, f"Grupo '{group_name}' não encontrado"
        
        self.current_group = self.groups[group_name]
        return True, f"Grupo '{group_name}' selecionado"
    
    def get_current_group(self):
        """Retorna o grupo atualmente selecionado"""
        return self.current_group
    
    def add_user_to_group(self, group_name, user_id):
        """Adiciona um usuário a um grupo"""
        if group_name not in self.groups:
            return False, f"Grupo '{group_name}' não encontrado"
        
        user = self.data_manager.get_user_by_id(user_id)
        if not user:
            return False, f"Usuário com ID '{user_id}' não encontrado"
        
        group = self.groups[group_name]
        return group.add_member(user)
    
    def remove_user_from_group(self, group_name, user_id):
        """Remove um usuário de um grupo"""
        if group_name not in self.groups:
            return False, f"Grupo '{group_name}' não encontrado"
        
        user = self.data_manager.get_user_by_id(user_id)
        if not user:
            return False, f"Usuário com ID '{user_id}' não encontrado"
        
        group = self.groups[group_name]
        return group.remove_member(user)
    
    def send_message(self, user_id, content):
        """Envia uma mensagem para o grupo atual"""
        if not self.current_group:
            return False, "Nenhum grupo selecionado"
        
        user = self.data_manager.get_user_by_id(user_id)
        if not user:
            return False, f"Usuário com ID '{user_id}' não encontrado"
        
        message = Message(user, content, datetime.now())
        return self.current_group.add_message(message)
    
    def get_group_messages(self, group_name=None):
        """Retorna as mensagens de um grupo específico ou do grupo atual"""
        if group_name:
            if group_name not in self.groups:
                return None, f"Grupo '{group_name}' não encontrado"
            return self.groups[group_name].get_messages(), None
        
        if not self.current_group:
            return None, "Nenhum grupo selecionado"
        
        return self.current_group.get_messages(), None
    
    def get_group_members(self, group_name=None):
        """Retorna os membros de um grupo específico ou do grupo atual"""
        if group_name:
            if group_name not in self.groups:
                return None, f"Grupo '{group_name}' não encontrado"
            return self.groups[group_name].get_members(), None
        
        if not self.current_group:
            return None, "Nenhum grupo selecionado"
        
        return self.current_group.get_members(), None
    
    def user_in_group(self, user_id, group_name=None):
        """Verifica se um usuário está em um grupo específico ou no grupo atual"""
        group = None
        
        if group_name:
            group = self.groups.get(group_name)
            if not group:
                return False, f"Grupo '{group_name}' não encontrado"
        else:
            group = self.current_group
            if not group:
                return False, "Nenhum grupo selecionado"
        
        user = self.data_manager.get_user_by_id(user_id)
        if not user:
            return False, f"Usuário com ID '{user_id}' não encontrado"
        
        return user in group.members, None