"""
Модуль содержит функции для получения пользовательских данных.
"""

__all__ = ['enter_user_data_manual', 'enter_user_data_from_file']


def enter_user_data_manual(
        manifold_standpipe_pressure_drilling: float = None,
        pump_flow_rate_drilling: float = None,
        casing_pressure_test: float = None,
        formation_loss_pressure: float = None,
        weak_formation_fracture_pressure: float = None,
        drilling_mud_density: float = None,
        kill_fluid_viscosity: float = None,
        weak_formation_depth: float = None,
        standpipe_pressure_after_shut_in: float = None,
        wellhead_pressure_after_shut_in: float = None,
        additional_standpipe_pressure_during_injection: float = None,
        productive_zone_depth: float = None,
        fluid_influx_volume: float = None,
        lower_circulation_pressure: float = None,
        lower_consumption: float = None
) -> dict[str, float]:
    """
    Ввод входных данных скважины.

    :param manifold_standpipe_pressure_drilling: Давление на стояке манифольда при бурении (промывке) скважины [Па]
    :param pump_flow_rate_drilling: Подача насоса при бурении (промывке) скважины [м3/с]
    :param casing_pressure_test: Давление опрессовки обсадной колонны [Па]
    :param formation_loss_pressure: Давление начала поглощения слабого пласта [Па]
    :param weak_formation_fracture_pressure: Давление гидроразрыва слабого пласта [Па]
    :param drilling_mud_density: Плотность бурового раствора в скважине [кг/м3]
    :param kill_fluid_viscosity: Вязкость жидкости глушения [Па*с]
    :param weak_formation_depth: Глубина залегания слабого пласта [м]
    :param standpipe_pressure_after_shut_in: Избыточное давление в бурильных трубах (на стояке) после закрытия скважины и стабилизации давления [Па]
    :param wellhead_pressure_after_shut_in: Избыточное давление на устье скважины после её закрытия и стабилизации давления [Па]
    :param additional_standpipe_pressure_during_injection: Дополнительное избыточное давление на стояке при закачке [Па]
    :param productive_zone_depth: Глубина залегания продуктивного горизонта [м]
    :param fluid_influx_volume: Объем поступившего в скважину флюида (увеличение уровня промывочной жидкости в рабочей емкости) [м3]
    :param lower_circulation_pressure: Давление циркуляции при пониженной подаче насоса [Па]
    :param lower_consumption: Расход при пониженной подаче насоса [м3/c]
    :return: Значения входных данных в виде словаря
    """
    return {'manifold_standpipe_pressure_drilling': manifold_standpipe_pressure_drilling,
            'pump_flow_rate_drilling': pump_flow_rate_drilling,
            'casing_pressure_test': casing_pressure_test,
            'formation_loss_pressure': formation_loss_pressure,
            'weak_formation_fracture_pressure': weak_formation_fracture_pressure,
            'drilling_mud_density': drilling_mud_density,
            'kill_fluid_viscosity': kill_fluid_viscosity,
            'weak_formation_depth': weak_formation_depth,
            'standpipe_pressure_after_shut_in': standpipe_pressure_after_shut_in,
            'wellhead_pressure_after_shut_in': wellhead_pressure_after_shut_in,
            'additional_standpipe_pressure_during_injection': additional_standpipe_pressure_during_injection,
            'productive_zone_depth': productive_zone_depth,
            'fluid_influx_volume': fluid_influx_volume,
            'lower_circulation_pressure': lower_circulation_pressure,
            'lower_consumption': lower_consumption
            }


def enter_user_data_from_file(file_path: str) -> dict[str, float]:
    """
    Ввод пользовательских данных скважины из текстового файла.

    :param file_path: Путь к текстовому файлу с данными
    :return: Значения исходных данных в виде словаря
    """
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, value = line.strip().split(': ')
            data[name] = float(value)
    return data
