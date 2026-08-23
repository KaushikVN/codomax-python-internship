"""
Codomax Python Internship - Module 3: Object-Oriented Python
Project: Python Banking System
Concepts: Classes, Objects, Constructors, Encapsulation, Abstraction,
          Inheritance, Polymorphism, and Transaction Logging.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import json
import os

DATA_FILE = "bank_accounts.json"


# 1. Abstraction: Abstract Base Class
class Account(ABC):
    def __init__(self, account_number: str, holder_name: str, initial_balance: float = 0.0):
        self._account_number = account_number          # Protected attribute
        self._holder_name = holder_name                # Protected attribute
        self.__balance = float(initial_balance)        # Private attribute (Encapsulation)
        self._transactions = []
        self._record_transaction("Account Created", initial_balance)

    # Getters / Setters (Encapsulation)
    @property
    def account_number(self):
        return self._account_number

    @property
    def holder_name(self):
        return self._holder_name

    @property
    def balance(self):
        return self.__balance

    def _set_balance(self, amount: float):
        self.__balance = amount

    def _record_transaction(self, transaction_type: str, amount: float):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "timestamp": timestamp,
            "type": transaction_type,
            "amount": amount,
            "resulting_balance": self.__balance
        }
        self._transactions.append(record)

    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            print("❌ Deposit amount must be greater than 0.")
            return False
        self.__balance += amount
        self._record_transaction("Deposit", amount)
        print(f"✅ Deposited ₹{amount:.2f}. New Balance: ₹{self.__balance:.2f}")
        return True

    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        """Abstract method enforced across subclasses."""
        pass

    def display_statement(self):
        print(f"\n--- Statement for Account: {self._account_number} ({self._holder_name}) ---")
        print(f"{'Date & Time':<22} {'Transaction':<15} {'Amount':<12} {'Balance':<12}")
        print("-" * 65)
        for t in self._transactions:
            print(f"{t['timestamp']:<22} {t['type']:<15} ₹{t['amount']:<11.2f} ₹{t['resulting_balance']:<11.2f}")
        print(f"Current Available Balance: ₹{self.__balance:.2f}\n")

    def to_dict(self):
        return {
            "account_number": self._account_number,
            "holder_name": self._holder_name,
            "balance": self.__balance,
            "account_type": self.__class__.__name__,
            "transactions": self._transactions
        }


# 2. Inheritance & Polymorphism: Savings Account
class SavingsAccount(Account):
    def __init__(self, account_number: str, holder_name: str, initial_balance: float = 1000.0, min_balance: float = 500.0):
        super().__init__(account_number, holder_name, initial_balance)
        self.min_balance = min_balance

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            print("❌ Withdrawal amount must be positive.")
            return False
        if self.balance - amount < self.min_balance:
            print(f"❌ Withdrawal denied. Minimum balance of ₹{self.min_balance:.2f} required.")
            return False
        self._set_balance(self.balance - amount)
        self._record_transaction("Withdrawal", amount)
        print(f"✅ Withdrawn ₹{amount:.2f}. Remaining Balance: ₹{self.balance:.2f}")
        return True


# 3. Inheritance & Polymorphism: Current (Checking) Account with Overdraft
class CurrentAccount(Account):
    def __init__(self, account_number: str, holder_name: str, initial_balance: float = 0.0, overdraft_limit: float = 5000.0):
        super().__init__(account_number, holder_name, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            print("❌ Withdrawal amount must be positive.")
            return False
        if self.balance - amount < -self.overdraft_limit:
            print(f"❌ Overdraft limit exceeded. Maximum overdraft limit is ₹{self.overdraft_limit:.2f}.")
            return False
        self._set_balance(self.balance - amount)
        self._record_transaction("Withdrawal (Overdraft Allowed)", amount)
        print(f"✅ Withdrawn ₹{amount:.2f}. Current Balance: ₹{self.balance:.2f}")
        return True


# 4. Bank Manager / Controller Class
class Bank:
    def __init__(self):
        self.accounts = {}
        self.load_data()

    def create_account(self, acc_type: str, acc_num: str, name: str, initial_deposit: float):
        if acc_num in self.accounts:
            print(f"❌ Account number '{acc_num}' already exists.")
            return

        if acc_type.lower() == "savings":
            acc = SavingsAccount(acc_num, name, initial_deposit)
        elif acc_type.lower() == "current":
            acc = CurrentAccount(acc_num, name, initial_deposit)
        else:
            print("❌ Invalid account type. Choose Savings or Current.")
            return

        self.accounts[acc_num] = acc
        self.save_data()
        print(f"🎉 {acc_type.capitalize()} account created successfully for {name}!")

    def get_account(self, acc_num: str) -> Account:
        return self.accounts.get(acc_num)

    def save_data(self):
        data = {acc_num: acc.to_dict() for acc_num, acc in self.accounts.items()}
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for acc_num, info in data.items():
                    if info["account_type"] == "SavingsAccount":
                        acc = SavingsAccount(info["account_number"], info["holder_name"], info["balance"])
                    else:
                        acc = CurrentAccount(info["account_number"], info["holder_name"], info["balance"])
                    acc._transactions = info.get("transactions", [])
                    self.accounts[acc_num] = acc
        except Exception:
            self.accounts = {}


def main():
    bank = Bank()

    while True:
        print("\n==========================================")
        print("🏦 PYTHON OOP BANKING SYSTEM")
        print("==========================================")
        print("1. Create New Account (Savings / Current)")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance & Statement")
        print("5. View All Accounts")
        print("6. Exit")
        print("==========================================")

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            acc_type = input("Enter Account Type (Savings / Current): ").strip()
            acc_num = input("Enter unique Account Number: ").strip()
            name = input("Enter Account Holder Name: ").strip()
            try:
                initial_deposit = float(input("Enter Initial Deposit: "))
                bank.create_account(acc_type, acc_num, name, initial_deposit)
            except ValueError:
                print("❌ Invalid deposit value.")

        elif choice in ["2", "3", "4"]:
            acc_num = input("Enter Account Number: ").strip()
            acc = bank.get_account(acc_num)
            if not acc:
                print(f"❌ Account '{acc_num}' not found.")
                continue

            if choice == "2":
                try:
                    amount = float(input("Enter amount to deposit: "))
                    if acc.deposit(amount):
                        bank.save_data()
                except ValueError:
                    print("❌ Invalid numeric amount.")

            elif choice == "3":
                try:
                    amount = float(input("Enter amount to withdraw: "))
                    if acc.withdraw(amount):
                        bank.save_data()
                except ValueError:
                    print("❌ Invalid numeric amount.")

            elif choice == "4":
                acc.display_statement()

        elif choice == "5":
            if not bank.accounts:
                print("No accounts exist.")
            else:
                print(f"\n{'Acc Number':<15} {'Holder Name':<20} {'Type':<15} {'Balance':<10}")
                print("-" * 65)
                for a in bank.accounts.values():
                    print(f"{a.account_number:<15} {a.holder_name:<20} {a.__class__.__name__:<15} ₹{a.balance:<10.2f}")

        elif choice == "6":
            print("👋 Thank you for banking with us!")
            break
        else:
            print("⚠️ Invalid choice. Select 1 to 6.")


if __name__ == "__main__":
    main()