# main.py
# Ponto de entrada do sistema de chat de grupos de estudo

import os
from data import DataManager
from controller import GroupController
from view import TerminalView

def main():
    # Definir o caminho do arquivo CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'users.csv')
    
    # Inicializar o gerenciador de dados
    data_manager = DataManager(csv_path)
    
    # Verificar se o arquivo CSV existe, caso contrário, criar um exemplo
    if not os.path.exists(csv_path):
        success, message = data_manager.create_sample_csv()
        print(message)
    
    # Inicializar o controlador com o gerenciador de dados
    controller = GroupController(data_manager)
    
    # Inicializar a interface do terminal
    view = TerminalView(controller)
    
    # Executar o loop principal da aplicação
    view.run()

if __name__ == "__main__":
    main()