"""
Модуль содержит функции для расчёта параметров базовым методом глушения.
"""

from constants import GRAVITY as G, PI


def calculate_reservoir_pressure(drill_pipe_pressure_excess, drilling_fluid_density, current_well_depth):
    """
    Расчёт пластового давления.

    :param drill_pipe_pressure_excess: Избыточное давление в бурильных трубах (на стояке) [Па]
    :param drilling_fluid_density: Плотность бурового раствора в скважине [кг/м^3]
    :param current_well_depth: Глубина текущего забоя [м]
    :return: Пластовое давление [Па]
    """
    return drill_pipe_pressure_excess + G * drilling_fluid_density * current_well_depth


# p_plast = calculate_reservoir_pressure(drill_pipe_pressure_excess, drilling_fluid_density, current_well_depth)
def calculation_density_killing_fluid(p_plast, current_well_depth, productive_zone_depth):
    """
    Расчёт плотности жидкости глушения.

    :param p_plast: Пластовое давление [Па]
    :param current_well_depth: Глубина текущего забоя [м]
    :param productive_zone_depth: Глубина залегания продуктивного горизонта [м]
    :return: Плотность жидкости глушения [кг/м3]
    """
    if productive_zone_depth > 1200:
        k_dop = 1.05
    else:
        k_dop = 1.1
    return k_dop * p_plast / (G * current_well_depth)


def get_tool_friction_loss(f, density_liquid, v, d_nar_instrument, l_pipe):
    return ((f * density_liquid * (v**2))/(2*d_nar_instrument)) * l_pipe


def get_fluid_speed(Q, d_nar_instrument):
    return (4 * Q) / (PI * d_nar_instrument**2)


def reynolds_criterion(density_liquid, v, d_nar_instrument, viscosity):
    return (density_liquid * v * d_nar_instrument) / viscosity


def friction_coef(reynolds_criterion_value):
    if reynolds_criterion_value <= 2000:  # Ламинарный режим потока
        return 64/reynolds_criterion_value
    else:  # Турбулентный режим потока
        return 0.316/(reynolds_criterion_value**(1/4))


# density_liquid = calculation_density_killing_fluid(p_plast, current_well_depth, productive_zone_depth)
def calculate_initial_standpipe_pressure(Q, d_nar_instrument, density_liquid, viscosity, l_pipe,
                                         drill_pipe_pressure_excess, reserve_pressure):
    """
    Расчёт начального давление на стояке во время вымыва пластового флюида из кольцевого пространства.

    :param Q: Подача насоса при бурении (промывке) скважины [м^3/c]
    :param d_nar_instrument: Наружный диаметр одноразмерного бурильного инструмента [м]
    :param density_liquid: Плотность жидкости глушения [кг/м^3]
    :param viscosity: Вязкость жидкости глушения [Па * с]
    :param l_pipe: Длина секции одноразмерного типа труб [м]
    :param drill_pipe_pressure_excess: Избыточное давление в бурильных трубах (на стояке) [Па]
    :param reserve_pressure: Дополнительное избыточное давление на стояке при закачке [Па]
    :return: Начальное давление на стояке во время вымыва пластового флюида из кольцевого пространства
    """
    v = get_fluid_speed(Q, d_nar_instrument)  # Cкорость потока флюида в трубах
    reynolds_criterion_value = reynolds_criterion(density_liquid, v, d_nar_instrument, viscosity)
    f = friction_coef(reynolds_criterion_value)
    tool_friction_loss = get_tool_friction_loss(f, density_liquid, v, d_nar_instrument, l_pipe)
    return drill_pipe_pressure_excess + tool_friction_loss + reserve_pressure


def calculate_target_circulation_pressure(tool_friction_loss, reserve_pressure):
    """
    Расчёт целевого давления циркуляции после закачки в трубное пространство жидкости глушения.

    :param tool_friction_loss: Потери давления на трение в инструменте [Па]
    :param reserve_pressure: Дополнительное избыточное давление на стояке при закачке [Па]
    :return: Целевое давление циркуляции после закачки в трубное пространство жидкости глушения
    """
    return tool_friction_loss + reserve_pressure


def calculate_initial_standpipe_pressure_multiple_pipes(drill_pipe_pressure_excess, reserve_pressure, sum_loss_pressure):
    """
    Расчёт начального давление на стояке во время вымыва пластового флюида из кольцевого пространства.
    :param sum_loss_pressure: Сумма потерь давления во всем инструменте [Па]
    :param drill_pipe_pressure_excess: Избыточное давление в бурильных трубах (на стояке) [Па]
    :param reserve_pressure: Дополнительное избыточное давление на стояке при закачке [Па]
    :return: Начальное давление на стояке во время вымыва пластового флюида из кольцевого пространства
    """
    return drill_pipe_pressure_excess + sum_loss_pressure + reserve_pressure
