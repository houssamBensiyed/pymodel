import re
from .fields import Field

class ModelMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        is_base_model = namespace.get('__module__') == __name__ and name == "Model"

        fields = {}
        for base in bases:
            if hasattr(base, '_fields'):
                fields.update(base._fields)

        primary_keys = []
        for key, value in list(namespace.items()):
            if isinstance(value, Field):
                fields[key] = value
                if value.primary_key: 
                    primary_keys.append(key) # to check how it works in tests

        namespace['_fields'] = fields
