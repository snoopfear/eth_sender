import time
import random
from web3 import Web3

# ✅ Настройки под Mainnet
RPC_URL = "https://ethereum-rpc.publicnode.com"  # Замените на свой рабочий RPC
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Проверка соединения
if not web3.is_connected():
    raise Exception("❌ Не удалось подключиться к RPC-узлу Ethereum Mainnet")

SEND_PERCENTAGE = 1  # Процент отправляемого ETH
MIN_DELAY = 5
MAX_DELAY = 10
BALANCE_CHECK_DELAY = 1

def load_wallets(file_path):
    wallets = []
    with open(file_path, "r") as file:
        for line in file:
            private_key, receiver_address = line.strip().split(":")
            if not private_key.startswith("0x"):
                private_key = "0x" + private_key
            wallets.append((private_key, receiver_address))
    return wallets

def check_balances(wallets):
    print("\n--- Проверка баланса кошельков (Mainnet) ---\n")
    for private_key, receiver_address in wallets:
        sender_address = web3.eth.account.from_key(private_key).address
        balance = web3.eth.get_balance(sender_address)
        eth_balance = web3.from_wei(balance, "ether")
        print(f"Адрес: {sender_address} | Баланс: {eth_balance:.6f} ETH")
        print(f"Ожидание {BALANCE_CHECK_DELAY} секунд...")
        time.sleep(BALANCE_CHECK_DELAY)
    print("\n✅ Проверка баланса завершена.\n")

def send_eth(private_key, receiver_address, percentage):
    account = web3.eth.account.from_key(private_key)
    sender_address = account.address
    balance = web3.eth.get_balance(sender_address)
    eth_balance = web3.from_wei(balance, "ether")
    print(f"Баланс {sender_address}: {eth_balance:.6f} ETH")

    amount_to_send = int(balance * (percentage / 100))
    if amount_to_send == 0:
        print(f"❌ Недостаточно средств для отправки с {sender_address}")
        return

    receiver_address = Web3.to_checksum_address(receiver_address)
    tx = {
        "from": sender_address,
        "to": receiver_address,
        "value": amount_to_send,
        "gas": 21000,
        "gasPrice": web3.eth.gas_price,
        "nonce": web3.eth.get_transaction_count(sender_address),
        "chainId": 1,  # ✅ Mainnet chain ID
    }

    signed_tx = web3.eth.account.sign_transaction(tx, private_key)

    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"✅ Транзакция отправлена! Hash: {web3.to_hex(tx_hash)}")
    except Exception as e:
        print(f"❌ Ошибка при отправке: {e}")

def send_eth_to_wallets(wallets, percentage):
    print("\n--- Запуск передачи ETH (Mainnet) ---\n")
    for private_key, receiver_address in wallets:
        print(f"➡️ Отправка с {private_key[:10]}... на {receiver_address}")
        send_eth(private_key, receiver_address, percentage)
        delay = random.randint(MIN_DELAY, MAX_DELAY)
        print(f"⏳ Ожидание {delay} секунд...")
        time.sleep(delay)
    print("\n✅ Передача ETH завершена.\n")

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
            send_eth_to_wallets(wallets, SEND_PERCENTAGE)
        elif choice == "3":
            print("👋 Выход из программы.")
            break
        else:
            print("❗ Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()
