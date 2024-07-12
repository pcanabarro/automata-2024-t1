"""Implementação de autômatos finitos."""


def load_automata(filename):
    """
    Lê os dados de um autômato finito a partir de um arquivo.

    A estrutura do arquivo deve ser:

    <lista de símbolos do alfabeto, separados por espaço (' ')>
    <lista de nomes de estados>
    <lista de nomes de estados finais>
    <nome do estado inicial>
    <lista de regras de transição, com "origem símbolo destino">

    Um exemplo de arquivo válido é:

    ```
    a b
    q0 q1 q2 q3
    q0 q3
    q0
    q0 a q1
    q0 b q2
    q1 a q0
    q1 b q3
    q2 a q3
    q2 b q0
    q3 a q1
    q3 b q2
    ```

    Caso o arquivo seja inválido uma exceção Exception é gerada.

    """
    with open(filename, "rt", encoding="utf-8") as file:
        lines = file.readlines()

    # Validação e extração dos dados do arquivo
    try:
        sigma = lines[0].strip().split()
        states = lines[1].strip().split()
        final_states = lines[2].strip().split()
        initial_state = lines[3].strip()

        # Verifica se os estados inicial e finais estão na lista de estados
        if initial_state not in states or any(f not in
                                              states for f in final_states):
            raise TypeError("Estado inicial ou estado final inválido.")

        delta = {}
        for line in lines[4:]:
            origin, symbol, destination = line.strip().split()
            if origin not in states or (destination
                                        not in states) or (symbol
                                                           not in sigma):
                raise ValueError("Transição inválida.")
            delta.setdefault(origin, {})[symbol] = destination

        # Retorna a estrutura do autômato
        return states, sigma, delta, initial_state, final_states

    except ValueError as e:
        raise ValueError("Formato inválido do arquivo de autômato.") from e
    except Exception as e:
        raise print("Erro Inesperado") from e


def process(automaton, words):
    """
    Process the words list using automaton param and return the result.

    :param automaton: Tuple (Q, Sigma, delta, q0, F)
    :param words: Words list to be processed
    :return: Dict associating each word with result
    """
    __, sigma, delta, initial_state, final_states = automaton
    print(automaton)
    result = {}

    for word in words:
        current_state = initial_state
        valid = True

        for letter in word:
            if letter not in sigma:
                result[word] = 'INVALIDA'
                valid = False
                break
            current_state = delta.get(current_state, {}).get(letter, 'REJEITA')

        if valid:
            result[word] = 'ACEITA' if (current_state
                                        in final_states) else 'REJEITA'

    return result
