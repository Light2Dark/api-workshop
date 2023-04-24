def get_state_symbol(state: str):
    states = {
        "Acre": "AC",
        "Amazonas": "AM",
        "Amapa": "AP",
        "Para": "PA",
        "Maranhao": "MA",
        "Rondonia": "RO",
        "Roraima": "RR",
        "Tocantins": "TO",
        "Mato Grosso": "MT"
    }
    
    return states.get(state, None)