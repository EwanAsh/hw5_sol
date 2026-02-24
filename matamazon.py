# TODO add all imports needed here
import json
import argparse
import sys


class InvalidIdException(Exception):
    pass


class InvalidPriceException(Exception):
    pass


class Customer:
    # TODO implement this class as instructed
    def __init__(self, id: int, name: str, city: str, address: str):
        if not isinstance(id, int) or id <= 0:
            raise InvalidIdException('Invalid customer id.')
        self.id = id
        self.name = name
        self.city = city
        self.address = address

    def __repr__(self):
        return (f"Customer(id={self.id}, "
                f"name='{self.name}', "
                f"city='{self.city}', "
                f"address='{self.address}')")


class Supplier:
    # TODO implement this class as instructed
    def __init__(self, id: int, name: str, city: str, address: str):
        if not isinstance(id, int) or id <= 0:
            raise InvalidIdException('Invalid supplier id.')
        self.id = id
        self.name = name
        self.city = city
        self.address = address

    def __repr__(self):
        return (f"Supplier(id={self.id}, "
                f"name='{self.name}', "
                f"city='{self.city}', "
                f"address='{self.address}')")


class Product:
    # TODO implement this class as instructed
    def __init__(self, id: int, name: str, price: float, supplier_id: int, quantity: int):
        if not isinstance(id, int) or id <= 0:
            raise InvalidIdException("Product id must be a positive integer")

        if not isinstance(supplier_id, int) or supplier_id <= 0:
            raise InvalidIdException("Supplier id must be a positive integer")

        if not isinstance(quantity, int) or quantity <= 0:
            raise InvalidIdException("Quantity must be a positive integer")

        if not isinstance(price, (int, float)) or price <= 0:
            raise InvalidPriceException("Price must be positive")

        self.id = id
        self.name = name
        self.price = price
        self.supplier_id = supplier_id
        self.quantity = quantity

    def __repr__(self):
        return (f"Product(id={self.id}, "
                f"name='{self.name}', "
                f"price={self.price}, "
                f"supplier_id={self.supplier_id}, "
                f"quantity={self.quantity})")

    def __lt__(self, other):
        return self.price < other.price


class Order:
    # TODO implement this class as instructed
    def __init__(self, id: int, customer_id: int, product_id: int, quantity: int, total_price: float):
        # validate ids + quantity
        if not isinstance(id, int) or id <= 0:
            raise InvalidIdException("Order id must be a positive integer")

        if not isinstance(customer_id, int) or customer_id <= 0:
            raise InvalidIdException("Customer id must be a positive integer")

        if not isinstance(product_id, int) or product_id <= 0:
            raise InvalidIdException("Product id must be a positive integer")

        if not isinstance(quantity, int) or quantity <= 0:
            raise InvalidIdException("Quantity must be a positive integer")

        # validate price
        if not isinstance(total_price, (int, float)) or total_price <= 0:
            raise InvalidPriceException("Total price must be positive")

        self.id = id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity
        self.total_price = total_price

    def __repr__(self):
        return (f"Order(id={self.id}, "
                f"customer_id={self.customer_id}, "
                f"product_id={self.product_id}, "
                f"quantity={self.quantity}, "
                f"total_price={self.total_price})")


class MatamazonSystem:
    def __init__(self):
        # TODO implement this method if needed
        self.customers = {}
        self.suppliers = {}
        self.products = {}
        self.orders = {}
        self.next_order_id = 1

    def register_entity(self, entity, is_customer):
        # TODO implement this method as instructed
        entity_dict = self.customers if is_customer else self.suppliers
        entity_type = "Customer" if is_customer else "Supplier"

        existing = entity_dict.get(entity.id)

        if existing and repr(existing) != repr(entity):
            raise InvalidIdException(f"{entity_type} with this is already exists")

        if not existing:
            entity_dict[entity.id] = entity

    def add_or_update_product(self, product):
        # TODO implement this method as instructed
        existing = self.products.get(product.id)

        if existing and existing.supplier_id != product.supplier_id:
            raise InvalidIdException("Product belongs to a different supplier")

        self.products[product.id] = product

    def place_order(self, customer_id, product_id, quantity=1):
        # TODO implement this method as instructed
        if customer_id not in self.customers:
            raise InvalidIdException("Customer does not exist")

        product = self.products.get(product_id)
        if not product:
            return "The product does not exist in the system"

        if quantity > product.quantity:
            return "The quantity requested for this product is greater than the quantity in stock"

        product.quantity -= quantity

        order_id = self.next_order_id
        self.next_order_id += 1
        total_price = product.price * quantity
        order = Order(order_id, customer_id, product_id, quantity, total_price)

        self.orders[order_id] = order

        return "The order has been accepted in the system"

    def remove_object(self, _id, class_type):
        # TODO implement this method as instructed
        if not isinstance(_id, int) or _id <= 0:
            raise InvalidIdException("Invalid id")

        if class_type is Customer:
            if _id not in self.customers:
                raise InvalidIdException("Customer does not exist")
            if any(o.customer_id == _id for o in self.orders.values()):
                raise InvalidIdException("Customer is referenced by an existing order")
            del self.customers[_id]
            return

        if class_type is Product:
            if _id not in self.products:
                raise InvalidIdException("Product does not exist")
            if any(o.product_id == _id for o in self.orders.values()):
                raise InvalidIdException("Product is referenced by an existing order")
            del self.products[_id]
            return

        if class_type is Supplier:
            if _id not in self.suppliers:
                raise InvalidIdException("Supplier does not exist")
            for o in self.orders.values():
                p = self.products.get(o.product_id)
                if p and p.supplier_id == _id:
                    raise InvalidIdException("Supplier is referenced by an existing order")
            del self.suppliers[_id]
            return

        if class_type is Order:
            if _id not in self.orders:
                raise InvalidIdException("Order does not exist")
            order = self.orders[_id]
            product = self.products.get(order.product_id)
            if product:
                product.quantity += order.quantity
            del self.orders[_id]
            return

    def search_products(self, query, max_price=None):
        # TODO implement this method as instructed
        matches = []

        for p in self.products.values():
            if p.quantity == 0:
                continue
            if query not in p.name:
                continue
            if max_price is not None and p.price > max_price:
                continue
            matches.append(p)

        return sorted(matches)

    def export_system_to_file(self, path):
        # TODO implement this method as instructed
        try:
            with open(path, "w", encoding="utf-8") as f:
                for c in self.customers.values():
                    print(c, file=f)
                for s in self.suppliers.values():
                    print(s, file=f)
                for p in self.products.values():
                    print(p, file=f)
        except OSError:
            raise

    def export_orders(self, out_file):
        # TODO implement this method as instructed
        data = {}

        try:
            for o in self.orders.values():
                product = self.products.get(o.product_id)
                if product is None:
                    raise InvalidIdException("Order references a non-existing product")

                supplier = self.suppliers.get(product.supplier_id)
                if supplier is None:
                    raise InvalidIdException("Order references a non-existing supplier")

                origin = supplier.city

                data.setdefault(origin, []).append(repr(o))

            json.dump(data, out_file)

        except Exception:
            raise

