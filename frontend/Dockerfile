# Usa una imagen base de Node.js
FROM node:16 AS build

# Configura el directorio de trabajo dentro del contenedor
WORKDIR /home
# Copia los archivos de configuración de npm
COPY package.json package-lock.json ./

# Instala las dependencias
RUN npm install

# Copia el resto del código fuente
COPY . .

# Construye la aplicación para producción
RUN npm run build

# Instalar react-scripts antes de construir
RUN npm install --save react-scripts


# Usa nginx para servir la aplicación en producción
FROM nginx:alpine

# Copia los archivos construidos al servidor nginx
COPY --from=build /home/build /usr/share/nginx/html

# Exponer el puerto 80
EXPOSE 80

# Iniciar nginx
CMD ["nginx", "-g", "daemon off;"]
