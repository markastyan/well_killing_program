"""
Модуль содержит функции для выбора метода глушения.
"""

__all__ = ['choose_method']


def choose_method(
        lowering_depth: float = None,
        max_height: float = 50.0,
        current_depth: float = None,
        formation_loss_pressure: float = None,
        drilling_mud_density: float = None,
        fluid_density: float = None, *,
        is_manual: bool = False,
        manual_type: str = "Базовый"
) -> str:
    """
    Выбор метода глушения скважины.

    :param lowering_depth: Глубина спуска инструмента [м]
    :param max_height: Псевдопараметр максимальной высоты подъёма инструмента над забоем [м]
    :param current_depth: Глубина текущего забоя [м]
    :param formation_loss_pressure: Давление начала поглощения слабого пласта [Па]
    :param drilling_mud_density: Плотность бурового раствора в скважине [кг/м3]
    :param fluid_density: Плотность флюида в скважине [кг/м3]
    :param is_manual: Если параметр задан True, тип задаётся вручную
    :param manual_type: Метод, который выбирается вручную (Базовый/Бурильщика)
    :return: Значения входных данных в виде словаря
    """

    if not is_manual:
        return manual_type

    is_lowering_possible = False
    is_there_intake = False
    is_gravitational_displacement_possible = False

    if lowering_depth + max_height >= current_depth:
        is_lowering_possible = True
    if formation_loss_pressure is not None:
        is_there_intake = True
    if drilling_mud_density > fluid_density:
        is_gravitational_displacement_possible = True

    if is_lowering_possible and is_there_intake:
        return "Базовый"
