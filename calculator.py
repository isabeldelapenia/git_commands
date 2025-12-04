from typing import Callable, List, Dict, Optional


def show_banner() -> None:
    print("=" * 55)
    print("   Soporta uso de 'ans' como último resultado.")
    print("=" * 55)


def read_number(prompt: str, last_result: Optional[float]) -> float:
    while True:
        raw_value = input(prompt).strip()

        # Permitir usar el último resultado
        if raw_value.lower() == "ans":
            if last_result is None:
                print("⚠ No hay resultado previo disponible todavía.")
                continue
            return last_result

        try:
            number = float(raw_value.replace(",", "."))
            return number
        except ValueError:
            print("⚠ Entrada inválida. Escriba un número válido o 'ans'.")


def choose_operation(available_ops: Dict[str, Callable[[float, float], float]]) -> str:
    """
    Muestra el menú de operaciones y devuelve la opción elegida.
    """
    print("\n--- MENÚ DE OPERACIONES ---")
    print(" +  → Suma")
    print(" -  → Resta")
    print(" *  → Multiplicación")
    print(" /  → División")
    print(" ^  → Potencia")
    print(" r  → Raíz (n-ésima raíz)")
    print(" h  → Ver historial")
    print(" c  → Limpiar historial")
    print(" q  → Salir")
    print("----------------------------")

    while True:
        op = input("Seleccione una opción: ").strip().lower()
        if op in available_ops or op in {"h", "q", "c", "r"}:
            return op
        print("⚠ Opción no válida. Intente de nuevo.")


def operation_add(a: float, b: float) -> float:
    """Realiza una suma."""
    return a + b


def operation_subtract(a: float, b: float) -> float:
    """Realiza una resta."""
    return a - b


def operation_multiply(a: float, b: float) -> float:
    """Realiza una multiplicación."""
    return a * b


def operation_divide(a: float, b: float) -> float:
    """Realiza una división, manejando división por cero."""
    if b == 0:
        raise ZeroDivisionError("No es posible dividir entre cero.")
    return a / b


def operation_power(a: float, b: float) -> float:
    """Realiza una potencia (a elevado a b)."""
    return a ** b


def operation_root(base: float, index: float) -> float:
    """Calcula la raíz n-ésima de un número."""
    if index == 0:
        raise ZeroDivisionError("El índice de la raíz no puede ser cero.")
    # Raíz n-ésima: base ** (1 / n)
    return base ** (1.0 / index)


def show_history(history: List[Dict[str, str]]) -> None:
    """Muestra el historial de operaciones."""
    if not history:
        print("\n🗒 Historial vacío todavía.")
        return

    print("\n🗒 HISTORIAL DE OPERACIONES:")
    for idx, item in enumerate(history, start=1):
        print(f"{idx}. {item['expression']} = {item['result']}")


def clear_history(history: List[Dict[str, str]]) -> None:
    """Limpia el historial de operaciones."""
    history.clear()
    print("🧹 Historial limpiado.")


def main() -> None:
    """Función principal de la calculadora."""
    operations = {
        "+": operation_add,
        "-": operation_subtract,
        "*": operation_multiply,
        "/": operation_divide,
        "^": operation_power,
    }

    history: List[Dict[str, str]] = []
    last_result: Optional[float] = None

    show_banner()

    while True:
        op = choose_operation(operations)

        if op == "q":
            print("\n👋 Saliendo de la calculadora. ¡Hasta luego!")
            break

        if op == "h":
            show_history(history)
            continue

        if op == "c":
            clear_history(history)
            continue

        # Operación especial de raíz
        if op == "r":
            print("\n--- CÁLCULO DE RAÍZ N-ÉSIMA ---")
            base = read_number("Ingrese el número (o 'ans'): ", last_result)
            index = read_number("Ingrese el índice de la raíz (por ejemplo, 2 para raíz cuadrada): ", last_result)

            try:
                result = operation_root(base, index)
                expression = f"raíz {index} de {base}"
                print(f"Resultado: {result}")
                history.append({"expression": expression, "result": str(result)})
                last_result = result
            except Exception as ex:
                print(f"⚠ Se produjo un error al calcular la raíz: {ex}")
            continue

        # Operaciones binarias estándar
        print("\n--- OPERACIÓN BINARIA ---")
        left = read_number("Ingrese el primer número (o 'ans'): ", last_result)
        right = read_number("Ingrese el segundo número (o 'ans'): ", last_result)

        operation_func = operations[op]
        symbol = op

        try:
            result = operation_func(left, right)
            expression = f"{left} {symbol} {right}"
            print(f"Resultado: {result}")
            history.append({"expression": expression, "result": str(result)})
            last_result = result
        except Exception as ex:
            print(f"⚠ Se produjo un error al realizar la operación: {ex}")


if __name__ == "__main__":
    main()
