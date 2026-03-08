"""
Модуль содержит функции для расчёта параметров, общих для всех методов глушения.
"""

from constants import GRAVITY as G, PI


def drill_tool_internal_volume(d_pipe, l_pipe):
    """
    Расчёт внутреннего объёма бурильного инструмента.

    :param d_pipe: Внутренний диаметр одноразмерного типа труб [м]
    :param l_pipe: Длина секции одноразмерного типа труб [м]
    :return: Внутренний обьем бурильного инструмента [м3]
    """
    return 0.785 * d_pipe ** 2 * l_pipe


def annular_volume(d_interval, d_nar_instrument, l_section, l_current):
    """
    Расчёт объёма кольцевого пространства

    :param d_interval: Диаметр интервала: (в случае открытого ствола - берется диаметр долота;
                                           в случае обсаженного ствола – внутренний диаметр обсадной колонны) [м]
    :param d_nar_instrument: Наружный диаметр одноразмерного бурильного инструмента [м]
    :param l_section: Длина секции одноразмерного типа труб [м]
    :param l_current: Глубина текущего забоя [м]
    :return: Объём кольцевого пространства [м3]
    """
    return ((0.785 * (d_interval ** 2 - d_nar_instrument ** 2) * l_section) +
            (0.785 * d_interval ** 2 * (l_current - l_section)))


# ОПРЕДЕЛЕНИЕ ГРАНИЧНЫХ ПАРАМЕТРОВ ПРОЦЕССА ГЛУШЕНИЯ:


def casing_max_allowable_pressure(p_crimping_k):
    """
    Расчёт максимально допустимого давления на устье с точки зрения прочности обсадной колонны

    :param p_crimping_k: Давление опрессовки обсадной колонны [Па]
    :return: Максимально допустимое давление на устье с точки зрения прочности обсадной колонны [Па]
    """
    return 0.8 * p_crimping_k


# p_excess_k = casing_max_allowable_pressure(p_crimping_k)
def circulation_pressure(pressure_begin, p_excess_k):
    """
    Начальное давление циркуляции должно удовлетворять этому условию

    :param pressure_begin: Начальное давление циркуляции [Па]
    :param p_excess_k: Максимально-допустимое давление на устье [Па]
    :return: True, если условие начального давления циркуляции удовлетворено; иначе False
    """
    return pressure_begin < p_excess_k


def equivalent_density_beginning_absorption(pressure_absorption_formation, h):
    """
    Расчёт эквивалентной плотности начала поглощения

    :param pressure_absorption_formation: Давление начала поглощения слабого пласта [Па]
    :param h: Глубина залегания слабого пласта [м]
    :return: Эквивалентная плотность начала поглощения [Па/м]
    """
    return pressure_absorption_formation / (G * h)


def equivalent_density_hydraulic_fracturing(weak_formation_fracture_pressure, h):
    """
    Расчёт эквивалентной плотности начала гидроразрыва

    :param weak_formation_fracture_pressure: Давление гидроразрыва слабого пласта [Па]
    :param h: Глубина залегания слабого пласта [Па]
    :return: Эквивалентная плотность начала гидроразрыва [Па/м]
    """
    return weak_formation_fracture_pressure / (G * h)


#equivalent_density_beginning_absorption = equivalent_density_beginning_absorption(pressure_absorption_formation, h)
#equivalent_density_hydraulic_fracturing = equivalent_density_hydraulic_fracturing(weak_formation_fracture_pressure, h)
def kill_fluid_density_condition(kill_fluid_density, equivalent_density_beginning_absorption, equivalent_density_hydraulic_fracturing):
    """
    Плотность жидкости глушения должна удовлетворять этому условию

    :param kill_fluid_density: плотность жидкости глушения [Кг/M^3]
    :param equivalent_density_beginning_absorption: Эквивалентная плотность начала поглощения [кг/м^3]
    :param equivalent_density_hydraulic_fracturing: Эквивалентная плотность начала гидроразрыва [кг/м^3]
    :return: True, если условие плотности жидкости глушения удовлетворено; иначе False
    """
    return kill_fluid_density < equivalent_density_beginning_absorption < equivalent_density_hydraulic_fracturing


