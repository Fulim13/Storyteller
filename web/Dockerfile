FROM node:16-alpine

WORKDIR /app/web/

COPY package*.json /app/web/
RUN npm install

COPY . /app/web/

CMD ["npm", "run","dev"]
