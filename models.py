# models.py
# Define as classes User, Group e Message para o sistema de chat de grupos de estudo

class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

class Message:
    def __init__(self, sender, content, timestamp=None):
        self.sender = sender  # Objeto User
        self.content = content
        self.timestamp = timestamp  # Opcional, pode ser implementado posteriormente
    
    def __str__(self):
        return f"{self.sender.name}: {self.content}"

class Group:
    def __init__(self, name, max_users=10):
        self.name = name
        self.members = []  # Lista de objetos User
        self.messages = []  # Lista de objetos Message
        self.max_users = max_users
    
    def add_member(self, user):
        """Adiciona um usuário ao grupo se ele não estiver presente e se houver espaço"""
        if user in self.members:
            return False, "Usuário já é membro do grupo"
        
        if len(self.members) >= self.max_users:
            return False, f"O grupo atingiu o limite máximo de {self.max_users} membros"
        
        self.members.append(user)
        return True, f"Usuário {user.name} adicionado ao grupo {self.name}"
    
    def remove_member(self, user):
        """Remove um usuário do grupo se ele estiver presente"""
        if user not in self.members:
            return False, "Usuário não é membro do grupo"
        
        self.members.remove(user)
        return True, f"Usuário {user.name} removido do grupo {self.name}"
    
    def add_message(self, message):
        """Adiciona uma mensagem ao histórico do grupo se o remetente for membro"""
        if message.sender not in self.members:
            return False, "Apenas membros podem enviar mensagens para o grupo"
        
        self.messages.append(message)
        return True, "Mensagem enviada com sucesso"
    
    def get_messages(self):
        """Retorna todas as mensagens do grupo"""
        return self.messages
    
    def get_members(self):
        """Retorna todos os membros do grupo"""
        return self.members
    
    def __str__(self):
        return f"Grupo: {self.name} ({len(self.members)} membros)"