# АНАЛИЗ ГАЗОНЕФТЕВОДОПРОЯВЛЕНИЯ:


def annular_fluid_column_height(v_fluid_well, current_depth, tool_depth, q_i_open, q_i_annular):
    """
    Расчёт высоты столба флюида в кольцевом пространстве (считая от забоя)

    :param v_fluid_well: Объем поступившего в скважину флюида [м^3]
    :param current_depth: Глубина текущего забоя [м]
    :param tool_depth: Глубина спуска инструмента [м]
    :param q_i_open: Удельный объем 1 метра открытого ствола [м]
    :param q_i_annular: Удельный объем 1 метра кольцевого пространства
    :return: Высота столба флюида в кольцевом пространстве (считая от забоя)
    """
    return ((v_fluid_well - (current_depth-tool_depth) * q_i_open) / q_i_annular) + (current_depth-tool_depth)


def annular_space_volume_per_meter(d_interval, d_nar_instrument):
    """
    Расчёт удельного объёма 1 метра кольцевого пространства инструмент – ствола скважины

    :param d_interval: Диаметр интервала [м]
    :param d_nar_instrument: Наружный диаметр одноразмерного бурильного инструмента [м]
    :return: Удельный объём 1 метра кольцевого пространства инструмент – ствол скважины [м^2]
    """
    return 0.785 * (d_interval ** 2 - d_nar_instrument ** 2)


def open_borehole_volume_per_meter(d_interval):
    """
    Расчёт удельного объёма 1 метра открытого ствола (забоя)

    :param d_interval: Диаметр интервала [м]
    :return: Удельный объём 1 метра открытого ствола (забоя) [м^2]
    """
    return 0.785 * d_interval ** 2


# Z = annular_fluid_column_height(v_fluid_well, tool_depth, q_i, l_pipe)
def reservoir_fluid_density(wellhead_pressure_excess, drill_pipe_pressure_excess, Z):
    """
    Определение плотности пластового флюида, поступившего в скважину

    :param wellhead_pressure_excess: Избыточное давление на устье скважины после её закрытия и стабилизации давления [Па]
    :param drill_pipe_pressure_excess: Избыточное давление в бурильных трубах (на стояке) [Па]
    :param Z: Высота столба флюида в кольцевом пространстве (считая от забоя) [м]
    :return: Плотность пластового флюида, поступившего в скважину
    """
    return (wellhead_pressure_excess - drill_pipe_pressure_excess) / (G * Z)


# fluid_value = reservoir_fluid_density (drilling_fluid_density, wellhead_pressure_excess,
# drill_pipe_pressure_excess, annular_fluid_column_height, Z)
def fluid_type(fluid_value):
    """
    Определение вида пластового флюида, поступившего в скважину

    :param fluid_value: Плотность пластового флюида, поступившего в скважину
    :return: Вид пластового флюида, поступившего в скважину
    """
    if 10 <= fluid_value < 360:
        return "Газ"
    elif 360 <= fluid_value < 700:
        return "Газовый конденсат"
    elif 700 <= fluid_value < 1080:
        return "Газированная нефть"
    elif 1080 <= fluid_value <= 1200:
        return "Пластовая вода"
    else:
        return "Ошибка в данных"


def calculate_drill_tool_internal_volume_multiple_pipes(inner_intervals):
    res = 0
    for i in inner_intervals:
        res += PI*0.25*i[0]*i[1]*i[1]
    return res


