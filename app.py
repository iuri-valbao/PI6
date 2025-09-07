from flask import Flask, render_template, request

app = Flask(__name__)

# --- Dados Mockados (Simulados) ---
# Substitua esta parte pela chamada a APIs e bancos de dados reais
def get_clima(localizacao):
    """Simula a consulta a uma API de clima."""
    # Retorna dados simulados baseados na localização
    if "São Paulo" in localizacao.lower():
        return {"temperatura": "25°C", "pluviosidade": "baixa", "solo": "argiloso"}
    elif "Curitiba" in localizacao.lower():
        return {"temperatura": "18°C", "pluviosidade": "moderada", "solo": "ácido"}
    else:
        return {"temperatura": "22°C", "pluviosidade": "variavel", "solo": "neutro"}

def get_variedades_sementes(cultura, condicoes_locais):
    """Simula a consulta a um banco de sementes e o cruzamento de dados."""
    recomendacoes = []

    # Exemplo simples de cruzamento de dados
    if "tomate" in cultura.lower():
        if "argiloso" in condicoes_locais["solo"]:
            recomendacoes.append({
                "nome": "Tomate Caqui",
                "detalhes": "Ótima adaptação a solos argilosos. Alta produtividade.",
                "irrigacao": "Moderada (2-3 vezes por semana)",
                "epoca": "Primavera/Verão",
                "performance": "90% de taxa de sucesso"
            })
        if "ácido" in condicoes_locais["solo"]:
            recomendacoes.append({
                "nome": "Tomate Cereja",
                "detalhes": "Tolerante a solos mais ácidos. Ideal para climas amenos.",
                "irrigacao": "Baixa (1-2 vezes por semana)",
                "epoca": "Todo o ano",
                "performance": "85% de taxa de sucesso"
            })
    
    if not recomendacoes:
        recomendacoes.append({
            "nome": "Nenhuma variedade encontrada",
            "detalhes": "Nossos dados não retornaram uma recomendação para sua região.",
            "irrigacao": "-",
            "epoca": "-",
            "performance": "-"
        })

    return recomendacoes

# --- Rotas da Aplicação ---
@app.route("/", methods=["GET", "POST"])
def index():
    # Inicializa a variável de resultados
    resultados = None
    
    # Se a requisição for do tipo POST (formulário enviado)
    if request.method == "POST":
        cultura = request.form.get("cultura")
        localizacao = request.form.get("localizacao")

        # --- Lógica do Processamento ---
        # 1. Coleta os dados da localização (simulado)
        condicoes_locais = get_clima(localizacao)
        
        # 2. Coleta e cruza os dados de sementes (simulado)
        recomendacoes = get_variedades_sementes(cultura, condicoes_locais)
        
        # 3. Armazena os resultados para passar para o template
        resultados = {
            "localizacao_pesquisada": localizacao,
            "cultura_pesquisada": cultura,
            "condicoes_locais": condicoes_locais,
            "recomendacoes": recomendacoes
        }

    # Renderiza o template, passando os resultados (se houver)
    return render_template("index.html", resultados=resultados)

if __name__ == "__main__":
    app.run(debug=True)