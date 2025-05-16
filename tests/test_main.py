import pytest
from src.main import Employee
from src.main import (
    get_indices,
    get_row_dict,
    get_max_fields_length,
    get_header,
    get_row,
)


@pytest.fixture
def employees():
    employees = [
        Employee(
            department="Marketing",
            name="Alice Johnson",
            hours="160",
            rate="50",
            payout="$8000",
        ),
        Employee(
            department="HR",
            name="Grace Lee",
            hours="160",
            rate="45",
            payout="$7200",
        ),
        Employee(
            department="Sales",
            name="Mia Young",
            hours="160",
            rate="37",
            payout="$5920",
        ),
    ]
    return employees


@pytest.mark.parametrize(
    "header, dataclass_type, res",
    [
        (
            ["id", "email", "name", "department", "hours_worked", "hourly_rate"],
            Employee,
            {"name": 2, "department": 3, "hours": 4, "rate": 5},
        ),
        (
            ["department", "id", "email", "name", "hours_worked", "rate"],
            Employee,
            {"department": 0, "name": 3, "hours": 4, "rate": 5},
        ),
    ],
)
def test_get_indices(header, dataclass_type, res):
    assert get_indices(header, dataclass_type) == res


@pytest.mark.parametrize(
    "row, indices, dataclass_type, res",
    [
        (
            ["1", "alice@example.com", "Alice Johnson", "Marketing", "160", "50"],
            {"name": 2, "department": 3, "hours": 4, "rate": 5},
            Employee,
            {
                "department": "Marketing",
                "name": "Alice Johnson",
                "hours": "160",
                "rate": "50",
                "payout": None,
            },
        ),
        (
            ["HR", "101", "grace@example.com", "Grace Lee", "160", "45"],
            {"department": 0, "name": 3, "hours": 4, "rate": 5},
            Employee,
            {
                "department": "HR",
                "name": "Grace Lee",
                "hours": "160",
                "rate": "45",
                "payout": None,
            },
        ),
        (
            ["mia@example.com", "Mia Young", "Sales", "160", "37", "203"],
            {"name": 1, "department": 2, "hours": 3, "rate": 4},
            Employee,
            {
                "department": "Sales",
                "name": "Mia Young",
                "hours": "160",
                "rate": "37",
                "payout": None,
            },
        ),
    ],
)
def test_get_row_dict(row, indices, dataclass_type, res):
    assert get_row_dict(row, indices, dataclass_type) == res


@pytest.mark.parametrize(
    "gap, res",
    [
        (
            5,
            {"department": 15, "name": 18, "hours": 10, "rate": 9, "payout": 11},
        )
    ],
)
def test_get_max_fields_length(employees, gap, res):
    assert get_max_fields_length(employees, gap) == res


@pytest.mark.parametrize(
    "keys, max_fields_length, group_field_name, res",
    [
        (
            ["department", "name", "hours", "rate", "payout"],
            {"department": 15, "name": 19, "hours": 10, "rate": 9, "payout": 11},
            "department",
            "                name                hours      rate      payout     ",
        )
    ],
)
def test_get_header(keys, max_fields_length, group_field_name, res):
    assert get_header(keys, max_fields_length, group_field_name) == res


@pytest.mark.parametrize(
    "item, max_fields_length, group_field_name, res",
    [
        (
            {
                "department": "Marketing",
                "name": "Alice Johnson",
                "hours": "160",
                "rate": "50",
                "payout": "$8000",
            },
            {"department": 15, "name": 19, "hours": 10, "rate": 9, "payout": 11},
            "department",
            "--------------- Alice Johnson       160        50        $8000      ",
        )
    ],
)
def test_get_row(item, max_fields_length, group_field_name, res):
    assert get_row(item, max_fields_length, group_field_name) == res
