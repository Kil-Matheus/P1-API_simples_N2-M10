# P1-API_simples_N2-M10

# Introdução
 É uma aplicação em Flask API de autenticação que utiliza JWT como requisito de segurança e operações básicos de banco de dados, o CRUD (CREAT, READ, UPDATE and DELETE)

 ## Dependências
- Flask
- Flask SQLAlchemy
- Flask JWT Extended

## Configuração do Aplicativo
- `template_folder` é configurado para o diretório "templates".
- O banco de dados é configurado para SQLite, com o arquivo "project.db".
- A chave secreta para o JWT é definida como "goku-vs-vegeta".
- O local de armazenamento do token JWT é configurado como cookies.

## Rotas

### /login (POST)
- Rota para autenticação de usuários.
- Recebe o nome de usuário e a senha através do formulário.
- Retorna um token JWT após a autenticação bem-sucedida.

### /token (POST)
- Rota para criar um token JWT.
- Recebe o nome de usuário e a senha no formato JSON.
- Verifica as credenciais no banco de dados.
- Retorna um token JWT com o ID do usuário.

### /user-register (GET)
- Rota para exibir o formulário de registro de usuário.

### /user-login (GET)
- Rota para exibir o formulário de login de usuário.

### / (GET)
- Rota raiz que retorna uma simples mensagem "Hello, World!".

### /users (GET)
- Rota para obter todos os usuários cadastrados.

### /users/<int:id> (GET)
- Rota para obter um usuário específico pelo ID.

### /users (POST)
- Rota para criar um novo usuário.
- Recebe os dados do usuário em formato JSON.

### /users/<int:id> (PUT)
- Rota para atualizar os dados de um usuário existente pelo ID.
- Recebe os novos dados do usuário em formato JSON.

### /users/<int:id> (DELETE)
- Rota para excluir um usuário pelo ID.

### /content (GET)
- Rota protegida que exibe o conteúdo após a autenticação.

### /error (GET)
- Rota para exibir uma página de erro.

# Referências

O desenvolvimento realiza foi como parte de um exercício oferecido pelo Professor Murilo, na qual fica em anexo o link da atividade.

***Atividade*** : https://murilo-zc.github.io/M10-Inteli-Eng-Comp/Encontros/encontro_01/intro_ponderada
***Referência do exercício***: https://murilo-zc.github.io/M10-Inteli-Eng-Comp/Encontros/encontro_01/nivel2

## Flutter fazendo requisições POST e GET para o Docker(Flask Backend)

link: https://drive.google.com/file/d/1WMpE_nLtcPsC6UDlH_3_KKSOerRK_25D/view?usp=sharing