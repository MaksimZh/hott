# 1. N-мерный тор
Методы тора в основном понятны.
Сюрпризом стал аргумент `coherence_functions` в методе `rec`.
Если петли независимы, то он, казалось бы, не нужен, а если зависимы,
то будто бы не хватает функций для комбинаций 3-х и более петель.
То же самое касается и метода `ind`.

# 2. Пи-типы и Сигма-типы
```Python
# Test 6: Verified container (Sigma type ensuring a property)
def is_sorted(lst):
    if all(lst[i] <= lst[i+1] for i in range(len(lst)-1)):
        return bool
    return Unit
    
# This should succeed - the list is sorted
sorted_container = Sigma(
    domain=list,
    codomain=is_sorted,
    first=[1, 2, 3, 4],
    second=True
)

# This should succeed - the list isn't sorted and we claim this
unsorted_container = Sigma(
    domain=list,
    codomain=is_sorted,
    first=[3, 1, 4, 2],
    second=unit
)
    
# This should fail - the list isn't sorted but we claim it is
try:
    invalid_container = Sigma(
        domain=list,
        codomain=is_sorted,
        first=[3, 1, 4, 2],
        second=True
    )
except:
    pass
else:
    assert False
```
Конструкция кажется странной. Видимо я чего-то не понимаю в сигма типах.

```Python
# Test 7: Pi type for parametric functions
square_matrix_operations = Pi(
    domain=int,  # size
    codomain=lambda n: Callable,
    function=lambda n: {
        "identity": lambda: [[1 if i == j else 0 for j in range(n)] for i in range(n)],
        "zero": lambda: [[0 for _ in range(n)] for _ in range(n)],
        "ones": lambda: [[1 for _ in range(n)] for _ in range(n)]
    }
)
...
ones_3x3 = square_matrix_operations(3)["ones"]()
assert all(all(cell == 1 for cell in row) for row in ones_3x3)
assert len(ones_3x3) == 3
assert all(len(row) == 3 for row in ones_3x3)
```

```Python
# Test 10: Pi type for dynamic validation functions
validator_factory = Pi(
    domain=str,  # validation type
    codomain=lambda type_name: Callable[[Any], bool],
    function=lambda type_name: {
        "positive_int": lambda x: isinstance(x, int) and x > 0,
        "email": lambda x: isinstance(x, str) and "@" in x,
        "non_empty_list": lambda x: isinstance(x, list) and len(x) > 0
    }.get(type_name, lambda x: True)  # Default passes everything
)
...
list_validator = validator_factory("non_empty_list")
...
assert list_validator([1, 2]) is True
assert list_validator([]) is False
```

3. Посложнее
```Python
# Test 11: Pi-type for half value
half = Pi(
    domain=int,
    codomain=lambda n: int if n % 2 == 0 else float,
    function=lambda n: n // 2 if n % 2 == 0 else float(n / 2),
)

h2 = half(2)
h3 = half(3)
assert isinstance(h2, int)
assert int(h2*2) == 2
assert isinstance(h3, float)
assert int(h3*2) == 3
```

```Python
# Test 12: Combo
value_half_quarter = Pi(
    domain=int,
    codomain=lambda n: Sigma,
    function=lambda n: Sigma(
        domain=int,
        codomain=lambda n: Sigma,
        first=n,
        second=Sigma(
            domain=object,
            codomain=lambda h: object if isinstance(h, int) else Unit,
            first=half(n),
            second=half(half(n)) if isinstance(half(n), int) else unit
        )
    )
)

vhq6 = value_half_quarter(6)
assert vhq6.first == 6
assert isinstance(vhq6.second.first, int)
assert vhq6.second.first == 3
assert isinstance(vhq6.second.second, float)
assert int(vhq6.second.second*2) == 3

vhq5 = value_half_quarter(5)
assert vhq5.first == 5
assert isinstance(vhq5.second.first, float)
assert (vhq5.second.first*2) == 5
assert vhq5.second.second == unit
```
