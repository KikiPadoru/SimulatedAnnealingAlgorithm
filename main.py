import os
import random
import math

import imageio.v2 as imageio
import matplotlib.pyplot as plt

cities = [(0, 0), (1, 2), (3, 1), (5, 3), (7, 2), (2, 5), (6, 6), (4, 4), (8, 7)]
images = []

def delete_image_files():
    for img in images:
        os.remove(img)

def paint_gif():
    imageio.mimsave('map.gif', [imageio.imread(img) for img in images], duration=1)


def paint(t, route, distance, k):
    # Построение графика маршрута
    x = [city[0] for city in cities]
    y = [city[1] for city in cities]
    plt.figure(dpi=200)
    plt.plot(x, y, 'ro')  # Рисуем города
    for i in range(len(route) - 1):
        plt.plot([cities[route[i]][0], cities[route[i + 1]][0]], [cities[route[i]][1], cities[route[i + 1]][1]],
                 'b--')  # Рисуем маршрут
    plt.plot([cities[route[-1]][0], cities[route[0]][0]], [cities[route[-1]][1], cities[route[0]][1]],
             'b--')  # Рисуем последний переход
    for i in range(len(route)):
        plt.text(cities[route[i]][0], cities[route[i]][1], str(route[i]), color='k', fontsize=14)
    plt.xlabel('X координата')
    plt.ylabel('Y координата')
    plt.title('Маршрут коммивояжера: {}\nОбщее расстояние: {:.2f}\nИтерация: {:.0f}\nТемпература: {:.1f}'
              .format(route, distance, k, t), loc='left', fontsize=7, fontweight='bold')
    plt.savefig('image/temp{:.0f}.jpg'.format(k))  # Сохранение временного изображения
    images.append('image/temp{:.0f}.jpg'.format(k))  # Добавление временного изображения в список
    plt.close()


def distance(city1, city2):
    # Расстояние между двумя городами по формуле Евклида
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def total_distance(route, cities):
    # Вычисление общего расстояния маршрута
    total = 0
    for i in range(len(route) - 1):
        total += distance(cities[route[i]], cities[route[i + 1]])
    total += distance(cities[route[-1]], cities[route[0]])  # возврат в начальный город
    return total


def simulated_annealing(cities, flag, T_max=100000, T_min=1, iterations=1000):
    current_route = list(range(len(cities)))  # начальный маршрут
    random.shuffle(current_route)  # случайное начальное решение
    current_distance = total_distance(current_route, cities)

    T = T_max
    alpha = 0.91  # коэффициент охлаждения

    best_distance = current_distance
    best_route = current_route

    for num in range(iterations):
        new_route = current_route[:]
        i, j = sorted(random.sample(range(len(cities)), 2))  # выбор двух случайных городов
        new_route[i:j + 1] = reversed(new_route[i:j + 1])  # обмен между выбранными городами
        new_distance = total_distance(new_route, cities)

        if new_distance < current_distance:
            current_route = new_route
            current_distance = new_distance
        else:
            delta = new_distance - current_distance
            if random.random() < math.exp(-delta / T):  # вероятность принятия худшего решения
                current_route = new_route
                current_distance = new_distance

        # Сохранение лучшего маршрута
        if current_distance < best_distance:
            best_distance = current_distance
            best_route = current_route
        if flag:
            paint(T, best_route, best_distance, num)
        if T <= T_min:
            break
        T *= alpha  # уменьшение температуры

    if flag:
        paint_gif()
        delete_image_files()

    return best_route, best_distance


route, distance = simulated_annealing(cities, True)
print("Кратчайший маршрут:", route)
print("Общее расстояние:", distance)
