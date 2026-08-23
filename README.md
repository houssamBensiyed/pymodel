<div align="center">

<pre>
██████╗ ██╗   ██╗███╗   ███╗ ██████╗ ██████╗ ███████╗██╗     
██╔══██╗╚██╗ ██╔╝████╗ ████║██╔═══██╗██╔══██╗██╔════╝██║     
██████╔╝ ╚████╔╝ ██╔████╔██║██║   ██║██║  ██║█████╗  ██║     
██╔═══╝   ╚██╔╝  ██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  ██║     
██║        ██║   ██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗███████╗
╚═╝        ╚═╝   ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝
</pre>

**A lightweight, declarative data modeling and field validation library for Python.**

[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Lint: Ruff](https://img.shields.io/badge/lint-ruff-261230?logo=ruff)
![Dependencies](https://img.shields.io/badge/dependencies-0-success)

</div>

---

## About

**PyModel** provides clean, descriptor-based fields to define data models in Python. It helps you validate types, manage default values, and enforce constraints with zero external dependencies.

---

## Features

- **Declarative Fields**: Define model attributes using clean field descriptors.
- **Type Validation**: Enforce strict types (int, str, bool, datetime) on assignment.
- **Nullability and Defaults**: Set default values and protect non-nullable fields.
- **Automatic Column Naming**: Field names are automatically converted to database-friendly column names.
- **Zero Dependencies**: Built entirely with the Python standard library.

---

## Installation

### Requirements

- Python **3.10+**

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/pymodel.git
cd pymodel

python -m venv .venv
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

pip install -e ".[dev]"
```

---

## Quick Start

Here is how to define and use fields on a class:

```python
import datetime
from pymodel import (
    IntegerField,
    StringField,
    BooleanField,
    DateTimeField,
)

class User:
    id = IntegerField(primary_key=True)
    name = StringField(max_length=50)
    age = IntegerField(nullable=True, default=18)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(nullable=True)

# Create an instance
user = User()

# Set valid values
user.id = 1
user.name = "Alice"
user.created_at = datetime.datetime.now()

print(user.name)       # Output: "Alice"
print(user.age)        # Output: 18 (default value)
print(user.is_active)  # Output: True (default value)
```

---

## Field Types and Options

### Available Field Classes

| Field Class | Expected Python Type | Key Options |
| :--- | :--- | :--- |
| `IntegerField` | `int` | `primary_key`, `unique`, `nullable`, `default`, `column` |
| `StringField` | `str` | `max_length`, `primary_key`, `unique`, `nullable`, `default`, `column` |
| `TextField` | `str` | `primary_key`, `unique`, `nullable`, `default`, `column` |
| `BooleanField` | `bool` | `nullable`, `default`, `column` |
| `DateTimeField` | `datetime.datetime` | `nullable`, `default`, `column` |

### Common Field Options

- `primary_key` (`bool`): Marks the field as a primary key. Default is `False`.
- `unique` (`bool`): Indicates if the field value must be unique. Default is `False`.
- `nullable` (`bool`): When `False`, setting `None` or deleting the field raises an error. Default is `False`.
- `default` (`Any`): The default value returned when no value is set. Default is `None`.
- `column` (`str`): Custom column name. If not provided, it is generated automatically from the field name.

---

## Examples

### Type Validation

PyModel raises a `TypeError` immediately if you assign the wrong type:

```python
user = User()

# Raises TypeError: Field 'age' expects an int, got str
user.age = "twenty"

# Booleans are not accepted as integers
# Raises TypeError: Field 'age' expects an int, got bool
user.age = True
```

### String Length Validation

`StringField` validates the length of the string:

```python
# Raises ValueError: Field 'name' exceeds max_length of 50
user.name = "A" * 51
```

### Deleting and Nullable Fields

Deleting a nullable field resets its value to `None`. Deleting a non-nullable field raises an `AttributeError`:

```python
user.age = 25
del user.age
print(user.age)  # Output: None

# Non-nullable field
# Raises AttributeError: Cannot delete non-nullable field 'name'
del user.name
```

### Column Name Derivation

Field names are automatically converted to column names:

```python
class Product:
    productId = IntegerField()      # column name -> 'product_id'
    unitPrice = IntegerField()      # column name -> 'unit_price'

print(Product.productId.column)     # Output: "product_id"
```

---

## Testing

Run the test suite with `pytest`:

```bash
python -m pytest
```

---

## License

Distributed under the **MIT License**. See [LICENSE](./LICENSE) for details.
