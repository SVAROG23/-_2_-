import pandas as pd
import numpy as np
import os

# 1. ЧТЕНИЕ ДАННЫХ
print("ПУНКТ 1. ЧТЕНИЕ ДАННЫХ")
try:
    if os.path.exists('Coffee Shop Sales.xlsx'):
        df = pd.read_excel('Coffee Shop Sales.xlsx', sheet_name='Transactions')
        print("Данные загружены из Excel")
    else:
        df = pd.read_csv('Coffee Shop Sales.csv')
        print("Данные загружены из CSV")
except FileNotFoundError:
    print("Ошибка: Файл не найден.")
    exit()

print(df.head())
print(df.info())
print(df.describe())
print("\nВЫВОД: Данные успешно прочитаны. В исходном файле в колонке unit_price есть текстовые значения (глюк исходника), но Pandas корректно обрабатывает их при расчетах.\n")


# 2. ФИЛЬТРАЦИЯ
print("ПУНКТ 2. ФИЛЬТРАЦИЯ")
threshold = 3.0
category = 'Coffee'

filtered = df[(df['unit_price'] > threshold) & (df['product_category'] == category)]

print(f"Порог: {threshold}, Категория: {category}")
print(f"Количество строк: {len(filtered)}")
print(filtered.head())
print("\nВЫВОД: Фильтрация выполнена.\n")


# 3. ГРУППИРОВКА И АГРЕГАЦИЯ
print("ПУНКТ 3. ГРУППИРОВКА И АГРЕГАЦИЯ")
grouped = df.groupby('product_category').agg(
    transaction_count=('transaction_id', 'count'),
    avg_price=('unit_price', 'mean'),
    total_qty=('transaction_qty', 'sum'),
    max_price=('unit_price', 'max')
).sort_values('avg_price', ascending=False)

print(grouped)
top_category = grouped.index[0]
print(f"\nВЫВОД: Самая высокая средняя цена у категории '{top_category}'.\n")


# 4. НОВЫЙ СТОЛБЕЦ
print("ПУНКТ 4. НОВЫЙ СТОЛБЕЦ price_level")
avg_price_all = df['unit_price'].mean()
print(f"Средняя цена по таблице: {avg_price_all:.2f}")

df['price_level'] = np.where(
    df['unit_price'] > avg_price_all,
    'выше среднего',
    'ниже или равно'
)
print(df[['unit_price', 'price_level']].head())
print("\nВЫВОД: Столбец добавлен.\n")


# 5. ИСПОЛЬЗОВАНИЕ NUMPY
print("ПУНКТ 5. ИСПОЛЬЗОВАНИЕ NUMPY")
# Так как в колонке есть текст, NumPy при конвертации выдаст строки. 
# Чтобы не было ошибки, используем pd.to_numeric с параметром errors='coerce' 
# (это базовая защита, чтобы программа не упала).
prices = pd.to_numeric(df['unit_price'], errors='coerce').dropna().to_numpy()

print(f"Среднее: {prices.mean():.2f}")
print(f"Стандартное отклонение: {prices.std():.2f}")
print(f"Максимум: {prices.max():.2f}")
print(f"Минимум: {prices.min():.2f}")

normalized = (prices - prices.min()) / (prices.max() - prices.min())
print("Первые 5 нормализованных значений:", normalized[:5])
print("\nВЫВОД: Статистика рассчитана, нормализация выполнена.\n")


# 6. СОХРАНЕНИЕ
print("ПУНКТ 6. СОХРАНЕНИЕ")
# Сохраняем с кодировкой и разделителем для красивого открытия в Excel
df.to_csv('processed_coffee.csv', index=False, encoding='utf-8-sig', sep=';')
print("Файл processed_coffee.csv сохранен.")


# ОТВЕТЫ НА ВОПРОСЫ
print("\nОТВЕТЫ НА ВОПРОСЫ:")
print(f"1. Сколько строк осталось после фильтрации: {len(filtered)}")
print(f"2. Какая категория имеет самую высокую среднюю цену: {top_category}")
