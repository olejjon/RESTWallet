## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/olejjon/RESTWallet.git
   cd RESTWallet
   
2. Запуск:
   ```bash
   docker build -t restwallet
   docker-compose up -d

### Создание кошелька
```bash

Запрос по "http://127.0.0.1:8000/api/v1/wallets/":
{
  "uuid": "wallet_2",
  "balance": 100.0
}


Ответ:
{
    "message": "Wallet created successfully",
    "wallet": {
        "uuid": "wallet_2",
        "balance": 100.0
    }
}
```

### Пополнение баланса
```bash

Запрос по "http://127.0.0.1:8000/api/v1/wallets/wallet_1/operation":
{
  "operationType": "DEPOSIT",
  "amount": 2500
}

Ответ:
{
    "message": "Operation successful"
}
```