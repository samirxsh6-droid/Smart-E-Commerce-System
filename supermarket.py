from abc import ABC, abstractmethod

# Requirement 1 & 3: The Blueprint & Data Protection
class Product(ABC):
    def __init__(self, product_id, name, price, stock):
        self.id = product_id
        self.name = name
        # Using setters for data protection
        self.price = price  
        self.stock = stock  

    # Data Protection (Encapsulation) for Price
    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Error: Price cannot be negative.")
        self.__price = value

    # Data Protection (Encapsulation) for Stock
    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, value):
        if value < 0:
            raise ValueError("Error: Stock cannot be less than zero.")
        self.__stock = value

    # Abstract methods (Forces child classes to implement them)
    @abstractmethod
    def apply_discount(self):
        pass

    @abstractmethod
    def display_info(self):
        pass

# Requirement 2: Specialization (Inheritance)
# Type A: Physical Product
class PhysicalProduct(Product):
    def __init__(self, product_id, name, price, stock, shipping_weight):
        super().__init__(product_id, name, price, stock)
        self.shipping_weight = shipping_weight

    def apply_discount(self):
        # 10% discount, but adds a $5 shipping fee per kg
        discounted_price = self.price * 0.90
        shipping_cost = self.shipping_weight * 5.0
        return discounted_price + shipping_cost

    def display_info(self):
        return f"[ Physical Product] {self.name} | Price: ${self.price:.2f} | Weight: {self.shipping_weight}kg"


# Type B: Digital Product
class DigitalProduct(Product):
    def __init__(self, product_id, name, price, stock, download_link):
        super().__init__(product_id, name, price, stock)
        self.download_link = download_link

    def apply_discount(self):
        # 20% flat discount, no shipping fees
        return self.price * 0.80

    def display_info(self):
        return f"[ Digital Product] {self.name} | Price: ${self.price:.2f} | Download Link: {self.download_link}"


# Requirement 4: Smart Behavior (Polymorphism)
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_product(self, product):
        if product.stock > 0:
            self.items.append(product)
            product.stock -= 1
            print(f" Successfully added '{product.name}' to your cart.")
        else:
            print(f"Sorry, '{product.name}' is currently out of stock.")

    def view_cart(self):
        if not self.items:
            print("Your shopping cart is empty.")
            return

        print("\n--- Cart Contents ---")
        for i, item in enumerate(self.items, 1):
            print(f"{i}. {item.display_info()}")
        print("------------------------")

    def checkout(self):
        if not self.items:
            print(" Cart is empty. Cannot proceed to checkout.")
            return

        total = 0.0
        print("\n Final Invoice:")
        for item in self.items:
            # Polymorphism: Same function name, different behavior per object
            final_price = item.apply_discount()
            total += final_price
            print(f"- {item.name}: Price after discount (& shipping if applicable) = ${final_price:.2f}")
        
        print("-" * 30)
        print(f" Grand Total: ${total:.2f}")
        self.items.clear()
        print(" Payment successful! Thank you for shopping with us.")

# Requirement 5: Terminal Interaction

def main():
    # Initialize store inventory
    # Initialize store inventory
    inventory = [
        PhysicalProduct(product_id=1, name="Gaming Laptop", price=1000.0, stock=5, shipping_weight=2.5),
        PhysicalProduct(product_id=2, name="Printed Book", price=20.0, stock=50, shipping_weight=0.5),
        DigitalProduct(product_id=3, name="Python Course", price=100.0, stock=999, download_link="link.com/python"),
        DigitalProduct(product_id=4, name="Digital Game", price=60.0, stock=999, download_link="link.com/game")
    ]

    cart = ShoppingCart()

    while True:
        print("\n" + "="*30)
        print(" Welcome to Our Smart Store")
        print("="*30)
        print("[1] View Available Products")
        print("[2] Add Product to Cart")
        print("[3] View Cart Contents")
        print("[4] Checkout")
        print("[5] Exit")

        choice = input("👉 Please choose an option (1-5): ")

        try:
            choice = int(choice)
        except ValueError:
            print(" Error: Invalid input. Please enter a number between 1 and 5.")
            continue

        if choice == 1:
            print("\n--- Product List ---")
            for idx, prod in enumerate(inventory):
                print(f"ID: {prod.id} | {prod.display_info()} | Stock: {prod.stock}")

        elif choice == 2:
            prod_id_input = input(" Enter the ID of the product you want to add: ")
            try:
                prod_id = int(prod_id_input)
                # Find product by ID
                selected_product = next((p for p in inventory if p.id == prod_id), None)
                
                if selected_product:
                    cart.add_product(selected_product)
                else:
                    print("Error: Product ID not found.")
            except ValueError:
                print("Error: Product ID must be a number.")

        elif choice == 3:
            cart.view_cart()

        elif choice == 4:
            cart.checkout()

        elif choice == 5:
            print("Goodbye! Hope to see you again soon.")
            break

        else:
            print("051Error: Invalid choice. Please choose from 1 to 5.")

if __name__ == "__main__":
    main()