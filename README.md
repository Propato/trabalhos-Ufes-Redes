# Servidor de Autenticação com Sockets

Este é o projeto desenvolvido na disciplina de Redes, com o objetivo de implementar um servidor para um dos desafios propostos, utilizando conceitos de redes e programação concorrente de soquetes.

## Desafio desenvolvido

Dos diversos desafios possíveis, o realizado foi sobre Autenticação e Autorização. Desenvolvendo um servidor de sockets concorrentes que realizam operações de Create User, Read Users, Login e Logout user e outras.

Há também níveis de usuários:
 
 - level 0: Unknown (Deslogado)
 - level 1: Comum user (usuário comum logado)
 - level 2: Adm

Como um extra do trabalho, outros desafios também se relacionam com o que foi proposto.

Os usuários podem fazer parte de equipes que os adm's criam, realizando operações que necessitam de tipos distintos de autorização e preparando certas estruturas no servidor para um sistema de jogos multiplayer de equipes ou de Chats de Múltiplas salas (substituindo as equipes por Salas).

## Especificações

Para informações precisas sobre requisitos, tecnologias e passo-a-passo, veja os READMEs mais detalhados do <a href="./server/README.md">Servidor</a> e do <a href="./client/README.md">Cliente</a>.

## Install

Para clonar o repositório e ter todos os códigos:

```bash
git clone <URL_DO_REPOSITORIO>
```

## O Projeto

Foi desenvolvido um servidor que apresenta ao cliente um Menu com diversas operações, que variam conforme o nível de usuário.

*É importante usar a biblioteca criada para o menor para que seja possível a comunicação correta e estruturada entre Cliente x Servidor.*

### Operações

#### Register

 - Level: 0 & 2
 
Realiza o registro de um usuário.

Caso um adm faça um registro, ele registrara um novo adm (nível de usuário 2).

#### Login

 - Level: 0

Realiza o login do usuário, validando user name e password e se ele já está logado no servidor.


#### Show teams

 - Level: 1 & 2

Mostra as equipes existentes.

Para usuários comum, mostra também o número de membros. Para adm's, mostra os membros (pelo endereço e nome).

#### Join team

 - Level: 1 & 2

Adiciona o Usuário logado a equipe escolhida, enviando o nome e senha dela.

#### Start team

 - Level: 2

Cria uma equipe, adicionando um nome e senha para ela.

#### Show online clients

 - Level: 2

Mostra os Usuários ativos no momento: Endereço e nome.

#### Logout

 - Level 1 & 2

Realiza o logout do usuário sem fechar o servidor.

#### Close

Encerra o cliente e fecha o servidor.

### Criptografia e Segurança

Além disto, como requisito do desafio, foi desenvolvida a criptografia das senhas dos usuários, garantindo maior segurança mesmo que as senhas sejam acessadas, seja de dentro do servidor ou por indivíduos externos.

#### Extra

Como um extra parte do desafio do Servidor de Chat com Suporte a Criptografia, foi implementado criptografia simétrica e assimétrica entre todas as mensagens do Servidor x Cliente.

Ao iniciar a conexão, o Servidor cria uma chave privada para o Cliente, enviando a pública para que ele criptografe suas mensagens de modo que apenas o servidor possa descriptografar e entender.

Além disto, assim que o cliente recebe a chave pública, ele a usa para criptografar a chave simétrica que ele criou para a sessão, enviando para o servidor a chave simétrica criptografada.

Assim, toda a comunicação do Cliente para Servidor passa por uma dupla criptografia:

 - Primeiro, usa-se a chave pública para criptografar.
 - Depois, usa-se a chave de sessão para criptografar novamente.

Já do Servidor para o Cliente, aplica-se apenas a criptografia com a chave de sessão.

### Melhorias e Possíveis Funcionalidades

 - Implementar demais operações CRUD
 - Implementar tempo limite de login para usuários inativos
 - Implementar suporte para Múltiplas salas de chat simultâneas
 - Implementar suporte para Jogos simples dentro de salas
 - Implementar novas classes para maior modularização e estruturação do Código
 - Implementar Super Classes para as classes do servidor e do cliente
 - Implementar Sistema de Testes
 - Adicionar mais comentários no código