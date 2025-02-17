# Servidor

Este projeto consiste no Servidor de Sockets.

A comunicação com o cliente é baseada em uma rotina de:

 - Escrita
 - Leitura
 - Confirmação/Negação

## Classes 

Foram desenvolvidas Três Classes: Server, Client e UI.

### Server

A classe Server é responsável por realizar as conexões com os clientes e criar novos sockets, associando-os à novas threads, para tratar o cliente.

É nela também onde ficam armazenados todos os dados (usuários, clientes, etc).

### Cliente

A classe Cliente tem a responsabilidade de lidar com o cliente, realizando as operações, trocas de mensagens e criptografia.

### UI

A classe UI tem a tarefa de formatar e montar mensagens para que fiquem mais organizadas, claras e apresentáveis.

## Pré-Requisitos
 
 - Sistemas Linux
 - Python3: v3.12.3
    - bcrypt: v3.2.2
    - cryptography: v41.0.7

*Outros OS também podem funcionar, mas não foram validados.*

## Setup

Antes de rodar, é necessário ter instalado todas as ferramentas.

Considerando que a maquina já possui python3 e pip instalados:

```bash
sudo pip install -r requirements.txt
```

Caso seu sistema não utilize pip para instalar bibliotecas (como o meu):

```bash
sudo apt install python3-bcrypt
sudo apt install python3-cryptography
```

## Running

Para executar, é possível definir os valores desejados do endereço do servidor, número máximo de clientes e número máximo de equipes (Valores já pré-definidos). Com isto, execute:

```bash
python3 index.py
```

Pronto, seu servidor já está online.

Para encerrar a thread do Servidor, basta `Ctrl+C`.
