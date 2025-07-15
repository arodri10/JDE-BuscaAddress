from flask import Flask, request, jsonify
import cx_Oracle
from config import ORACLE_CONFIG
from util import calcular_score

app = Flask(__name__)

@app.route('/api/jde/clientes-proximos', methods=['POST'])
def clientes_proximos():
    data = request.json
    nome = data.get("nome")
    cidade = data.get("cidade")
    uf = data.get("uf")

    if not all([nome, cidade, uf]):
        return jsonify({"erro": "nome, cidade e uf são obrigatórios"}), 400

    try:
        conn = cx_Oracle.connect(**ORACLE_CONFIG)
        cursor = conn.cursor()
        query = '''
            SELECT ABAN8, ABALPH, ABSIC, WWMLNM, WWALPH, ALCTY1, ALADDS, ALCTR
            FROM Proddta.F0101
            INNER JOIN Proddta.F0116 ON ALAN8 = ABAN8
            LEFT OUTER JOIN Proddta.F0111 ON WWAN8 = ABAN8
            WHERE ABSIC IN ('0010', '0011') AND ALCTR = 'BR'
        '''
        cursor.execute(query)
        col_names = [col[0] for col in cursor.description]
        resultados = []

        for row in cursor.fetchall():
            cliente = dict(zip(col_names, row))
            score = calcular_score(nome, cidade, uf, cliente)
            if score >= 60:
                cliente['score'] = score
                resultados.append(cliente)

        resultados.sort(key=lambda c: c['score'], reverse=True)
        return jsonify(resultados[:10])

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

if __name__ == '__main__':
    app.run(debug=True)
