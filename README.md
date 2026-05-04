# Desafio MBA Engenharia de Software com IA - Full Cycle

Este projeto foi feito inteiramente com a api da OpenAi e não usa a do google.
Ele possui um run time para calcular o tempo de cada pergunta feita.

# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate

# Subir Banco de Dados 
docker compose up -d

# Ativar script de Ingestão para o arquivo .\document.pdf
python src/ingest.py

# Ativar o Chat 
python src/chat.py

# Uso do chat 
Perguntas sobre os dados do pdf vetorizado e sair ou exit para sair