import pytest
import datetime
from pymodel.fields import IntegerField, StringField, BooleanField, DateTimeField

class DummyModel:
    age = IntegerField(nullable=True, default=18)
    name = StringField(max_length=50)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(nullable=True)

def test_set_valid_values():
    obj = DummyModel()
    obj.age = 25
    obj.name = "Alice"
    obj.is_active = False
    obj.created_at = datetime.datetime.now()

    assert obj.age == 25
    assert obj.name == "Alice"
    assert obj.is_active is False


def test_default_values():
    obj = DummyModel()

    assert obj.age == 18
    assert obj.is_active is True


def test_type_validation_raises_type_error():
    obj = DummyModel()

    with pytest.raises(TypeError) as exc_info:
        obj.age = "twenty"
    assert "expects an int" in str(exc_info.value)
    
    with pytest.raises(TypeError) as exc_info:
        obj.name = 123
    assert "expects a str" in str(exc_info.value)

def test_bool_not_accepted_as_int():
    obj = DummyModel()
    
    with pytest.raises(TypeError):
        obj.age = True

def test_string_max_length():
    obj = DummyModel()
    with pytest.raises(ValueError) as exc_info:
        obj.name = "A" * 51
    assert "exceeds max_length" in str(exc_info.value)

def test_nullable_and_delete():
    obj = DummyModel()
    obj.age = 30
    assert obj.age == 30

    del obj.age
    assert obj.age is None

    with pytest.raises(AttributeError) as exc_info:
        del obj.name
    assert "Cannot delete non-nullable field" in str(exc_info.value)

def test_set_none_on_non_nullable_without_default():
    obj = DummyModel()
    with pytest.raises(ValueError) as exc_info:
        obj.name = None
    assert "cannot be None" in str(exc_info.value)

def test_set_name_and_column_derivation():
    assert DummyModel.age.name == "age"
    assert DummyModel.age.column == "age"