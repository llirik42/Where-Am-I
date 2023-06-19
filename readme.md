# Где я? (задача с VII Турнира Юных Инжеренеров исследователей, проводимого в Новосибирске в 2021г.)

## Краткое описание

Реализовать программное обеспечение автопилота автомобиля, который движется по городу и составляет карту дорог.

## Условие

Используйте симулятор города с дорожной разметкой https://github.com/duckietown/gym-duckietown.

Автомобиль движется по незнакомому городу и составляет карту города, на которую заносит:
1. Дороги, их протяженность;
2. Перекрестки.

На автомобиле установлена камера, с помощью которой он и строит карту дорог. Задача состоит из трех уровней сложности:
1. Программа получает на вход набор скриншотов из имитатора. Для каждого скриншота известно положение камеры. По этим скриншотам программа строит карту города.
2. Учащийся управляет автомобилем в среде имитатора вручную. Программа строит карту города.
3. Автомобиль движется автоматически и автоматически строит карту города. Автомобиль останавливает движение, когда понимает, что он исследовал всю карту, и сохраняет её.

## Критерии оценивания
* На каждом уровне сложности задачи будет оцениваться точность составленной карты.
* Скорость составления карты.
* Проработанность алгоритма составления карты и формата ее хранения.