def load_system_from_file(path):
    # TODO implement this function as instructed
    system = MatamazonSystem()

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                obj = eval(line)

                if isinstance(obj, Customer):
                    system.register_entity(obj, is_customer=True)

                elif isinstance(obj, Supplier):
                    system.register_entity(obj, is_customer=False)

                elif isinstance(obj, Product):
                    system.add_or_update_product(obj)

    except Exception:
        raise

    return system

# TODO all the main part here
USAGE_LINE = "Usage: python3 matamazon.py -l < matamazon_log > -s < matamazon_system > -o <output_file> -os <out_matamazon_system>"


def _u2s(token: str) -> str:
    return token.replace("_", " ")


def _class_from_token(tok: str):
    tok = tok.lower()
    if tok == "customer":
        return Customer
    if tok == "supplier":
        return Supplier
    if tok == "product":
        return Product
    if tok == "order":
        return Order
    raise InvalidIdException("Invalid class_type")


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-l", dest="log_path")
    parser.add_argument("-s", dest="system_path", default=None)
    parser.add_argument("-o", dest="out_file_path")
    parser.add_argument("-os", dest="out_system_path")

    args = parser.parse_args()

    if not args.log_path:
        print(USAGE_LINE)
        sys.exit(1)

    try:
        if args.system_path is not None:
            system = load_system_from_file(args.system_path)
        else:
            system = MatamazonSystem()

        with open(args.log_path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue

                parts = line.split()
                cmd = parts[0].lower()

                if cmd == "register":
                    if len(parts) != 6:
                        raise ValueError
                    kind = parts[1].lower()
                    _id = int(parts[2])
                    name = _u2s(parts[3])
                    city = _u2s(parts[4])
                    address = _u2s(parts[5])

                    if kind == "customer":
                        system.register_entity(Customer(_id, name, city, address), True)
                    else:
                        system.register_entity(Supplier(_id, name, city, address), False)

                elif cmd in ("add", "update"):
                    if len(parts) != 6:
                        raise ValueError
                    pid = int(parts[1])
                    name = _u2s(parts[2])
                    price = float(parts[3])
                    supplier_id = int(parts[4])
                    quantity = int(parts[5])
                    system.add_or_update_product(Product(pid, name, price, supplier_id, quantity))

                elif cmd == "order":
                    if len(parts) not in (3, 4):
                        raise ValueError("bad order command length")
                    customer_id = int(parts[1])
                    product_id = int(parts[2])
                    qty = int(parts[3]) if len(parts) == 4 else 1
                    system.place_order(customer_id, product_id, qty)

                elif cmd == "remove":
                    if len(parts) != 3:
                        raise ValueError
                    class_tok = parts[1]
                    _id = int(parts[2])
                    cls = _class_from_token(class_tok)
                    system.remove_object(_id, cls)

                elif cmd == "search":
                    if len(parts) not in (2, 3):
                        raise ValueError("bad search command length")
                    query = _u2s(parts[1])
                    max_price = float(parts[2]) if len(parts) == 3 else None
                    res = system.search_products(query, max_price)
                    print(res)

                else:
                    raise ValueError("Unknown command")

        if args.out_file_path:
            with open(args.out_file_path, "w", encoding="utf-8") as out_f:
                system.export_orders(out_f)

        if args.out_system_path:
            system.export_system_to_file(args.out_system_path)

    except Exception:
        print("The matamazon script has encountered an error")
        sys.exit(1)


if __name__ == "__main__":
    main()