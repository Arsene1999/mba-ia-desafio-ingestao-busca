from search import search_prompt

def main():
    while(True):
        query = input("O que você deseja saber sobre o documento? (Digite 'sair' para encerrar o chat)\n> ")
        
        if(query.lower() in ["sair", "exit", "quit"]):
            print("Encerrando o chat. Até mais!")
            break
        
        chain = search_prompt(query)
        
        if not chain:
            print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
            return
        
    pass

if __name__ == "__main__":
    main()