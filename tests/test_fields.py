import pytest
import datetime
from pymodel.fields import IntegerField, StringField, BooleanField, DateTimeField

class DummyModel:
    age = IntegerField(nullable=True, default=18)
    name = StringField(max_length=50)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(nullable=True)

