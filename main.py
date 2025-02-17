import argparse
from config_loader import load_config
from turing_machine import TuringMachine

def main():
    parser = argparse.ArgumentParser(description="Simulación de Máquina de Turing para la Sucesión de Fibonacci")
    parser.add_argument("--config", type=str, default="config.yaml", help="Ruta del archivo de configuración YAML")
    parser.add_argument("--input", type=str, help="Cadena de entrada en notación unaria (por ejemplo, '111' para n=3)")
    parser.add_argument("--analyze", action="store_true", help="Realizar análisis empírico")
    args = parser.parse_args()
    
    config = load_config(args.config)
    
    if args.analyze:
        from analyzer import empirical_analysis
        empirical_analysis(config)
    else:
        if args.input is None:
            args.input = input("Ingrese la cadena de entrada (en unaria, por ejemplo, '111' para n=3): ")
        n = len(args.input)
        if n < 1:
            print("n debe ser al menos 1.")
            return
        # Configurar la cinta:
        # Para n<=2 (F(1)=1, F(2)=1) no hay iteración; para n>=3 se realizan n-2 iteraciones.
        if args.input.isdigit():  # Si el usuario ingresa un número en decimal (ej. "5")
            n = int(args.input)
            unary_input = "1" * n
        else:  # Si ya está en notación unaria
            unary_input = args.input
            n = len(unary_input)

        if n <= 2:
            iteration = ""
        else:
            iteration = "1" * (n - 2)

        A = "1"
        B = "1"
        
        tm = TuringMachine(config, iteration, A, B)
        print("Configuración inicial:")
        tm.print_configuration()
        print("Ejecutando la simulación...")
        tm.run()
        result_tape = tm.get_tape()
        # El resultado final se encuentra en el tercer segmento (B)
        result = result_tape.split("#")[2]
        print("Resultado (Fibonacci(n) en representación unaria):", result)
        print("Fibonacci(n) =", len(result))
        
if __name__ == "__main__":
    main()
