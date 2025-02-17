# Cliente

Este projeto consiste em uma biblioteca de Sockets para o Cliente se conectar e acessar ao Servidor.

Seu objetivo é ser uma interface simples para que qualquer um com o client.py possa repetir o processo, criando apenas o index.py.

## Classes 

Foi desenvolvido uma Classe para o sistema: ClientConnection.

### ClientConnection

A classe é responsável por realizar a conexão com o Servidor, criptografando suas mensagens e a sessão, em um eterno loop baseado em:

 - Leitura
 - Escrita
 - Confirmação

## Pré-Requisitos
 
 - Sistemas Linux
 - Python3: v3.12.3
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
sudo apt install python3-cryptography
```

## Running

Para executar, é possível definir os valores do endereço do servidor (já pré-definido no index.py). Com isto, execute:

```bash
python3 index.py
```

Pronto, seu Cliente está ativo e conectado ao Servidor (se este estiver ativo).

Para encerrar a thread do Servidor, basta enviar `close` em qualquer momento.
