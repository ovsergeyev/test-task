import argparse
from dataclasses import dataclass, fields, asdict
from typing import List, Dict, Union, Optional

CSV_DELIMITER = ","


@dataclass
class Employee:
    department: str
    name: str
    hours: str
    rate: str
    payout: str

    aliases = {"hours_worked": "hours", "hourly_rate": "rate", "salary": "rate"}


def get_indices(header: List[str], dataclass_type):
    result = {}
    csv_indices = {key: idx for idx, key in enumerate(header)}
    dataclass_keys = [f.name for f in fields(dataclass_type)]
    csv_keys = csv_indices.keys()
    aliases = getattr(dataclass_type, "aliases", {})
    for key in csv_keys:
        if key in dataclass_keys:
            result[key] = csv_indices[key]
        elif key in aliases.keys():
            result[aliases[key]] = csv_indices[key]
    return result


def get_row_dict(row, indices, dataclass_type):
    result = {}
    dataclass_keys = [f.name for f in fields(dataclass_type)]
    for key in dataclass_keys:
        if key in indices.keys():
            result[key] = row[indices[key]]
        else:
            result[key] = None
    return result


def get_max_fields_length(items: List[Union[Employee]], gap: int = 0) -> Dict[str, int]:
    result = {}
    for field in fields(items[0]):
        field_name = field.name
        max_len = max(len(str(getattr(item, field_name))) for item in items)
        max_len = max(max_len, len(field_name)) + gap
        result[field_name] = max_len

    return result


def get_header(
    keys: List[str],
    max_fields_length: Dict[str, int],
    group_field_name: Optional[str] = None,
) -> str:
    header_parts = []
    for key in keys:
        if key == group_field_name:
            header_parts.append(f"{' ' * max_fields_length[key]}")
        else:
            header_parts.append(f"{key:<{max_fields_length[key]}}")
    header = " ".join(header_parts)
    return header


def get_row(
    item: Dict,
    max_fields_length: Dict[str, int],
    group_field_name: Optional[str] = None,
) -> str:
    row_parts = []
    for key in item.keys():
        if key == group_field_name:
            row_parts.append(f"{'-' * max_fields_length[key]}")
        else:
            row_parts.append(f"{item[key]:<{max_fields_length[key]}}")
    row = " ".join(row_parts)
    return row


def get_employees(files: List[str]) -> List[Employee]:
    employees: List[Employee] = []
    for file_path in files:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            lines = file.readlines()
            header = lines[0].strip().split(CSV_DELIMITER)
            indices = get_indices(header, Employee)

            for line in lines[1:]:
                if not line.strip():
                    continue  # пропуск пыстых строк
                row = line.strip().split(CSV_DELIMITER)
                try:
                    employee = Employee(**get_row_dict(row, indices, Employee))
                    employees.append(employee)
                except Exception as e:
                    print(f"Ошибка при обработке строки {line}: {e}")
                    continue

    for employee in employees:
        employee.payout = f"${int(employee.hours) * int(employee.rate)}"

    return employees


def print_payout_report(employees: List[Employee]):
    max_fields_length = get_max_fields_length(employees, 5)
    keys = max_fields_length.keys()

    group_dict = {}
    for employee in employees:
        key = getattr(employee, "department")
        if key in group_dict.keys():
            group_dict[key].append(employee)
        else:
            group_dict[key] = [employee]

    header = get_header(list(keys), max_fields_length, "department")
    print(header)

    for group_key, group_items in group_dict.items():
        print(group_key)
        for group_item in group_items:
            row = get_row(asdict(group_item), max_fields_length, "department")
            print(row)
        hours = sum(int(item.hours) for item in group_items)
        payout = sum(int(item.hours) * int(item.rate) for item in group_items)
        end_row_dict = {
            "department": "",
            "name": "",
            "hours": hours,
            "rate": "",
            "payout": f"${payout}",
        }
        row = get_row(end_row_dict, max_fields_length)
        print(row)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_files", nargs="+", help="Список входных CSV файлов")
    parser.add_argument("--report", required=True, help="Тип отчета")

    args = parser.parse_args()

    if args.report == "payout":
        employees = get_employees(files=args.input_files)
        print_payout_report(employees)


if __name__ == "__main__":
    main()
