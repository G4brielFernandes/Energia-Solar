import pdfplumber
import pandas as pd
import lista  


def equipamentos(placas, max_kwp):
    area = placas * 2.8
    if max_kwp > 75:
        conector = 20
    elif max_kwp > 30.3:
        conector = 16
    elif max_kwp > 18:
        conector = 8
    elif max_kwp > 6.8:
        conector = 6
    else:
        conector = 4
    return area, conector


with pdfplumber.open("Radiação_solar.pdf") as pdf:
    data = []
    for page in pdf.pages:
        table = page.extract_table()
        if table:
            data.extend(table[1:] if data else table)

df = pd.DataFrame(data, columns=["Município", "Global", "Com Correção", "Fator kWh/kWp"])
df["Município"] = df["Município"].str.strip()
cidades_disponiveis = sorted(df["Município"].unique())

# --- Buscar fator kWh/kWp por cidade ---
def buscar_kwp(cidade):
    resultado = df[df["Município"].str.lower() == cidade.lower()]
    if not resultado.empty:
        return resultado.iloc[0]["Fator kWh/kWp"]
    else:
        return None

# --- Calcular economia ---
def economia(x):
    mes = x * 0.95
    ano = mes * 12
    final = ano * 25
    return mes, ano, final

# --- Calcular expansão máxima ---
def pode_chegar(max_kwp, placas, cida, potencia_placas):
    while True:
        x = potencia_placas * placas
        if x > (max_kwp * 1000):
            placas -= 1
            x = potencia_placas * placas
            break
        placas += 1
    kwh = (x / 1000) * cida
    return kwh, placas

# --- Cálculo principal ---
def resultado(cida, kwh, potencia_placas):
    r = buscar_kwp(cida)
    if r is None:
        return None

    div = float(potencia_placas / 1000)
    kwp_cidade = r.replace(',', '.')
    int_cid = float(kwp_cidade)
    int_kwh = float(kwh)

    placas = ((int_kwh / int_cid) // div) + 1
    kwp = (placas * potencia_placas) / 1000

    mes, ano, final = economia(int_kwh)
    modelo, max_kwp = lista.inversor(kwp)
    chega_kwh, chegar_placas = pode_chegar(max_kwp, placas, int_cid, potencia_placas)
    area, conector = equipamentos(int(placas), max_kwp)

    return {
        'kwp': round(kwp, 2),
        'placas': int(placas),
        'economia_mes': round(mes, 2),
        'economia_ano': round(ano, 2),
        'economia_25anos': round(final, 2),
        'modelo_inversor': modelo,
        'max_inversor': max_kwp,
        'kwh_maximo': round(chega_kwh, 2),
        'placas_maximo': int(chegar_placas),
        'area': round(area, 2),
        'conector': conector,
        'cidade': cida  # <- chave adicionada para referência da cidade
    }

def resultado_personalizado(resultado_anterior, modelo_inversor, max_kwp_inversor):
    try:
        potencia_placas = (resultado_anterior['kwp'] * 1000) / resultado_anterior['placas']  # Wp por placa

        cidade = resultado_anterior.get('cidade', '')
        fator_kwp = buscar_kwp(cidade)
        if fator_kwp is None:
            return None
        fator_kwp = float(str(fator_kwp).replace(',', '.'))

        # Recalcular placas para maximizar até capacidade do inversor escolhido
        placas = 1
        while True:
            potencia_total_placas = potencia_placas * placas
            if potencia_total_placas > max_kwp_inversor * 1000:
                placas -= 1
                break
            placas += 1

        if placas < 1:
            placas = 1

        kwp = (placas * potencia_placas) / 1000

        mes, ano, final = economia(fator_kwp * kwp)
        area, conector = equipamentos(placas, max_kwp_inversor)

        return {
            'kwp': round(kwp, 2),
            'placas': int(placas),
            'economia_mes': round(mes, 2),
            'economia_ano': round(ano, 2),
            'economia_25anos': round(final, 2),
            'modelo_inversor': modelo_inversor,
            'max_inversor': max_kwp_inversor,
            'kwh_maximo': round(fator_kwp * kwp, 2),
            'placas_maximo': int(placas),
            'area': round(area, 2),
            'conector': conector,
            'cidade': cidade
        }
    except Exception as e:
        print("Erro no resultado_personalizado:", e)
        return None