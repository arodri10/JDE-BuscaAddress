# 🔎 API de Busca Inteligente de Clientes (JDE E1)

Esta API realiza buscas fonéticas e por localização (UF/Cidade) em clientes cadastrados no **JD Edwards EnterpriseOne**, mesmo que o nome esteja escrito de forma diferente do informado.

---

## ⚙️ Tecnologias

- Python 3.10+
- Flask
- cx_Oracle (integração com banco Oracle JDE E1)
- RapidFuzz (similaridade textual)
- Unidecode (normalização de acentos)

---

## 📁 Estrutura do Projeto

```
.
├── main.py               # API Flask principal
├── util.py               # Funções de normalização e cálculo de similaridade
├── config.py             # Configuração de conexão com Oracle
├── requirements.txt      # Bibliotecas Python
└── README.md             # Este arquivo
```

---

## 🐍 Como rodar localmente

### 1. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure o acesso Oracle
Edite o arquivo `config.py` com seu usuário, senha e conexão:
```python
ORACLE_CONFIG = {
    "user": "JDE_USER",
    "password": "SENHA",
    "dsn": "host:porta/sid"
}
```

> 💡 A conexão pode exigir o Oracle Instant Client instalado. Veja: https://cx-oracle.readthedocs.io/en/latest/installation.html

---

## ▶️ Executando a API

```bash
python main.py
```

A API estará acessível em:  
`http://localhost:5000/api/jde/clientes-proximos`

---

## 🔁 Exemplo de requisição

**POST** `/api/jde/clientes-proximos`

```json
{
  "nome": "João Batista Transportes",
  "cidade": "Campinas",
  "uf": "SP"
}
```

---

## ✅ Resposta esperada
```json
[
  {
    "ABAN8": 123456,
    "ABALPH": "JOAO BATISTA TRANSP",
    "WWMLNM": null,
    "WWALPH": null,
    "ALCTY1": "Campinas",
    "ALADDS": "SP",
    "ALCTR": "BR",
    "score": 87.5
  }
]
```

## ✅ Para testar pelo DOS
```json
curl -X POST http://localhost:5000/api/jde/clientes-proximos -H "Content-Type: application/json" -d "{\"nome\":\"Andre\", \"cidade\":\"São Paulo\", \"uf\":\"SP\"}"
```


---

## 📌 Regras de Similaridade

- **Nome** tem peso de 70% (usa `fuzz.partial_ratio`)
- **Cidade** tem peso de 20%
- **UF** tem peso de 10%
- Resultados abaixo de `60` de score são ignorados

---

## 📬 Contato

Para dúvidas ou melhorias, entre em contato com o responsável pelo projeto.
