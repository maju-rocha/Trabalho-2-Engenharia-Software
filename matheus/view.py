# view.py
# Interface via terminal para interação com o usuário

import os
from datetime import datetime

class TerminalView:
    def __init__(self, controller):
        self.controller = controller
    
    def clear_screen(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_welcome(self):
        """Exibe mensagem de boas-vindas"""
        self.clear_screen()
        print("====================================================")
        print("  SISTEMA DE GRUPOS DE ESTUDO COM CHAT EM TERMINAL")
        print("====================================================")
        print("Desenvolvido para a disciplina de Engenharia de Software")
        print("\n")
    
    def show_main_menu(self):
        """Exibe o menu principal"""
        print("\nMENU PRINCIPAL")
        print("1. Criar novo grupo")
        print("2. Listar grupos existentes")
        print("3. Gerenciar grupo")
        print("4. Entrar em um chat de grupo")
        print("0. Sair")
        return input("\nEscolha uma opção: ")
    
    def create_group_menu(self):
        """Menu para criação de grupo"""
        self.clear_screen()
        print("===== CRIAR NOVO GRUPO =====\n")
        
        group_name = input("Nome do grupo: ")
        try:
            max_users = int(input("Número máximo de usuários (padrão: 10): ") or "10")
        except ValueError:
            max_users = 10
            print("Valor inválido. Usando o padrão: 10 usuários.")
        
        success, message = self.controller.create_group(group_name, max_users)
        print(f"\n{message}")
        input("\nPressione ENTER para continuar...")
    
    def list_groups(self):
        """Lista todos os grupos existentes"""
        self.clear_screen()
        print("===== GRUPOS EXISTENTES =====\n")
        
        groups = self.controller.get_all_groups()
        if not groups:
            print("Não há grupos cadastrados.")
        else:
            for i, group in enumerate(groups, 1):
                print(f"{i}. {group.name} ({len(group.members)}/{group.max_users} membros)")
        
        input("\nPressione ENTER para continuar...")
    
    def manage_group_menu(self):
        """Menu para gerenciar um grupo"""
        while True:
            self.clear_screen()
            print("===== GERENCIAR GRUPO =====\n")
            
            groups = self.controller.get_all_groups()
            if not groups:
                print("Não há grupos cadastrados.")
                input("\nPressione ENTER para continuar...")
                return
            
            print("Selecione um grupo:")
            for i, group in enumerate(groups, 1):
                print(f"{i}. {group.name}")
            print("0. Voltar")
            
            try:
                choice = int(input("\nEscolha uma opção: "))
                if choice == 0:
                    return
                
                if 1 <= choice <= len(groups):
                    selected_group = groups[choice-1]
                    self.manage_specific_group(selected_group.name)
                else:
                    print("\nOpção inválida!")
                    input("Pressione ENTER para continuar...")
            except ValueError:
                print("\nOpção inválida!")
                input("Pressione ENTER para continuar...")
    
    def manage_specific_group(self, group_name):
        """Menu para gerenciar um grupo específico"""
        while True:
            self.clear_screen()
            group = self.controller.get_group(group_name)
            if not group:
                print(f"Grupo '{group_name}' não encontrado!")
                input("\nPressione ENTER para continuar...")
                return
            
            print(f"===== GERENCIANDO GRUPO: {group.name} =====\n")
            print(f"Membros: {len(group.members)}/{group.max_users}")
            print("\nOpções:")
            print("1. Adicionar usuário")
            print("2. Remover usuário")
            print("3. Listar membros")
            print("4. Excluir grupo")
            print("0. Voltar")
            
            try:
                choice = int(input("\nEscolha uma opção: "))
                
                if choice == 0:
                    return
                elif choice == 1:
                    self.add_user_to_group(group_name)
                elif choice == 2:
                    self.remove_user_from_group(group_name)
                elif choice == 3:
                    self.list_group_members(group_name)
                elif choice == 4:
                    if self.confirm_delete_group(group_name):
                        return
                else:
                    print("\nOpção inválida!")
                    input("Pressione ENTER para continuar...")
            except ValueError:
                print("\nOpção inválida!")
                input("Pressione ENTER para continuar...")
    
    def add_user_to_group(self, group_name):
        """Adiciona um usuário ao grupo"""
        self.clear_screen()
        print(f"===== ADICIONAR USUÁRIO AO GRUPO: {group_name} =====\n")
        
        # Listar usuários disponíveis
        all_users = self.controller.data_manager.get_all_users()
        if not all_users:
            print("Não há usuários cadastrados no sistema.")
            input("\nPressione ENTER para continuar...")
            return
        
        print("Usuários disponíveis:")
        for user in all_users:
            print(f"ID: {user.id}, Nome: {user.name}, Email: {user.email}")
        
        user_id = input("\nDigite o ID do usuário que deseja adicionar: ")
        success, message = self.controller.add_user_to_group(group_name, user_id)
        print(f"\n{message}")
        input("\nPressione ENTER para continuar...")
    
    def remove_user_from_group(self, group_name):
        """Remove um usuário do grupo"""
        self.clear_screen()
        print(f"===== REMOVER USUÁRIO DO GRUPO: {group_name} =====\n")
        
        # Listar membros do grupo
        members, error = self.controller.get_group_members(group_name)
        if error:
            print(error)
            input("\nPressione ENTER para continuar...")
            return
        
        if not members:
            print("O grupo não possui membros.")
            input("\nPressione ENTER para continuar...")
            return
        
        print("Membros do grupo:")
        for user in members:
            print(f"ID: {user.id}, Nome: {user.name}, Email: {user.email}")
        
        user_id = input("\nDigite o ID do usuário que deseja remover: ")
        success, message = self.controller.remove_user_from_group(group_name, user_id)
        print(f"\n{message}")
        input("\nPressione ENTER para continuar...")
    
    def list_group_members(self, group_name):
        """Lista os membros de um grupo"""
        self.clear_screen()
        print(f"===== MEMBROS DO GRUPO: {group_name} =====\n")
        
        members, error = self.controller.get_group_members(group_name)
        if error:
            print(error)
        elif not members:
            print("O grupo não possui membros.")
        else:
            for i, user in enumerate(members, 1):
                print(f"{i}. {user.name} ({user.email})")
        
        input("\nPressione ENTER para continuar...")
    
    def confirm_delete_group(self, group_name):
        """Confirma a exclusão de um grupo"""
        self.clear_screen()
        print(f"===== EXCLUIR GRUPO: {group_name} =====\n")
        print("ATENÇÃO: Esta ação não pode ser desfeita!")
        confirm = input("\nDigite o nome do grupo para confirmar a exclusão: ")
        
        if confirm == group_name:
            success, message = self.controller.delete_group(group_name)
            print(f"\n{message}")
            input("\nPressione ENTER para continuar...")
            return True
        else:
            print("\nNome do grupo não corresponde. Operação cancelada.")
            input("\nPressione ENTER para continuar...")
            return False
    
    def chat_menu(self):
        """Menu para entrar em um chat de grupo"""
        while True:
            self.clear_screen()
            print("===== CHAT DE GRUPO =====\n")
            
            groups = self.controller.get_all_groups()
            if not groups:
                print("Não há grupos cadastrados.")
                input("\nPressione ENTER para continuar...")
                return
            
            print("Selecione um grupo para entrar no chat:")
            for i, group in enumerate(groups, 1):
                print(f"{i}. {group.name} ({len(group.members)} membros)")
            print("0. Voltar")
            
            try:
                choice = int(input("\nEscolha uma opção: "))
                if choice == 0:
                    return
                
                if 1 <= choice <= len(groups):
                    selected_group = groups[choice-1]
                    success, message = self.controller.select_group(selected_group.name)
                    if success:
                        self.enter_chat(selected_group.name)
                    else:
                        print(f"\n{message}")
                        input("\nPressione ENTER para continuar...")
                else:
                    print("\nOpção inválida!")
                    input("Pressione ENTER para continuar...")
            except ValueError:
                print("\nOpção inválida!")
                input("Pressione ENTER para continuar...")
    
    def enter_chat(self, group_name):
        """Interface de chat para um grupo específico"""
        self.clear_screen()
        print(f"===== CHAT DO GRUPO: {group_name} =====\n")
        print("Digite 'sair' para voltar ao menu anterior.")
        print("Digite 'usuarios' para ver os usuários online.")
        print("Digite 'limpar' para limpar a tela.")
        print("\n--- Início da conversa ---")
        
        # Exibe mensagens anteriores
        messages, _ = self.controller.get_group_messages(group_name)
        if messages:
            for msg in messages:
                print(f"{msg.sender.name}: {msg.content}")
        
        # Solicita ID do usuário para o chat
        user_id = input("\nDigite seu ID de usuário para entrar no chat: ")
        is_member, error = self.controller.user_in_group(user_id, group_name)
        
        if error:
            print(f"\n{error}")
            input("\nPressione ENTER para continuar...")
            return
        
        if not is_member:
            print("\nVocê não é membro deste grupo. Apenas membros podem participar do chat.")
            input("\nPressione ENTER para continuar...")
            return
        
        user = self.controller.data_manager.get_user_by_id(user_id)
        print(f"\nBem-vindo(a) ao chat, {user.name}!")
        
        while True:
            message_content = input("\n> ")
            
            if message_content.lower() == 'sair':
                break
            elif message_content.lower() == 'usuarios':
                members, _ = self.controller.get_group_members(group_name)
                print("\nUsuários no grupo:")
                for member in members:
                    print(f"- {member.name}")
            elif message_content.lower() == 'limpar':
                self.clear_screen()
                print(f"===== CHAT DO GRUPO: {group_name} =====\n")
                print("Digite 'sair' para voltar ao menu anterior.")
                print("Digite 'usuarios' para ver os usuários online.")
                print("Digite 'limpar' para limpar a tela.")
                print("\n--- Conversa ---")
            elif message_content.strip():
                success, message = self.controller.send_message(user_id, message_content)
                if not success:
                    print(f"Erro: {message}")
    
    def run(self):
        """Executa o loop principal da aplicação"""
        self.show_welcome()
        
        while True:
            choice = self.show_main_menu()
            
            if choice == '0':
                self.clear_screen()
                print("Obrigado por usar o Sistema de Grupos de Estudo!")
                print("Encerrando...")
                break
            elif choice == '1':
                self.create_group_menu()
            elif choice == '2':
                self.list_groups()
            elif choice == '3':
                self.manage_group_menu()
            elif choice == '4':
                self.chat_menu()
            else:
                print("\nOpção inválida! Por favor, tente novamente.")
                input("Pressione ENTER para continuar...")