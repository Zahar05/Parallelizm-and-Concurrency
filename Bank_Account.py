# 2. Создайте класс BankAccount с полем balance, реализуйте
# методы deposit(amount: float) (пополнение) и withdraw
# (amount: float) (списание).
# Запустите несколько потоков, которые одновременно меняют
# баланс и добейтесь возникновения RaceCondition. Скопируйте
# код, в копии избавьтесь от RaceCondition одним из методов
# ограничения потоков.


import threading

# Класс без защиты RaceCondition
class BankAccount:
    def __init__(self):
        self.balance = 0

    def deposit(self, amount: float):
        self.balance += amount

    def withdraw(self, amount: float):
        self.balance -= amount

# Класс с защитой с помощью блокировки
class SafeBankAccount(BankAccount):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()

    def deposit(self, amount: float):
        with self.lock:
            self.balance += amount

    def withdraw(self, amount: float):
        with self.lock:
            self.balance -= amount

# Рабочая функция для потоков
def worker(account, amount, repetitions):
    for _ in range(repetitions):
        account.deposit(amount)
        account.withdraw(amount)

if __name__ == "__main__":
    print("=== Без защиты (Race Condition):")
    account = BankAccount()
    threads = []

    # Малое число операций для отображения RaceCondition
    for _ in range(10):
        t = threading.Thread(target=worker, args=(account, 10, 100))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Баланс после всех операций (без защиты): {account.balance}\n")

    print("=== С защитой (без Race Condition):")
    safe_account = SafeBankAccount()
    safe_threads = []

    for _ in range(10):
        t = threading.Thread(target=worker, args=(safe_account, 10, 100))
        safe_threads.append(t)
        t.start()

    for t in safe_threads:
        t.join()

    print(f"Баланс после всех операций (с защитой): {safe_account.balance}")