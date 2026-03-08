"""
Модуль для расчета глушения методом Бурильщика
"""

from constants import GRAVITY as G


#новая переменная q_lowered вводимая пользователем
def calculate_pressure_circulation(p, q_lowered, q, lowering_depth, current_depth):
    """
    Расчёт давления циркуляции на пониженной подаче давления на стояке при пониженной подаче насоса

    :param p: Давление на стояке манифольда при бурении (промывке) скважины [Па]
    :param q_lowered: Расход при пониженной подаче насоса [м^3/c]
    :param q: Подача насоса при бурении (промывке) скважины [м^3/c]
    :param lowering_depth: Глубина спуска инструмента [м]
    :param current_depth: Глубина текущего забоя [м]
    :return: Давление циркуляции при пониженной подаче насоса [Па]
    """
    circulation_pressure = 1.1 * p * ((q_lowered/q)**2) * (lowering_depth / current_depth)
    return circulation_pressure


def calc_max_wellhead_pressure(casing_pressure_test, pressure_absorption_formation, drilling_mud_density, h):
    """
    Максимально-допустимое давление на устье с точки зрения прочности обсадной колонны:

    :param casing_pressure_test: Давление опрессовки обсадной колонны [Па]
    :param pressure_absorption_formation: Давление начала поглощения слабого пласта [Па]
    :param drilling_mud_density: Плотность бурового раствора в скважине [кг/м3]
    :param h: Глубина залегания слабого пласта [м]
    :return: Максимально-допустимое давление на устье для недопущения поглощения, максимально-допустимое давление [Па]
    """

    a = casing_pressure_test * 0.8
    b = pressure_absorption_formation - (drilling_mud_density * G * h)

    return b, min(a, b)


def calc_initial_circulation_pressure(drill_pipe_pressure_excess, circulation_pressure,
                                      additional_standpipe_pressure_during_injection):
    """
    Расчёт начального давление циркуляции

    :param drill_pipe_pressure_excess: Избыточное давление в бурильных трубах (на стояке) [Па]
    :param circulation_pressure: Давление циркуляции при пониженной подаче насоса [Па]
    :param additional_standpipe_pressure_during_injection: Дополнительное избыточное давление на стояке при закачке [Па]
    :return: Начального давление циркуляции [Па]
    """
    return drill_pipe_pressure_excess + circulation_pressure + additional_standpipe_pressure_during_injection


def calc_fact_reservoir_pressure(drill_pipe_pressure_excess, drilling_fluid_density, productive_zone_depth):
    """
    Фактическое пластовое давление вскрытого пласта:

    :param drill_pipe_pressure_excess: Избыточное давление в бурильных трубах (на стояке) [Па]
    :param drilling_fluid_density: Плотность бурового раствора в скважине [кг/м^3]
    :param productive_zone_depth: Глубина залегания продуктивного горизонта [м]
    :return: Фактическое пластовое давление [Па]
    """
    fact_reservoir_pressure = drill_pipe_pressure_excess + G * drilling_fluid_density * productive_zone_depth
    return fact_reservoir_pressure

#ПЕРЕДАЮТСЯ ДРУГИЕ ДАННЫЕ
def calc_mud_density_increment(productive_zone_depth, fact_reservoir_pressure, drilling_fluid_density, current_depth):
    """
    Определение дополнительного приращения плотности промывочной жидкости

    :param productive_zone_depth: Глубина залегания продуктивного горизонта [м]
    :param fact_reservoir_pressure: Фактическое пластовое давление [Па]
    :param drilling_fluid_density: Плотность бурового раствора в скважине [кг/м^3]
    :param current_depth: Глубина текущего забоя [м]
    :return: Дополнительное приращение плотности промывочной жидкости
    """
    if productive_zone_depth > 1200:
        a = 1.05
    else:
        a = 1.1
    mud_density_increment = (a * fact_reservoir_pressure) / G / current_depth - drilling_fluid_density
    return mud_density_increment

#ПЕРЕДАЮТСЯ ДРУГИЕ ДАННЫЕ
def calc_kill_mud_density(fact_reservoir_pressure, current_depth, productive_zone_depth):
    """
    Определение плотности жидкости глушения, необходимой для глушения скважины

    :param  fact_reservoir_pressure: Фактическое пластовое давление[Па]
    :param current_depth: Глубина текущего забоя [м]
    :param productive_zone_depth: Глубина залегания продуктивного горизонта [м]
    :return: Плотность жидкости глушения, необходимой для глушения скважины [кг/м3]
    """
    if productive_zone_depth > 1200:
        a = 1.05
    else:
        a = 1.1
    kill_mud_density = (a * fact_reservoir_pressure) / G / current_depth
    return kill_mud_density

