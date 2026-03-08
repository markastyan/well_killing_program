
#подсчет обьема интсрумента для каждого элемента. Всего их 4 в экселе

def drill_tool_internal_volume(d_pipe, l_pipe):
    """
    Расчёт внутреннего объёма бурильного инструмента.

    :param d_pipe: Внутренний диаметр одноразмерного типа труб [м]
    :param l_pipe: Длина секции одноразмерного типа труб [м]
    :return: Внутренний обьем бурильного инструмента [м3]
    """
    return 0.785 * d_pipe ** 2 * l_pipe

# ну потом общий обьем подсчитывается, всего инструмента

# Расчет обьема кольцевого пространства с элементом 4 или 3 (интервал 2)
# Формула также используется для подсчета обьема к.п. интервала 1 с элементом 2 и с элементом 1
def annular_volume_2or1(d_interval_2_or1, d_nar_instrument, l_section):
    """
    Расчёт объёма кольцевого пространства.

    :param d_interval_2_or1: Диаметр интервала 2 или 1 (в зависимости от расчета):  [м]
    :param d_nar_instrument: Наружный диаметр бурильного инструмента (элемент 4 или 3) или (элемент 2 или 1) [м]
    :param l_section: Длина элемента инструмента (4 или 3) или (2 или 1) [м]
    :return: Объём кольцевого пространства (интервал 2 с элементом 4 или элементом 3)  или (интервал 1 с элементом 2 или элементом 1) [м3]
    """
    print("annular_volume_2or1", d_interval_2_or1, d_nar_instrument, l_section)
    return 0.785 * (d_interval_2_or1 ** 2 - d_nar_instrument ** 2) * l_section


#Интервал 1 с элементом 3
def annular_volume_1_3(d_interval_1, d_nar_instrument_3, l_section_4, l_section_3, l_interval_2):
    """
    Расчёт объёма кольцевого пространства.

    :param d_interval_1: Диаметр интервала 1:  [м]
    :param d_nar_instrument_3: Наружный диаметр бурильного инструмента (элемент 3) [м]
    :param l_section_4: Длина элемента инструмента 4 [м]
    :param l_section_3: Длина элемента инструмента 3 [м]
    :param l_interval_2: Длина интервала 2 [м]
    :return: Объём кольцевого пространства интервал 2 с элементом 4 [м3]
    """
    print("annular_volume_1_3", d_interval_1, d_nar_instrument_3, l_section_4, l_section_3, l_interval_2)
    return 0.785 * (d_interval_1 ** 2 - d_nar_instrument_3 ** 2) * (l_section_4 + l_section_3 - l_interval_2)

#Интервал 1 без элементов
def annular_volume_1(d_interval_1, current_depth, l_section_1, l_section_2, l_section_3, l_section_4):
    """
    Расчёт объёма кольцевого пространства.

    :param d_interval_1: Диаметр интервала 1:  [м]
    :param current_depth: Глубина текущего забоя [м]
    :param l_section_1: Длина элемента инструмента 1 [м]
    :param l_section_2: Длина элемента инструмента 2 [м]
    :param l_section_3: Длина элемента инструмента 3 [м]
    :param l_section_4: Длина элемента инструмента 4 [м]
    :return: Объём кольцевого пространства интервал 1 без элементов [м3]
    """
    print("annular_volume_1", d_interval_1, current_depth, l_section_1, l_section_2, l_section_3, l_section_4)
    return 0.785 * d_interval_1 ** 2 * (current_depth - (l_section_1 + l_section_2 + l_section_3 + l_section_4))
