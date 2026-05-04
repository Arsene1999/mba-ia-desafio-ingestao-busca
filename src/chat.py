from search import search_prompt

def main():
    query = input("O que você deseja saber sobre o documento? ")
    search_prompt(query)
    chain = search_prompt(query)

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    pass

if __name__ == "__main__":
    main()