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
        if args.input.isdigit():  
            n = int(args.input)
            unary_input = "1" * n
        else: 
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
        result = result_tape.split("#")[2]
        print("Resultado (Fibonacci(n) en representación unaria):", result)
        print("Fibonacci(n) =", len(result))
        
if __name__ == "__main__":
    main()
