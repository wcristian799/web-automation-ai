# Baseado na imagem oficial do Node
FROM node:14

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Primeiro copia apenas os arquivos package.json e package-lock.json
COPY package*.json ./

# Instala as dependências do projeto
RUN npm install

# Agora, copia o restante dos arquivos do projeto
COPY . .

# Compila o aplicativo para produção
RUN npm run build

# Instala o serve para servir o app construído
RUN npm install -g serve

# Define o comando para iniciar o app
["npx", "serve", "-s", "build"]  