def calculate_annular_volumes_multiple_pipes(outer_intervals, inner_intervals, diff, isMultiple=False, inner_tube_intervals=None):
    volumes = [PI * diff * outer_intervals[0][1] * outer_intervals[0][1] / 4]
    volumes_inner_tube = [0]
    lengths = []
    outer_intervals[0] = (outer_intervals[0][0]-diff, outer_intervals[0][1])
    outer_index, inner_index = 0, 0
    outer_length_rem, inner_length_rem = outer_intervals[0][0], inner_intervals[0][0]
    while outer_index < len(outer_intervals) and inner_index < len(inner_intervals):
        outer_length, outer_diameter = outer_intervals[outer_index]
        inner_length, inner_diameter = inner_intervals[inner_index]
        segment_length = min(outer_length_rem, inner_length_rem)
        outer_radius = outer_diameter / 2
        inner_radius = inner_diameter / 2
        segment_volume = PI * segment_length * (outer_radius**2 - inner_radius**2)
        lengths.append(segment_length)
        volumes.append(segment_volume)
        if isMultiple:
            inner_tube_radius = inner_tube_intervals[inner_index]
            volumes_inner_tube.append(PI * segment_length * (inner_tube_radius**2))
        outer_length_rem -= segment_length
        inner_length_rem -= segment_length
        if outer_length_rem == 0:
            outer_index += 1
            if outer_index < len(outer_intervals):
                outer_length_rem = outer_intervals[outer_index][0]
        if inner_length_rem == 0:
            inner_index += 1
            if inner_index < len(inner_intervals):
                inner_length_rem = inner_intervals[inner_index][0]
    if isMultiple:
        sum_volumes = []
        for i in range(len(volumes)):
            sum_volumes.append(volumes[i]+volumes_inner_tube[i])
        return sum_volumes, lengths
    return volumes, lengths

'''
def calc_fluid_h(v_fluid_well, current_depth, volume_list_kp):
    """
    Расчет высоты столба флюида

    :param v_fluid_well:  Обьем притока поступившего в скважину
    :param current_depth: Глубина пласта
    :param volume_list_kp: Массив: [ОБЬЕМ_ЗАТРУБНОГО_ПРОСТРАНСТВА, длина элемента]
    :return:
    """
    current_value = v_fluid_well
    h = 0
    for value in volume_list_kp:
        if len(value) > 0:
            past_current_value = current_value
            past_h = h
            current_value -= value[0]
            h -= value[1]
            if h < 0:
                h = -h
            if current_value <= 0:
                specific_volume = value[0] / value[1]
                h_fluid = current_depth - (past_h - past_current_value/specific_volume)
                return h_fluid
'''

def calc_fluid_h(v_fluid_well, volume_list_kp):
    """
    Расчет высоты столба флюида

    :param v_fluid_well:  Обьем притока поступившего в скважину
    :param volume_list_kp: Массив: [ОБЬЕМ_ЗАТРУБНОГО_ПРОСТРАНСТВА, длина элемента]
    :return:
    """
    h = 0
    for cur_val in volume_list_kp:
        if v_fluid_well >= cur_val[0]:
            h += cur_val[1]
            v_fluid_well -= cur_val[0]
            #print("norm h, v", h, v_fluid_well)
        else:
            h += cur_val[1]*v_fluid_well/cur_val[0]
            #print("low h", h)
            return h


