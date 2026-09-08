import math
from datetime import datetime, timedelta

# Исходные данные заказа (в реальном приложении придут из формы) 
client_name = "Ирина Соколова"
client_phone = "+7 900 123-45-67"
order_number_raw = "1047"          # номер заказа приходит строкой
goods_sum_raw = "1490.00"          # сумма товаров приходит строкой
weight_raw = "7.4"                 # вес заказа в килограммах, строка
distance_km_raw = "6.2"            # расстояние до клиента, строка
payment_is_online = True           # оплата картой онлайн или наличными курьеру
created_at = datetime(2026, 9, 8, 19, 30)

# Преобразование типов: строки -> числа
order_number = int(order_number_raw)
goods_sum = float(goods_sum_raw)
weight = float(weight_raw)
distance_km = float(distance_km_raw)

# Функция 1. Оформление заказа: зона доставки и стоимость 
FREE_DELIVERY_FROM = 2000.0  # порог бесплатной доставки, руб.

if distance_km <= 3.0:
    zone_name = "Центр"
    base_delivery_price = 149.0
    travel_minutes = 15
elif distance_km <= 8.0:
    zone_name = "Городская зона"
    base_delivery_price = 249.0
    travel_minutes = 30
else:
    zone_name = "Пригород"
    base_delivery_price = 399.0
    travel_minutes = 55

# Надбавка за тяжёлый заказ: каждый килограмм свыше 10 кг стоит +20 руб.
if weight > 10.0:
    overweight_kg = math.ceil(weight - 10.0)
    weight_surcharge = overweight_kg * 20.0
else:
    weight_surcharge = 0.0

delivery_price = base_delivery_price + weight_surcharge

# Бесплатная доставка при крупном заказе
if goods_sum >= FREE_DELIVERY_FROM:
    delivery_is_free = True
    delivery_cost = 0.0
else:
    delivery_is_free = False
    delivery_cost = delivery_price

total_to_pay = goods_sum + delivery_cost

# Функция 2. Назначение курьера 
# Сервис работает с 08:00 до 23:00
work_start_hour = 8
work_end_hour = 23
is_working_time = work_start_hour <= created_at.hour < work_end_hour

courier_is_free = True  # диспетчер видит, что свободный курьер есть

if weight <= 5.0:
    courier_type = "пеший курьер"
    courier_name = "Алексей"
elif weight <= 15.0:
    courier_type = "велокурьер"
    courier_name = "Марат"
else:
    courier_type = "автокурьер"
    courier_name = "Сергей"

courier_assigned = is_working_time and courier_is_free

# Функция 3. Расчёт срока доставки 
prep_minutes = 10  # время на сборку и передачу заказа курьеру
total_minutes = prep_minutes + travel_minutes
planned_delivery_at = created_at + timedelta(minutes=total_minutes)

# Функция 4. Отслеживание статуса заказа 
if not is_working_time:
    order_status = "отменён: сервис не работает в это время"
elif not courier_assigned:
    order_status = "ожидает свободного курьера"
else:
    order_status = "передан курьеру, в пути к клиенту"

# Функция 5. Формирование квитанции 
# Трек-номер: дата заказа + номер заказа
tracking_number = "DLV-" + created_at.strftime("%Y%m%d") + "-" + str(order_number)
payment_method = "онлайн-оплата" if payment_is_online else "наличные курьеру"

print("=== Квитанция по заказу ===")
print("Трек-номер:            " + tracking_number)
print("Клиент:                " + client_name + ", " + client_phone)
print("Зона доставки:         " + zone_name + " (" + str(distance_km) + " км)")
print("Вес заказа:            " + str(weight) + " кг")
print("Курьер:                " + courier_name + " (" + courier_type + ")")
print("Сумма товаров:         " + str(round(goods_sum, 2)) + " руб.")

if delivery_is_free:
    print("Доставка:              бесплатно (заказ от " + str(FREE_DELIVERY_FROM) + " руб.)")
else:
    print("Доставка:              " + str(round(delivery_cost, 2)) + " руб.")
    if weight_surcharge > 0.0:
        print("  в т.ч. надбавка за вес: " + str(round(weight_surcharge, 2)) + " руб.")

print("Итого к оплате:        " + str(round(total_to_pay, 2)) + " руб. (" + payment_method + ")")
print("Заказ создан:          " + created_at.strftime("%d.%m.%Y %H:%M"))
print("Плановая доставка:     " + planned_delivery_at.strftime("%d.%m.%Y %H:%M")
      + " (через " + str(total_minutes) + " мин)")
print("Статус заказа:         " + order_status)
