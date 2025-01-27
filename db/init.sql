DO $$
BEGIN
  -- Создание пользователя, если он не существует
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'user') THEN
    CREATE USER "user" WITH SUPERUSER PASSWORD '123';
  END IF;

  -- Создание базы данных, если она не существует
  IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'wallet123') THEN
    CREATE DATABASE wallet123 OWNER "user";
  END IF;

  -- Предоставление прав пользователю на базу данных
  GRANT ALL PRIVILEGES ON DATABASE wallet123 TO "user";
END $$;