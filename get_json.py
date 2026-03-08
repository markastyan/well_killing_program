import json
from utility import to_float


def load_json_as_tuple(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)

    data_dict = {}
    for item in data:
        number = item.get('number')
        data_dict[number] = item

    result_tuple = tuple(data_dict.items())
    return result_tuple

