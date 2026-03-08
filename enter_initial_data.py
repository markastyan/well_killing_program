"""
Модуль содержит функции для получения исходных данных.
"""

__all__ = ['enter_initial_data_manual', 'enter_initial_data_from_file', 'enter_initial_data_manual_multiple_pipes', 'enter_initial_data_from_file_multiple_pipes']


def enter_initial_data_manual(
        inner_diameter: float = None,
        section_length: float = None,
        interval_diameter: float = None,
        outer_diameter: float = None,
        interval_length: float = None,
        current_depth: float = None,
        lowering_depth: float = None
) -> dict[str, float]:
    """
    Ввод исходных данных скважины вручную.

    :param inner_diameter: Внутренний диаметр одноразмерного типа труб [м]
    :param section_length: Длина секции одноразмерного типа труб [м]
    :param interval_diameter: Диаметр интервала (в случае открытого ствола - диаметр долота; в случае обсаженного ствола – внутренний диаметр обсадной колонны) [м]
    :param outer_diameter: Наружный диаметр одноразмерного бурильного инструмента [м]
    :param interval_length: Длина интервала [м]
    :param current_depth: Глубина текущего забоя [м]
    :param lowering_depth: Глубина спуска инструмента [м]
    :return: Значения исходных данных в виде словаря
    """
    return {'inner_diameter': inner_diameter,
            'section_length': section_length,
            'interval_diameter': interval_diameter,
            'outer_diameter': outer_diameter,
            'interval_length': interval_length,
            'current_depth': current_depth,
            'lowering_depth': lowering_depth}


def enter_initial_data_from_file(file_path: str) -> dict[str, float]:
    """
    Ввод исходных данных скважины из текстового файла.

    :param file_path: Путь к текстовому файлу с данными
    :return: Значения исходных данных в виде словаря
    """
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, value = line.strip().split(': ')
            data[name] = float(value)
    return data


def enter_initial_data_from_file_multiple_pipes(file_path: str) -> dict[str, float]:
    """
    Ввод исходных данных скважины из текстового файла.

    :param file_path: Путь к текстовому файлу с данными
    :return: Значения исходных данных в виде словаря
    """
    data = {}
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if i == 0:
                *_, current_depth, lowering_depth = line.strip().split(' ')
                data['current_depth'] = float(current_depth)
                data['lowering_depth'] = float(lowering_depth)
                data['outer_pipe_values'] = []
                data['inner_pipe_values'] = []
            else:
                if len(line.strip().split(" ")) == 3:
                    data['inner_pipe_values'].append([float(x) for x in line.strip().split(" ")])
                if len(line.strip().split(" ")) == 2:
                    data['outer_pipe_values'].append([float(x) for x in line.strip().split(" ")])
    return data


def enter_initial_data_manual_multiple_pipes(
        outer_pipe_values: list = None,
        inner_pipe_values: list = None,
        current_depth: float = None,
        lowering_depth: float = None,
) -> dict[str, float | list]:
    """
    Ввод исходных данных скважины вручную.

    :param outer_pipe_values: Значения внешних элементов труб
    :param inner_pipe_values: Значения внутренних элементов труб
    :param current_depth: Глубина текущего забоя [м]
    :param lowering_depth: Глубина спуска инструмента [м]
    :return: Значения исходных данных в виде словаря
    """
    return {'current_depth': current_depth,
            'lowering_depth': lowering_depth,
            'outer_pipe_values': outer_pipe_values,
            'inner_pipe_values': inner_pipe_values
            }


def enter_initial_data_from_program(*args, **kwargs) -> tuple:
    """
    Ввод исходных данных скважины из программы.

    :return: Значения исходных данных в виде словаря
    """
    raise NotImplementedError("Функция ещё не реализована.")