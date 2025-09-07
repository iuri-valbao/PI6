from flask import Flask, render_template, request
import requests # Importe a biblioteca requests

app = Flask(__name__)

# --- Configure sua chave de API aqui ---
API_KEY = "01cff47d321d789bd5933fe3bfe1c7db"

# --- Funções para Requisições à API Real ---
def get_clima_real(localizacao):
    """
    Consulta a API OpenWeatherMap para obter dados de clima.
    Primeiro, converte o nome da cidade em coordenadas (geocoding).
    Depois, usa as coordenadas para buscar os dados de clima.
    """
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={localizacao}&limit=1&appid={API_KEY}"
    
    try:
        # Requisição para obter latitude e longitude
        response_geo = requests.get(geocoding_url)
        response_geo.raise_for_status() # Lança um erro para status de erro (4xx ou 5xx)
        geo_data = response_geo.json()

        if not geo_data:
            return {"error": "Localização não encontrada."}

        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']

        # Requisição para obter dados de clima com as coordenadas
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"
        
        response_weather = requests.get(weather_url)
        response_weather.raise_for_status()
        weather_data = response_weather.json()

        # Extrai os dados relevantes
        temperatura = weather_data['main']['temp']
        descricao_clima = weather_data['weather'][0]['description']
        umidade = weather_data['main']['humidity']
        
        return {
            "temperatura": f"{temperatura}°C",
            "pluviosidade": descricao_clima,
            "umidade": f"{umidade}%",
            "lat": lat,
            "lon": lon
        }

    except requests.exceptions.RequestException as e:
        # Trata erros de requisição, como problemas de conexão
        return {"error": f"Erro ao conectar com a API: {e}"}
    except Exception as e:
        # Trata outros erros
        return {"error": f"Ocorreu um erro: {e}"}

# --- Dados Mockados para sementes (mantemos por enquanto) ---
# A função get_variedades_sementes() continua a mesma por enquanto.
def get_variedades_sementes(cultura, condicoes_locais):
    """Simula a consulta a um banco de sementes e o cruzamento de dados."""
    # Código existente...
    recomendacoes = []

    # Exemplo simples de cruzamento de dados
    if "tomate" in cultura.lower():
        # Lógica agora mais real, baseada na temperatura da API
        temp_str = condicoes_locais.get('temperatura', '20°C')
        temp_celsius = float(temp_str.replace("°C", ""))
        
        if temp_celsius > 25:
            recomendacoes.append({
                "nome": "Tomate de Clima Quente",
                "detalhes": "Variedade resistente a altas temperaturas.",
                "irrigacao": "Frequente",
                "epoca": "Verão",
                "performance": "90% de taxa de sucesso"
            })
        elif 15 <= temp_celsius <= 25:
             recomendacoes.append({
                "nome": "Tomate Híbrido",
                "detalhes": "Ótima adaptação a solos diversos e temperaturas moderadas.",
                "irrigacao": "Moderada",
                "epoca": "Primavera/Outono",
                "performance": "95% de taxa de sucesso"
            })
        else:
            recomendacoes.append({
                "nome": "Tomate de Estufa",
                "detalhes": "Indicado para ambientes controlados.",
                "irrigacao": "Controlada",
                "epoca": "Qualquer época em estufa",
                "performance": "80% de taxa de sucesso"
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
    resultados = None
    if request.method == "POST":
        cultura = request.form.get("cultura")
        localizacao = request.form.get("localizacao")

        # --- Chamada para a nova função de API real ---
        condicoes_locais = get_clima_real(localizacao)
        
        # Se a API retornou um erro, passamos a mensagem para o template
        if 'error' in condicoes_locais:
            resultados = {"erro": condicoes_locais["error"]}
        else:
            recomendacoes = get_variedades_sementes(cultura, condicoes_locais)
            
            resultados = {
                "localizacao_pesquisada": localizacao,
                "cultura_pesquisada": cultura,
                "condicoes_locais": condicoes_locais,
                "recomendacoes": recomendacoes
            }

    return render_template("index.html", resultados=resultados)

if __name__ == "__main__":
    app.run(debug=True)
