from unidecode import unidecode
from rapidfuzz import fuzz

def normalizar(texto):
    """Remove acentos e coloca tudo em minúsculo"""
    if not texto:
        return ""
    return unidecode(texto.strip().lower())

def calcular_score(nome_input, cidade_input, uf_input, cliente):
    """
    Calcula a similaridade entre os dados de entrada e os dados do cliente JDE.
    Campos usados:
    - Nome: ABALPH, WWALPH, WWMLNM
    - Cidade: ALCTY1
    - UF: ALADDS
    """
    campos_nome = [cliente.get('ABALPH'), cliente.get('WWALPH'), cliente.get('WWMLNM')]
    nome_max_score = max([
        fuzz.partial_ratio(normalizar(nome_input), normalizar(nome))
        for nome in campos_nome if nome
    ], default=0)

    cidade_score = 100 if normalizar(cidade_input) == normalizar(cliente.get('ALCTY1')) else 0
    uf_score = 100 if normalizar(uf_input) == normalizar(cliente.get('ALADDS')) else 0

    score_total = round(nome_max_score * 0.7 + cidade_score * 0.2 + uf_score * 0.1, 2)
    return score_total
