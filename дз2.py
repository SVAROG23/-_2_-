import pandas as pd
import numpy as np
import os

# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (Структурирование приложения)

def load_data(file_path_xlsx='Coffee Shop Sales.xlsx', file_path_csv='Coffee Shop Sales.csv'):
    """Чтение данных с обработкой ошибок (EAFP подход)"""
    print("=" * 60)
    print("ПУНКТ 1. ЧТЕНИЕ ДАННЫХ")
    print("=" * 60)
    
    try:
        if os.path.exists(file_path_xlsx):
            df = pd.read_excel(file_path_xlsx, sheet_name='Transactions')
            print(f"Данные загружены из {file_path_xlsx}")
        elif os.path.exists(file_path_csv):
            df = pd.read_csv(file_path_csv)
            print(f"Данные загружены из {file_path_csv}")
        else:
            raise FileNotFoundError("Файл с данными не найден в папке с проектом.")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

    # Проверка на наличие нужных столбцов
    required_columns = [
        'transaction_id', 'transaction_date', 'transaction_time',
        'transaction_qty', 'store_id', 'store_location', 'product_id',
        'unit_price', 'product_category', 'product_type', 'product_detail'
    ]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        print(f"ОШИБКА: В данных отсутствуют столбцы: {missing}")
        return None

    print("\n--- Первые 5 строк ---")
    print(df.head())
    print("\n--- Общая информация ---")
    df.info()
    print("\n--- Базовая статистика ---")
    print(df.describe())
    
    print(f"\nВЫВОД: Загружено {len(df)} строк и {len(df.columns)} столбцов.")
    print(f"Пропущенных значений: {df.isnull().sum().sum()}")
    return df


def filter_data(df, threshold=3.0, category='Coffee'):
    """Фильтрация данных по цене и категории"""
    print("\n" + "=" * 60)
    print("ПУНКТ 2. ФИЛЬТРАЦИЯ")
    print("=" * 60)
    
    # Проверка категории (LBYL)
    available_categories = df['product_category'].unique()
    if category not in available_categories:
        print(f"Категория '{category}' не найдена. Доступные: {list(available_categories)}")
        category = available_categories[0]
        print(f"Используем категорию по умолчанию: '{category}'")

    filtered = df[(df['unit_price'] > threshold) & (df['product_category'] == category)]
    
    print(f"Порог цены: {threshold}, Категория: {category}")
    print(f"Количество строк после фильтрации: {len(filtered)}")
    print("\n--- Первые 5 строк после фильтрации ---")
    print(filtered.head())
    
    print(f"\nВЫВОД: После фильтрации осталось {len(filtered)} строк.")
    return filtered


def group_and_aggregate(df):
    """Группировка и агрегация"""
    print("\n" + "=" * 60)
    print("ПУНКТ 3. ГРУППИРОВКА И АГРЕГАЦИЯ")
    print("=" * 60)
    
    grouped = df.groupby('product_category').agg(
        transaction_count=('transaction_id', 'count'),
        avg_price=('unit_price', 'mean'),
        total_qty=('transaction_qty', 'sum'),
        max_price=('unit_price', 'max')
    ).sort_values('avg_price', ascending=False)

    print(grouped.to_string())
    top_category = grouped.index[0]
    print(f"\nВЫВОД: Самая высокая средняя цена у категории '{top_category}' "
          f"({grouped.loc[top_category, 'avg_price']:.2f}).")
    return top_category


def add_price_level(df):
    """Добавление нового столбца"""
    print("\n" + "=" * 60)
    print("ПУНКТ 4. НОВЫЙ СТОЛБЕЦ price_level")
    print("=" * 60)
    
    avg_price_all = df['unit_price'].mean()
    print(f"Средняя цена по всей таблице: {avg_price_all:.2f}")

    df['price_level'] = np.where(
        df['unit_price'] > avg_price_all,
        'выше среднего',
        'ниже или равно'
    )

    print("\n--- Первые 5 строк с новым столбцом ---")
    print(df[['unit_price', 'price_level']].head())
    
    above = (df['price_level'] == 'выше среднего').sum()
    below = (df['price_level'] == 'ниже или равно').sum()
    print(f"\nВЫВОД: 'выше среднего' — {above} строк, 'ниже или равно' — {below} строк.")
    return df


def numpy_analysis(df):
    """Расчеты через NumPy и нормализация"""
    print("\n" + "=" * 60)
    print("ПУНКТ 5. ИСПОЛЬЗОВАНИЕ NUMPY")
    print("=" * 60)
    
    prices = df['unit_price'].to_numpy()
    print(f"Среднее: {prices.mean():.2f}")
    print(f"Стандартное отклонение: {prices.std():.2f}")
    print(f"Максимум: {prices.max():.2f}")
    print(f"Минимум: {prices.min():.2f}")

    normalized = (prices - prices.min()) / (prices.max() - prices.min())
    print("\nПервые 5 нормализованных значений:")
    print(normalized[:5])
    print(f"\nВЫВОД: Нормализация выполнена. Диапазон значений — от 0 до 1.")


def save_data(df, filename='processed_coffee.csv'):
    """Сохранение обработанного DataFrame"""
    print("\n" + "=" * 60)
    print("ПУНКТ 6. СОХРАНЕНИЕ")
    print("=" * 60)
    
    try:
        df.to_csv(filename, index=False)
        print(f"Файл {filename} успешно сохранён.")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")


# ГЛАВНАЯ ФУНКЦИЯ (Точка входа)

def main():
    # 1. Чтение
    df = load_data()
    if df is None:
        return  # Прерываем выполнение, если данные не загрузились
    
    # 2. Фильтрация
    filtered = filter_data(df)
    
    # 3. Группировка
    top_category = group_and_aggregate(df)
    
    # 4. Новый столбец
    df = add_price_level(df)
    
    # 5. NumPy
    numpy_analysis(df)
    
    # 6. Сохранение
    save_data(df)
    
    # ОТВЕТЫ НА ВОПРОСЫ
    print("\n" + "=" * 60)
    print("ОТВЕТЫ НА ВОПРОСЫ")
    print("=" * 60)
    print(f"1. Сколько строк осталось после фильтрации: {len(filtered)}")
    print(f"2. Какая категория имеет самую высокую среднюю цену: {top_category}")

if __name__ == "__main__":
    main()