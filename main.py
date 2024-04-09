from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'Bem-vindo à minha API que lista os 10 vídeos mais acessados Youtube! Para acessar os vídeos mais populares de um país específico, adicione o código do país à URL. Por exemplo: /api/top_videos/US'

@app.route('/api/top_videos/<country_code>')
def top_videos(country_code):
    API_KEY = "AIzaSyBTVkiKfBKoPkMhu7MSYEM6GYqwlPYuCGI"  # Substitua pela sua chave de API do YouTube

    # Faz uma solicitação GET à API do YouTube Data para obter os vídeos mais populares
    response = requests.get(
        f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode={country_code}&maxResults=10&key={API_KEY}"
    )

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Solicita informações sobre o país
        country_response = requests.get(
            f"https://restcountries.com/v3.1/alpha/{country_code}"
        )

        # Verifica se a solicitação para obter informações do país foi bem-sucedida
        if country_response.status_code == 200:
            country_name = country_response.json()[0]["name"]["common"]
        else:
            country_name = "País Desconhecido"

        # Lista para armazenar os dados dos vídeos
        videos_data = []

        # Itera pelos resultados da resposta
        for item in response.json()["items"]:
            video_title = item["snippet"]["title"]
            video_url = f"https://www.youtube.com/watch?v={item['id']}"
            view_count = int(item["statistics"]["viewCount"])
            videos_data.append({
                "title": video_title,
                "viewCount": view_count,
                "url": video_url
            })

        # Ordena os vídeos por número de visualizações em ordem decrescente
        videos_data.sort(key=lambda x: x["viewCount"], reverse=True)

        # Formata os dados em JSON
        data = {
            "country": country_name,
            "top_videos": videos_data
        }

        return jsonify(data)

    else:
        return jsonify({"error": "Falha na solicitação à API do YouTube Data."})

if __name__ == '__main__':
    app.run(debug=True)