#ПЕРЕДАЮТСЯ ДРУГИЕ ДАННЫЕ
def calc_final_circulation_pressure(circulation_pressure, kill_mud_density, drilling_mud_density, additional_standpipe_pressure_during_injection):
    """
    Определение конечного давления циркуляции при глушении скважины:

    :param circulation_pressure: Давление циркуляции при пониженной подаче насоса [Па]
    :param kill_mud_density: Плотности жидкости глушения, необходимой для глушения скважины [кг/м3]
    :param drilling_mud_density: Плотность бурового раствора в скважине [кг/м3]
    :param additional_standpipe_pressure_during_injection: Дополнительное избыточное давление на стояке при закачке [Па]

    :return: Конечное давление циркуляции при глушении скважины [Па]
    """
    return circulation_pressure * kill_mud_density / drilling_mud_density + additional_standpipe_pressure_during_injection


def calc_gradient(drill_pipe_pressure_excess, drilling_mud_density, productive_zone_depth):
    """
    Определение градиента распределения избыточного трубного давления

    :param drill_pipe_pressure_excess: Избыточное давление в бурильных трубах (на стояке) [Па]
    :param drilling_mud_density: Плотность бурового раствора в скважине [кг/м3]
    :param productive_zone_depth: Глубина залегания продуктивного горизонта [м]
    :return: Градиент распределения избыточного трубного давления
    """
    gradient = drill_pipe_pressure_excess / (G * drilling_mud_density * productive_zone_depth)
    return gradient


#v_annular = annular_volume()
def calc_maximum_v_gas(v_fluid, v_annular, gradient):
    """
    Определение максимального увеличения объема газовой пачки при подходе к устью

    :param v_fluid: Объем поступившего в скважину флюида [м^3]
    :param v_annular: Объем кольцевого пространства [м^3]
    :param gradient: Градиент распределения избыточного трубного давления
    :return: Максимальное увеличение объема газовой пачки [м^3]
    """
    b = gradient**2 + 4*(gradient + 1) * v_fluid/v_annular
    b = b**(1/2)
    c = b - gradient
    maximum_v_gas = 0.5 * v_annular * c
    return maximum_v_gas


def calc_maximum_pressure_annular_space(fact_reservoir_pressure, drill_pipe_pressure_excess, maximum_v_gas, v_annular):
    """
    Определение максимального давления в кольцевом пространстве в процессе глушения скважины:

    :param fact_reservoir_pressure: Фактическое пластовое давление [Па]
    :param drill_pipe_pressure_excess: Избыточное давление в бурильных трубах (на стояке) [Па]
    :param maximum_v_gas: Максимальное увеличение объема газовой пачки [м^3]
    :param v_annular: Объем кольцевого пространства [м^3]
    :return: Максимальное давление в кольцевом пространстве
    """
    return drill_pipe_pressure_excess + ((fact_reservoir_pressure - drill_pipe_pressure_excess) *
                                         (maximum_v_gas / v_annular))


def calc_point_maximum_pressure(v_annular, maximum_v_gas):
    """
    Определение точки максимального давления на графике первой стадии глушения скважины:

    :param v_annular: Объем кольцевого пространства [м^3]
    :param maximum_v_gas: Максимальное увеличение объема газовой пачки [м^3]
    :return: Точка максимального давления на графике первой стадии глушения скважины
    """
    point_maximum_pressure = v_annular - maximum_v_gas
    return point_maximum_pressure

#ПЕРЕДАЮТСЯ ДРУГИЕ ДАННЫЕ
#Расчет продолжительности глушения:
#v_internal=drill_tool_internal_volume()
def calc_duration_pipe_replacement(v_internal, q_lowered):
    """
    Продолжительность стадии замещения жидкости в трубах

    :param v_internal: внутренний объем бурильного инструмента [м^3]
    :param q_lowered: Расход при пониженной подаче насоса [м^3/c]
    :return: Продолжительность стадии замещения жидкости в трубах
    """
    t_tr = (v_internal / q_lowered)/60
    return t_tr

#ПЕРЕДАЮТСЯ ДРУГИЕ ДАННЫЕ
def calc_duration_pipe_annular(v_annular, q_lowered, t_tr):
    """
    Продолжительность стадии замещения жидкости в кольцевом пространстве

    :param v_annular: внутренний обьем кольцевого пространства[м^3]
    :param q_lowered: Расход при пониженной подаче насоса [м^3/c]
    :return: Продолжительность стадии замещения жидкости в кольцевом пространстве
    """
    t_annular = (t_tr + v_annular / q_lowered) / 60
    return t_annular


# Продолжительность одного цикла циркуляции:
def calc_circulation_cycle(t_tr, t_annular):
    """
    Продолжительность стадии замещения жидкости в кольцевом пространстве

    :param t_tr: Продолжительность стадии замещения жидкости в трубах
    :param t_annular: Продолжительность стадии замещения жидкости в кольцевом пространстве
    :return: Продолжительность одного цикла циркуляции
    """
    t_c = t_tr + t_annular
    return t_c