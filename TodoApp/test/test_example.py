import pytest


def test_equal_or_not_equal():
    assert 3 != 2

def test_instance():
    assert isinstance("Hello", str)
    assert isinstance(10, int)

def test_boolean():
    is_boolean = True

    assert is_boolean is True
    assert ("Hello" == "World") is False

def test_lt_and_gt():
    assert 3 < 10
    assert 15 > 6

def test_list():
    num_list = [1, 2, 3, 4, 5]
    boolean_list = [False, False]

    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(boolean_list)


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, completed_year: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.completed_year = completed_year

@pytest.fixture
def default_person():
    return Student("Hari", "Raj", "Computer Science", 2015)

def test_person_initialisation(default_person):

    assert default_person.first_name == "Hari", "First name should be Hari"
    assert default_person.last_name == "Raj", "Last name should be Raj"
    assert default_person.major == "Computer Science"
    assert default_person.completed_year == 2015