def calc_water_h(time, speed_potok, volume_list_kp, current_depth, lowering_depth, inner_pipe_values, density, viscosity, volume_instr=None, outer_pipe_values=None):
    """
    Расчет уровней жидкости для глушения в трубе и затрубном пространстве в момент времени t.

    :param time: Время закачки жидкости (минуты).
    :param speed_potok: Скорость закачки жидкости (литры в минуту).
    :param volume_list_kp: Список интервалов: [(объем на единицу длины, длина интервала)].
    :param current_depth: Глубина пласта (метры).
    :param volume_instr: Внутренний объем трубы (литры). Если None, расчет безнапорной закачки.
    :param density: Плотность жидкости глушения (кг/м³).
    :param viscosity: Вязкость жидкости глушения (Па * с) (это входные данные)
    :param lowering_depth: Глубина спуска инструмента
    :return: Уровень жидкости в трубе (метры), уровень жидкости в затрубном пространстве (метры).
    """
    # Рассчитываем общий объем закачанной жидкости
    volume_potok = time * speed_potok

    level_in_tube = 0
    pressure_loss = 0


    if volume_instr is not None:
        # Напорная закачка
        if volume_instr > volume_potok:
            level_in_annulus = 0
            inner_pipe_values = inner_pipe_values[::-1]
            #print('inner_pipe_value', inner_pipe_values)
            for i in inner_pipe_values:
                #print('volume_potok', volume_potok)
                cur_vol = PI*i[1]*i[1]*i[2]/4
                #print('cur_vol', cur_vol)
                reynolds_criterion = (density * speed_potok * i[1]) / viscosity
                if reynolds_criterion <= 2000:
                    f = 64 / reynolds_criterion
                else:
                    f = 0.316 / (reynolds_criterion ** (1 / 4))
                if volume_potok > cur_vol:
                    volume_potok -= cur_vol
                    level_in_tube += i[2]
                    #Начинается магия
                    temporary_pressure_loss = ((f * density * (speed_potok**2)) / 2*i[1]) *i[2]
                    pressure_loss = pressure_loss + temporary_pressure_loss
                    # Магия заканчивается

                else:
                    level_in_tube += volume_potok/(PI*i[1]*i[1]/4)
                    temporary_pressure_loss = ((f * density * (speed_potok ** 2)) / 2 * i[1]) * (volume_potok/(PI*i[1]*i[1]/4))
                    pressure_loss = pressure_loss + temporary_pressure_loss

        else:
            volume_potok -= volume_instr
            #print(volume_potok, current_depth, volume_list_kp)
            #print(calc_fluid_h(volume_potok, current_depth, volume_list_kp))
            # Считаем потери давления в инструменте
            for i in inner_pipe_values:
                reynolds_criterion = (density * speed_potok * i[1]) / viscosity
                if reynolds_criterion <= 2000:
                    f = 64 / reynolds_criterion
                else:
                    f = 0.316 / (reynolds_criterion ** (1 / 4))
                temporary_pressure_loss = ((f * density * (speed_potok ** 2)) / 2 * i[1]) * i[2]
                pressure_loss = pressure_loss + temporary_pressure_loss # получили сумму потерь в инструменте

            level_in_tube = lowering_depth
            level_in_annulus = calc_fluid_h(volume_potok, volume_list_kp)
            #print(volume_potok, level_in_annulus)
            level_in_annulus = min(current_depth, float(level_in_annulus or current_depth))
    else:
        # Безнапорная закачка
        sum_volumes, lengths = calculate_annular_volumes_multiple_pipes([(val[1], val[0]) for val in outer_pipe_values], [(val[2], val[0]) for val in inner_pipe_values], current_depth-lowering_depth, isMultiple=True, inner_tube_intervals=[val[1] for val in inner_pipe_values])
        level_in_tube = calc_fluid_h(volume_potok, [[i, j] for i, j in zip(sum_volumes, lengths)])
        level_in_annulus = (level_in_tube or 0) + current_depth - lowering_depth
        level_in_tube = lowering_depth - min(lowering_depth, float(level_in_tube or lowering_depth))
        level_in_annulus = min(current_depth, float(level_in_annulus or current_depth))
    return level_in_tube, level_in_annulus, pressure_loss

'''
volume_list_kp = [(0.05, 100), (0.03, 200)]  # Интервалы: объем 0.05 л/м на 100 м и 0.03 л/м на 200 м
current_depth = 300  # Глубина пласта, м
time = 30  # Минуты
speed_potok = 10  # Литры в минуту
volume_instr = 500  # Литры

level_in_tube, level_in_annulus = calc_water_h(time, speed_potok, volume_list_kp, current_depth, volume_instr)
print(f"Уровень в трубе: {level_in_tube:.2f} м, уровень в затрубном пространстве: {level_in_annulus:.2f} м")
'''