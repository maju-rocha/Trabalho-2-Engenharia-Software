#!/usr/bin/env python3

"""
Sistema de fórum de perguntas e respostas em terminal.
Objetivo: permitir que alunos postem perguntas e respostas de forma colaborativa.
As perguntas são identificadas pelo RA do autor.
"""

def main():
    # Lista de perguntas: cada pergunta é um dict com RA, user, text, answers
    questions = []
    # Em vez de gerar RA automaticamente, solicitamos RA ao postar pergunta

    print("Bem-vindo ao fórum de perguntas e respostas!")
    # Solicita nome de usuário inicial
    user = input("Digite seu nome: ").strip()

    while True:
        # Exibe menu de opções
        print("\nMenu:")
        print("1. Fazer pergunta")
        print("2. Listar perguntas")
        print("3. Responder pergunta")
        print("4. Ver respostas de uma pergunta pelo RA")
        print("5. Trocar usuário")
        print("0. Sair")
        choice = input("Escolha uma opção: ").strip()

        if choice == '1':
            # Postar nova pergunta solicitando RA
            try:
                ra = input("Digite seu RA: ").strip()
            except Exception:
                print("RA inválido.")
                continue
            question_text = input("Digite sua pergunta: ").strip()
            questions.append({
                'RA': ra,
                'user': user,
                'text': question_text,
                'answers': []
            })
            print(f"Pergunta registrada com RA {ra}.")

        elif choice == '2':
            # Listar todas as perguntas
            if not questions:
                print("Nenhuma pergunta registrada.")
            else:
                print("Perguntas:")
                for q in questions:
                    print(f"RA {q['RA']}: ({q['user']}) {q['text']}")

        elif choice == '3':
            # Responder a uma pergunta existente por RA
            if not questions:
                print("Nenhuma pergunta disponível para responder.")
                continue
            ra = input("Digite o RA da pergunta que deseja responder: ").strip()
            selected = next((q for q in questions if q['RA'] == ra), None)
            if not selected:
                print("Pergunta não encontrada para o RA informado.")
                continue
            answer_text = input("Digite sua resposta: ").strip()
            selected['answers'].append({
                'user': user,
                'text': answer_text
            })
            print("Resposta registrada.")

        elif choice == '4':
            # Exibir respostas de uma pergunta específica por RA
            if not questions:
                print("Nenhuma pergunta registrada.")
                continue
            ra = input("Digite o RA da pergunta para ver respostas: ").strip()
            selected = next((q for q in questions if q['RA'] == ra), None)
            if not selected:
                print("Pergunta não encontrada para o RA informado.")
                continue
            print(f"\nPergunta (RA {selected['RA']}): {selected['text']} (por {selected['user']})")
            if not selected['answers']:
                print("Nenhuma resposta para esta pergunta.")
            else:
                print("Respostas:")
                for i, a in enumerate(selected['answers'], start=1):
                    print(f"{i}. ({a['user']}) {a['text']}")

        elif choice == '5':
            # Trocar usuário atual
            user = input("Digite o novo nome de usuário: ").strip()
            print(f"Usuário alterado para {user}.")

        elif choice == '0':
            # Encerrar o programa
            print("Saindo do fórum. Até mais!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
