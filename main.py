import time
import random
from web3 import Web3

# ✅ Настройки RPC для Ethereum Mainnet
RPC_URL = "https://ethereum-rpc.publicnode.com"  # Замените на ваш RPC-ключ
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Проверка соединения
if not web3.is_connected():
    raise Exception("❌ Не удалось подключиться к RPC-узлу Ethereum Mainnet")

# 🎯 Диапазон отправки ETH (в ETH)
MIN_AMOUNT_TO_SEND_ETH = 0.065
MAX_AMOUNT_TO_SEND_ETH = 0.07

# Задержки
MIN_DELAY = 2000
MAX_DELAY = 10000
BALANCE_CHECK_DELAY = 1

# Загрузка кошельков из файла
def load_wallets(file_path):
    wallets = []
    with open(file_path, "r") as file:
        for line in file:
            private_key, receiver_address = line.strip().split(":")
            if not private_key.startswith("0x"):
                private_key = "0x" + private_key
            wallets.append((private_key, receiver_address))
    return wallets

# Проверка баланса
def check_balances(wallets):
    print("\n--- Проверка баланса кошельков (Mainnet) ---\n")
    for private_key, receiver_address in wallets:
        sender_address = web3.eth.account.from_key(private_key).address
        balance = web3.eth.get_balance(sender_address)
        eth_balance = web3.from_wei(balance, "ether")
        print(f"Адрес: {sender_address} | Баланс: {eth_balance:.6f} ETH")
        time.sleep(BALANCE_CHECK_DELAY)
    print("\n✅ Проверка баланса завершена.\n")

# Отправка ETH в случайном диапазоне
def send_eth(private_key, receiver_address):
    account = web3.eth.account.from_key(private_key)
    sender_address = account.address
    balance = web3.eth.get_balance(sender_address)
    eth_balance = web3.from_wei(balance, "ether")
    print(f"Баланс {sender_address}: {eth_balance:.6f} ETH")

    # Случайное значение в ETH и перевод в wei
    random_amount_eth = round(random.uniform(MIN_AMOUNT_TO_SEND_ETH, MAX_AMOUNT_TO_SEND_ETH), 8)
    amount_to_send_wei = web3.to_wei(random_amount_eth, "ether")

    gas_price = web3.eth.gas_price
    gas_limit = 21000
    gas_fee = gas_price * gas_limit

    if balance < amount_to_send_wei + gas_fee:
        print(f"❌ Недостаточно средств для отправки {random_amount_eth} ETH с учётом комиссии.")
        return

    receiver_address = Web3.to_checksum_address(receiver_address)
    tx = {
        "from": sender_address,
        "to": receiver_address,
        "value": amount_to_send_wei,
        "gas": gas_limit,
        "gasPrice": gas_price,
        "nonce": web3.eth.get_transaction_count(sender_address),
        "chainId": 1,
    }

    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"✅ Отправлено {random_amount_eth} ETH | Hash: {web3.to_hex(tx_hash)}")
    except Exception as e:
        print(f"❌ Ошибка при отправке: {e}")

# Обход по кошелькам и отправка
def send_eth_to_wallets(wallets):
    print("\n--- Запуск передачи ETH (Mainnet) ---\n")
    for private_key, receiver_address in wallets:
        print(f"➡️ Отправка с {private_key[:10]}... на {receiver_address}")
        send_eth(private_key, receiver_address)
        delay = random.randint(MIN_DELAY, MAX_DELAY)
        print(f"⏳ Ожидание {delay} секунд...")
        time.sleep(delay)
    print("\n✅ Передача ETH завершена.\n")

# Главное меню
def main_menu():
    wallets = load_wallets("wallets.txt")
    while True:
        print("\n--- Главное меню ---")
        print("1. Проверить баланс кошельков (Mainnet)")
        print("2. Запустить передачу ETH")
        print("3. Выйти")
        
        choice = input("\nВведите номер действия: ")

        if choice == "1":
            check_balances(wallets)
        elif choice == "2":
            send_eth_to_wallets(wallets)
        elif choice == "3":
            print("👋 Выход из программы.")
            break
        else:
            print("❗ Неверный выбор. Попробуйте снова.")

# Старт
if __name__ == "__main__":
    main_menu()
