from core.base_types import *

# 1
ref_index = Sum(42, "foo", is_left_active=True)
ref_key = Sum(42, "foo", is_left_active=False)

# 2
number_str = Sum("42", Sum(42, 42.0, is_left_active=True), is_left_active=True)
number_int = Sum("42", Sum(42, 42.0, is_left_active=True), is_left_active=False)
number_float = Sum("42", Sum(42, 42.0, is_left_active=False), is_left_active=False)

# 3
mapping = Product(
    Product("foo", 42),
    Product(
        Product("boo", 17),
        Product("bar", 100),
    )
)

# 4
position = Product(100, 200)
size = Product(50, 20)
rect = Product(position, size)
