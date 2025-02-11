# turing_machine.py
class TuringMachine:
    def __init__(self, config, iteration, A, B):
        """
        Inicializa la máquina con la configuración y la cinta.
        
        Parámetros:
          - config: diccionario con la configuración (cargado desde YAML).
          - iteration: cadena en unaria que representa el contador de iteraciones (n-2).
          - A: cadena en unaria que representa el segmento A (F(n-2)).
          - B: cadena en unaria que representa el segmento B (F(n-1)).
        """
        self.config = config
        self.state = config['machine']['start_state']
        self.accept_state = config['machine']['accept_state']
        self.blank = config['machine']['blank']
        self.iteration = iteration  
        self.A = A  
        self.B = B  
        self.head_position = 0  
        self.transitions = config['transitions']
        self.temp = None  

    def get_tape(self):
        """Devuelve la representación completa de la cinta."""
        return self.iteration + "#" + self.A + "#" + self.B

    def print_configuration(self):
        """Imprime la configuración actual: estado, posición de la cabeza y contenido de la cinta."""
        print(f"Estado: {self.state}, Cabeza: {self.head_position}, Cinta: {self.get_tape()}")

    def step(self):
        """Ejecuta un paso (transición) de la máquina según el estado actual."""
        if self.state not in self.transitions:
            print("No hay transición definida para este estado. Se detiene la máquina.")
            self.state = self.accept_state
            return
        
        trans = self.transitions[self.state]
        action = trans.get('action')
        if self.state == 'q_check':
            self.check_iteration(trans)
        elif self.state == 'q_add':
            self.add(trans)
        elif self.state == 'q_update':
            self.update(trans)
        else:
            print("Estado desconocido. Se detiene la máquina.")
            self.state = self.accept_state

    def check_iteration(self, trans):
        """
        Estado q_check: se verifica el segmento 'iteration'.
          - Si está vacío, se pasa al estado de aceptación.
          - Si no, se procede a q_add.
        """
        if self.iteration == "":
            self.state = trans.get('if_empty', self.accept_state)
        else:
            self.state = trans.get('if_not_empty', 'q_add')

    def add(self, trans):
        """
        Estado q_add: se “suman” A y B (concatenando las cadenas) para calcular el nuevo número de Fibonacci.
        Se guarda el valor anterior de B en temp para la actualización.
        """
        self.temp = self.B 
        self.B = self.A + self.B  
        self.state = trans.get('next_state', 'q_update')

    def update(self, trans):
        """
        Estado q_update: se actualiza la cinta:
          - A toma el valor antiguo de B (guardado en temp).
          - Se elimina un símbolo '1' del contador (segmento iteration) para decrementar la iteración.
        """
        self.A = self.temp
        if self.iteration != "":
            self.iteration = self.iteration[1:]  
        self.state = trans.get('next_state', 'q_check')

    def run(self):
        """Ejecuta la simulación completa mostrando cada configuración."""
        self.print_configuration()
        while self.state != self.accept_state:
            self.step()
            self.print_configuration()
        print("La máquina se ha detenido en el estado de aceptación.")
        return self.get_tape()
