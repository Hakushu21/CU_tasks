import toml
import sys
import re

class ConfigTransformer:
    def __init__(self):
        pass
    
    def transform_value(self, value):
        """Преобразует значения в формат учебного конфигурационного языка."""
        if isinstance(value, int):
            return str(value)  # Числа остаются числами
        elif isinstance(value, list):
            # Для массива: (значение, значение, значение)
            return f"({', '.join(map(self.transform_value, value))})"
        elif isinstance(value, str):
            # Для строки возвращаем саму строку
            return value
        return str(value)

    def transform(self, toml_data):
        """Преобразует данные из TOML в формат учебного конфигурационного языка."""
        output_lines = []

        for section, values in toml_data.items():
            if isinstance(values, dict):
                # Перебираем все ключи и значения в секции
                for key, value in values.items():
                    # Пишем объявление константы
                    transformed_value = self.transform_value(value)
                    output_lines.append(f"var {key} := {transformed_value}")
            else:
                # Если это список или другое значение
                transformed_value = self.transform_value(values)
                output_lines.append(f"{section} := {transformed_value}")

        return "\n".join(output_lines)

    def process_input(self, input_text):
        """Обрабатывает входной текст TOML и преобразует его."""
        try:
            toml_data = toml.loads(input_text)
            return self.transform(toml_data)
        except toml.TomlDecodeError as e:
            print(f"Ошибка синтаксиса TOML: {e}")
            sys.exit(1)

def main():
    transformer = ConfigTransformer()
    
    # Чтение входных данных
    input_text = sys.stdin.read()
    
    # Преобразование
    result = transformer.process_input(input_text)
    
    # Вывод результата
    print(result)

if __name__ == "__main__":
    main()
