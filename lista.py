inversores = [
    {"modelo": "3k Saj", "kwp": 4.5},
    {"modelo": "4k Saj", "kwp": 6.0},
    {"modelo": "5k  Saj", "kwp": 7.5},
    {"modelo": "6k Saj", "kwp": 9.0},
    {"modelo": "6k Solis", "kwp": 10.8},
    {"modelo": "8k Sungrow", "kwp": 12.0},
    {"modelo": "8k Saj", "kwp": 12.5},
    {"modelo": "10k Sungrow", "kwp": 15.0},
    {"modelo": "10k Saj", "kwp": 15.5},
    {"modelo": "15k Saj", "kwp": 22.5},
    {"modelo": "20k Saj", "kwp": 30.0},
    {"modelo": "30k Sungrow", "kwp": 45.0},
    {"modelo": "50k Sungrow", "kwp": 75.3},
]

def inversor(kwp: float):
    for inversor in inversores:
        if inversor["kwp"] >= kwp:
            modelo = inversor["modelo"]
            max_kwp = inversor["kwp"]
            return modelo , max_kwp
        

if __name__ == '__main__':

    modelo , max_kwp = inversor(5.3)
    print(modelo)
    print(max_kwp)