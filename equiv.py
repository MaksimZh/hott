from core.univalence import *
from typing import Any

# 1 -----------------------------------

class Stack:
    def __init__(self):
        self._items = []
    def push(self, item):
        self._items.append(item)
    def pop(self):
        return self._items.pop()
    def to_list(self):
        return self._items.copy()

type List = list[Any]

def stack_to_list(x: Stack) -> List:
    return x.to_list()

def list_to_stack(x: List) -> Stack:
    s = Stack()
    for v in x:
        s.push(v)
    return s

stack_list_equivalence = create_type_equivalence(
    Stack, List, stack_to_list, list_to_stack)

s = Stack()
s.push(1)
s.push(2)
s.push(3)
l = stack_list_equivalence.function(s)
s1 = stack_list_equivalence.inverse.backward(l)
assert s1.pop() == 3
assert s1.pop() == 2
assert s1.pop() == 1

assert stack_list_equivalence.function(Stack()) == []
assert stack_list_equivalence.inverse.backward([]).to_list() == []


# 2 -----------------------------------

class Celsius:
    def __init__(self, value: float):
        self.value = value

class Fahrenheit:
    def __init__(self, value: float):
        self.value = value

def c2f(x: Celsius) -> Fahrenheit:
    return Fahrenheit(x.value * 9/5 + 32)

def f2c(x: Fahrenheit) -> Celsius:
    return Celsius((x.value - 32) * 5/9);

cf_equivalence = create_type_equivalence(
    Celsius, Fahrenheit, c2f, f2c)

x = Univalence.transport_uni_axi(Celsius, Fahrenheit, cf_equivalence, Celsius(0))
assert isinstance(x, Fahrenheit) and x.value == 32
x = Univalence.transport_uni_axi(Celsius, Fahrenheit, cf_equivalence, Celsius(100))
assert isinstance(x, Fahrenheit) and x.value == 212

x = cf_equivalence.inverse.backward(cf_equivalence.function(Celsius(0)))
assert isinstance(x, Celsius) and x.value == 0
x = cf_equivalence.function(cf_equivalence.inverse.backward(Fahrenheit(212)))
assert isinstance(x, Fahrenheit) and x.value == 212


# 3 -----------------------------------

class JSONData:
    def __init__(self, data: str):
        self.data = data

class XMLData:
    def __init__(self, data: str):
        self.data = data

class PythonDict:
    def __init__(self, data: dict):
        self.data = data


def json2dict(data: JSONData) -> PythonDict:
    return {"name": "John", "age": 30}

def dict2json(data: PythonDict) -> JSONData:
    return JSONData('{"name": "John", "age": 30}')

def dict2xml(data: PythonDict) -> XMLData:
    return XMLData('John30')

def xml2dict(data: XMLData) -> PythonDict:
    return {"name": "John", "age": 30}

json_dict_equiv = create_type_equivalence(
    JSONData, PythonDict, json2dict, dict2json)
dict_xml_equiv = create_type_equivalence(
    PythonDict, XMLData, dict2xml, xml2dict)

json_xml_equiv = json_dict_equiv.compose(dict_xml_equiv)

json_dict_path = Univalence.uni_axi(JSONData, PythonDict, json_dict_equiv)
dict_xml_path = Univalence.uni_axi(PythonDict, XMLData, dict_xml_equiv)
json_dict_xml_path = json_dict_path.trans(dict_xml_path)

json_xml_path = Univalence.uni_axi(JSONData, XMLData, json_xml_equiv)

x = JSONData('{"name": "John", "age": 30}')
y = Univalence.transport_uni_axi(JSONData, PythonDict, json_dict_equiv, x)
z = Univalence.transport_uni_axi(PythonDict, XMLData, dict_xml_equiv, y)
u = Univalence.transport_uni_axi(JSONData, XMLData, json_xml_equiv, x)

assert z.data == u.data
assert json_dict_xml_path == json_xml_path
