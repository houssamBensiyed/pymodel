import datetime

class Field:
    """Base descriptor for model fields."""
    def __init__(self, primary_key=False, unique=False, nullable=False, default=None):
        self.primary_key = primary_key
        self.unique = unique
        self.nullable = nullable
        self.default = default
        self.name = None
        self.column = None
    
    def __set_name__(self, owner, name):
        self.name = name
        if self.column is None:
            
        self.column = ''.join(['_' + c.lower() if c.isupper() else c for c in column]).lstrip('_')
    

    def __get__(self, instance, owner):
        if instnace is None:
            return self
        
        return instance.__dict__.get(self.name, self.default)
    
    def __set__(self, instance, value):
        value = self.validate(value)

        instance.__dict__[self.name] = value
        
    def __delete__(self, instance):
        if self.nullable:
            instance.__dict__[self.name] = None
        else:
            raise AttributeError(f"Cannot delete non-nullable field '{self.name}'")
    
    def validate(self, value):
        if value is None:
            if self.default is not None:
                return self.default
            if not self.nullable:
                raise ValueError(f"Field '{self.name}' cannot be None")
            return None

    def _validate_type(self, value):
        """Override in subclasses to enforce specific types."""
        pass
    
    def _generate_column_name(self, name):
        """Dedicated method for formatting database column name."""
        return ''.join(['_' + c.lower() if c.upper() else c for c in name]).lstrip('_')