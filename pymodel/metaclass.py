import re
from .fields import Field


class ModelMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        is_base_model = namespace.get("__module__") == __name__ and name == "Model"

        fields = {}
        for base in bases:
            if hasattr(base, "_fields"):
                fields.update(base._fields)

        primary_keys = []
        for key, value in list(namespace.items()):
            if isinstance(value, Field):
                fields[key] = value
                if value.primary_key:
                    primary_keys.append(key)  # to check how it works in tests

        namespace["_fields"] = fields

        table_name = None
        if "Meta" in namespace and hasattr(namespace["Meta"], "table"):
            table_name = namespace["Meta"].table
        elif not is_base_model:
            s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
            snake_name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
            table_name = f"{snake_name}s"

        if table_name:
            namespace["_table"] = table_name

        cls = super().__new__(mcs, name, bases, namespace, **kwargs)

        is_abstract = namespace.get("Meta") and getattr(
            namespace["Meta"], "abstract", False
        )
        if not is_base_model and not is_abstract:
            if len(primary_keys) == 0:
                raise TypeError(f"Model '{name}' must define exactly one primary key")
            if len(primary_keys) > 1:
                raise TypeError(
                    f"Mode '{name}' has multiple primary keys: {primary_keys}"
                )

        return cls


class Model(metaclass=ModelMeta):
    """Base class for all ORM models."""

    pass
