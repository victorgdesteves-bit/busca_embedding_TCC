-- Execute este script como root ou usuário com privilégios administrativos

CREATE DATABASE IF NOT EXISTS busca_semantica 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'busca_user'@'localhost'

IDENTIFIED BY 'busca_password_123';

GRANT ALL PRIVILEGES ON busca_semantica.* TO 'busca_user'@'localhost';

FLUSH PRIVILEGES;

USE busca_semantica;

SELECT 'Banco de dados configurado com sucesso!' as status;
