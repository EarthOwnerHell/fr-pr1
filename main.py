import math
from datetime import datetime, timedelta

# Параметры сервиса 
FREE_DELIVERY_FROM = 2000.0   # порог бесплатной доставки, руб.
WORK_START_HOUR = 8           # сервис работает с 08:00
WORK_END_HOUR = 23            # ... до 23:00
PREP_MINUTES = 10             # время на сборку и передачу заказа курьеру
OVERWEIGHT_LIMIT_KG = 10.0    # вес, свыше которого начинается надбавка
OVERWEIGHT_RATE = 20.0        # цена за каждый килограмм сверх лимита, руб.


# Функция 1. Оформление заказа: зона и стоимость доставки 
def delivery_zone(distance_km):
    """Название зоны доставки по расстоянию до клиента."""
    if distance_km <= 3.0:
        return "Центр"
    if distance_km <= 8.0:
        return "Городская зона"
    return "Пригород"


def zone_base_price(distance_km):
    """Базовый тариф доставки для зоны, руб."""
    if distance_km <= 3.0:
        return 149.0
    if distance_km <= 8.0:
        return 249.0
    return 399.0


def zone_travel_minutes(distance_km):
    """Ориентировочное время в пути по зоне, мин."""
    if distance_km <= 3.0:
        return 15
    if distance_km <= 8.0:
        return 30
    return 55


def weight_surcharge(weight):
    """Надбавка за тяжёлый заказ: каждый кг сверх лимита стоит OVERWEIGHT_RATE."""
    if weight > OVERWEIGHT_LIMIT_KG:
        extra_kg = math.ceil(weight - OVERWEIGHT_LIMIT_KG)
        return extra_kg * OVERWEIGHT_RATE
    return 0.0


def is_free_delivery(goods_sum):
    """Признак бесплатной доставки при крупном заказе."""
    return goods_sum >= FREE_DELIVERY_FROM


def delivery_cost(distance_km, weight, goods_sum):
    """Итоговая стоимость доставки с учётом веса и бесплатного порога."""
    if is_free_delivery(goods_sum):
        return 0.0
    return zone_base_price(distance_km) + weight_surcharge(weight)


def total_to_pay(distance_km, weight, goods_sum):
    """Общая сумма к оплате: товары + доставка."""
    return goods_sum + delivery_cost(distance_km, weight, goods_sum)


# Функция 2. Назначение курьера 
def courier_type(weight):
    """Тип курьера по весу заказа."""
    if weight <= 5.0:
        return "пеший курьер"
    if weight <= 15.0:
        return "велокурьер"
    return "автокурьер"


def courier_name(weight):
    """Имя курьера, закреплённого за данным типом передвижения."""
    if weight <= 5.0:
        return "Алексей"
    if weight <= 15.0:
        return "Марат"
    return "Сергей"


def is_working_time(moment):
    """Попадает ли момент времени в рабочие часы сервиса."""
    return WORK_START_HOUR <= moment.hour < WORK_END_HOUR


def is_courier_assigned(moment, courier_is_free):
    """Можно ли назначить курьера: рабочее время и есть свободный курьер."""
    return is_working_time(moment) and courier_is_free


# Функция 3. Расчёт срока доставки
def delivery_minutes(distance_km):
    """Полное время доставки: сборка + путь по зоне, мин."""
    return PREP_MINUTES + zone_travel_minutes(distance_km)


def planned_delivery_at(created_at, distance_km):
    """Плановое время вручения заказа."""
    return created_at + timedelta(minutes=delivery_minutes(distance_km))


# Функция 4. Отслеживание статуса заказа
def order_status(moment, courier_is_free):
    """Текущий статус заказа на момент оформления."""
    if not is_working_time(moment):
        return "отменён: сервис не работает в это время"
    if not is_courier_assigned(moment, courier_is_free):
        return "ожидает свободного курьера"
    return "передан курьеру, в пути к клиенту"


# Функция 5. Формирование квитанции
def tracking_number(created_at, order_number):
    """Трек-номер заказа: дата + номер заказа."""
    return "DLV-" + created_at.strftime("%Y%m%d") + "-" + str(order_number)


def payment_method_name(payment_is_online):
    """Человекочитаемое название способа оплаты."""
    if payment_is_online:
        return "онлайн-оплата"
    return "наличные курьеру"


def build_receipt(created_at, order_number, client_name, client_phone,
                  distance_km, weight, goods_sum, payment_is_online,
                  courier_is_free):
    """Собирает текст итоговой квитанции по заказу (переиспользует функции 1–4)."""
    receipt = "=== Квитанция по заказу ===\n"
    receipt += "Трек-номер:            " + tracking_number(created_at, order_number) + "\n"
    receipt += "Клиент:                " + client_name + ", " + client_phone + "\n"
    receipt += ("Зона доставки:         " + delivery_zone(distance_km)
                + " (" + str(distance_km) + " км)\n")
    receipt += "Вес заказа:            " + str(weight) + " кг\n"
    receipt += ("Курьер:                " + courier_name(weight)
                + " (" + courier_type(weight) + ")\n")
    receipt += "Сумма товаров:         " + str(round(goods_sum, 2)) + " руб.\n"

    if is_free_delivery(goods_sum):
        receipt += ("Доставка:              бесплатно (заказ от "
                    + str(FREE_DELIVERY_FROM) + " руб.)\n")
    else:
        receipt += ("Доставка:              "
                    + str(round(delivery_cost(distance_km, weight, goods_sum), 2))
                    + " руб.\n")
        if weight_surcharge(weight) > 0.0:
            receipt += ("  в т.ч. надбавка за вес: "
                        + str(round(weight_surcharge(weight), 2)) + " руб.\n")

    receipt += ("Итого к оплате:        "
                + str(round(total_to_pay(distance_km, weight, goods_sum), 2))
                + " руб. (" + payment_method_name(payment_is_online) + ")\n")
    receipt += "Заказ создан:          " + created_at.strftime("%d.%m.%Y %H:%M") + "\n"
    receipt += ("Плановая доставка:     "
                + planned_delivery_at(created_at, distance_km).strftime("%d.%m.%Y %H:%M")
                + " (через " + str(delivery_minutes(distance_km)) + " мин)\n")
    receipt += "Статус заказа:         " + order_status(created_at, courier_is_free)
    return receipt


# Сценарий: оформление конкретного заказа 
# Исходные данные (в реальном приложении придут из формы, поэтому строки)
client_name = "Ирина Соколова"
client_phone = "+7 900 123-45-67"
order_number_raw = "1047"
goods_sum_raw = "1490.00"
weight_raw = "7.4"
distance_km_raw = "6.2"
payment_is_online = True
courier_is_free = True
created_at = datetime(2026, 9, 8, 19, 30)

# Преобразование типов: строки -> числа
order_number = int(order_number_raw)
goods_sum = float(goods_sum_raw)
weight = float(weight_raw)
distance_km = float(distance_km_raw)

print(build_receipt(created_at, order_number, client_name, client_phone,
                    distance_km, weight, goods_sum, payment_is_online,
                    courier_is_free))
