from typing import List

class Ring(list):
    def __getitem__(self, index):
        return super().__getitem__(index % len(self))

    def __setitem__(self, index, value):
        return super().__setitem__(index % len(self), value)

def sign(num: int) -> int:
    return (num > 0) - (num < 0)

def cyclical_shift(arr: List[int], shift: int) -> List[int]:
    return arr[-shift:] + arr[:-shift]

def gluing_two(arr1: List[int], arr2: List[int]) -> List[int]:
    last_edge = arr1[-1]
    if last_edge in arr2:
        arr2 = [-i for i in arr2[::-1]]
    arr2 = cyclical_shift(arr2, -arr2.index(-last_edge))
    return arr1[:-1] + arr2[1:]

def gluing_all(scheme: List[List[int]]) -> List[int]:
    polygon = scheme.pop(0)
    for _ in range(len(scheme)):
        flag = False
        while not flag:
            last_one = abs(polygon[-1])
            for index, element in enumerate(scheme):
                element = [abs(j) for j in element]
                if last_one in element:
                    polygon = gluing_two(polygon, scheme.pop(index))
                    flag = True
                    break
            if not flag:
                polygon = cyclical_shift(polygon, 1)
    return polygon

def euler(polygon: List[int]) -> int:
    temp = []
    for i in polygon:
        temp.append(0)
        temp.append(i)
    polygon = Ring(temp)
    abs_polygon = Ring([abs(i) for i in temp])
    polygon[0] = 1
    ind, equivalence_class, dot_position = 1, 1, -sign(polygon[1])
    edge = abs_polygon[ind]
    ind = ind + 2
    while 0 in polygon:
        while abs_polygon[ind] != edge:
            ind = ind + 2
        delta_ind = sign(polygon[ind]) * dot_position
        ind = ind + delta_ind
        if polygon[ind] == 0:
            polygon[ind] = equivalence_class
            ind = ind + delta_ind
            edge = abs_polygon[ind]
            dot_position = - sign(polygon[ind]) * delta_ind
            ind = ind + 2
        else:
            if 0 in polygon:
                equivalence_class = equivalence_class + 1
                ind = polygon.index(0)
                polygon[ind] = equivalence_class
                ind = ind + 1
                edge = abs_polygon[ind]
                dot_position = - sign(polygon[ind])
                ind = ind + 2
            else:
                break
    return len(set(list(polygon)[0::2])) - len(set(list(abs_polygon)[1::2])) + 1

def main():
    print("Рекомендации: \n"
          "Введите схему представления поверхности в виде: 1 2 3, -1 -2 -3. \n"
          "То есть многоугольники отделяйте запятыми, а строны одного \n"
          "многоугольника пробелами. Вместо привычных буквенных обозначений \n"
          "используйте цифры и минусы для указания обратного направления. \n"
          "Не используйте нули! \n"
          "\n"
          "Примечание: \n"
          "Проверка корректности введённых данных не предусмотрена. Предполагается, \n"
          "что вы знаете определение правильного семейства многоугольников. \n")

    while True:
        s = input("Введите схему: ")
        polygons = s.split(',')
        scheme = []
        for i in polygons:
            scheme.append([int(j) for j in i.split(' ') if j])
        print(f'Эйлерова характеристика = {euler(gluing_all(scheme))}')
        print()

main()