from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

import poetry_version

__version__ = poetry_version.extract(source_file=__file__)


def run_turing_machine(
    machine: Dict,
    input_: str,
    steps: Optional[int] = None,
) -> Tuple[str, List, bool]:
    blank = machine['blank']
    start_state = machine['start state']
    final_states = set(machine['final states'])
    table = machine['table']
    
    # La bande initialisée avec l'input
    tape = list(input_)
    position = 0
    current_state = start_state
    
    # Historique d'exécution
    history = []
    
    # Nombre de pas exécutés
    step_count = 0
    
    # Fonction pour ajouter une étape à l'historique
    def add_to_history(state, reading, position, memory, transition):
        history.append({
            'state': state,
            'reading': reading,
            'position': position,
            'memory': ''.join(memory),
            'transition': transition
        })
    
    while True:
        # Lire le symbole actuel
        if position < 0 or position >= len(tape):
            reading = blank
        else:
            reading = tape[position]
        
        # Ajouter l'état actuel à l'historique
        add_to_history(current_state, reading, position, tape.copy(), table.get(current_state, {}).get(reading, {}))
        
        # Vérifier si l'état actuel est final
        if current_state in final_states:
            return ''.join(tape).strip(blank), history, True
        
        # Obtenir la transition correspondante
        transitions = table.get(current_state, {})
        if reading not in transitions:
            # Pas de transition disponible, machine bloquée
            return ''.join(tape).strip(blank), history, False
        
        transition = transitions[reading]
        
        # Appliquer la transition
        if isinstance(transition, str):
            # Transition simple (R ou L)
            if transition == 'R':
                position += 1
            elif transition == 'L':
                position -= 1
        else:
            # Transition complexe (écrire, déplacer, changer d'état)
            if 'write' in transition:
                if position < 0:
                    tape.insert(0, transition['write'])
                    position = 0
                elif position >= len(tape):
                    tape.append(transition['write'])
                else:
                    tape[position] = transition['write']
            
            if 'R' in transition:
                current_state = transition['R']
                position += 1
            elif 'L' in transition:
                current_state = transition['L']
                position -= 1
        
        # Incrémenter le compteur de pas
        step_count += 1
        if steps is not None and step_count >= steps:
            return ''.join(tape).strip(blank), history, False