from flask import Flask, request, jsonify, Response, redirect
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Rota principal '/'
@app.route('/')
def home():
    # Redirecionar para o link do GitHub
    return redirect("https://github.com/ThiagoSousa81/Read-me-Apps/#readme", code=302)  

# Função para buscar dados do usuário no GitHub --- Não utilizada
def get_github_user_data(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Aqui você pode adicionar qualquer outro dado que deseje usar como "pontuação"
        # Por exemplo, estamos pegando os seguidores e o número de repositórios públicos
        score = data['followers'] + data['public_repos']  # Pontuação baseada em seguidores + repositórios públicos
        return {
            "username": username,
            "score": score,
            "followers": data['followers'],
            "public_repos": data['public_repos']
        }
    else:
        return None

# Função para buscar o conteúdo do SVG da API do GitHub Readme Stats
def get_github_svg(username):
    url = f"https://github-readme-stats.vercel.app/api?username={username}&show_icons=true&theme=transparent&locale=pt-br"
    response = requests.get(url)
    return response.text

# Função para extrair o valor final de stroke-dashoffset da animação CSS
def extract_stroke_dashoffset_from_svg(svg_content):
    soup = BeautifulSoup(svg_content, 'html.parser')
    
    # Encontrar a tag <style> onde a animação é definida
    style_tag = soup.find('style')
    if style_tag:
        # Extrair o conteúdo do CSS dentro da tag <style>
        css_content = style_tag.string
        
        # Buscar pelo padrão do keyframes 'rankAnimation'
        if 'rankAnimation' in css_content:
            # Encontrar a parte 'to' da animação que define o valor final de stroke-dashoffset
            to_value = None
            lines = css_content.split("\n")
            for line in lines:
                if 'to {' in line:
                    # A linha com 'to {' tem o valor final do stroke-dashoffset
                    next_line = lines[lines.index(line) + 1]
                    if 'stroke-dashoffset' in next_line:
                        # Extrair o valor final de stroke-dashoffset
                        to_value = float(next_line.split(':')[1].strip().replace(';', ''))
                        break
            return to_value
    return None


# Rota para obter a pontuação dos usuários via GET
@app.route('/github_scores', methods=['GET'])
def get_github_scores():
    usernames = request.args.get('usernames', '').split(',')
    
    if not usernames:
        return jsonify({"error": "No usernames provided"}), 400
    
    scores = []
    
    # Itera sobre os usernames e consulta a API do GitHub Readme Stats
    for username in usernames:
        svg_content = get_github_svg(username)
        stroke_dashoffset = extract_stroke_dashoffset_from_svg(svg_content)
        
        if stroke_dashoffset is not None:
            scores.append({
                "username": username,
                "stroke_dashoffset": stroke_dashoffset
            })
        else:
            scores.append({
                "username": username,
                "score": "Not found or unable to extract score"
            })
    
    # Ordena os usuários pelo valor de stroke-dashoffset (do menor para o maior)
    scores.sort(key=lambda x: x['stroke_dashoffset'] if isinstance(x['stroke_dashoffset'], (int, float)) else float('inf'))
    
    # Agora, com o valor de stroke-dashoffset, podemos retornar a pontuação classificada
    return jsonify(scores)



# Função para coletar as chaves da API
def get_keys():
    url = "https://ebs-csp.vercel.app/assimetric/generate?size=1024&raw=0"
    response = requests.get(url)
    return response.json()

# Função para dividir a chave em várias linhas
"""def split_key_into_lines(key, max_length=60):
    # Dividir a chave em partes de tamanho máximo definido
    lines = [key[i:i + max_length] for i in range(0, len(key), max_length)]
    return lines"""

def split_key_into_lines(key):
    """Divide a chave em várias linhas com base nas quebras de linha presentes no texto."""
    return key.split('\n')  # Divida a chave em linhas usando a quebra de linha '\n'

# Função para gerar o SVG
def generate_matrix_svg(private_key, public_key):
    # Escapar caracteres especiais para SVG
    private_key = private_key.replace('&', '&amp;').replace('"', '&quot;').replace("'", '&apos;').replace('<', '&lt;').replace('>', '&gt;')
    public_key = public_key.replace('&', '&amp;').replace('"', '&quot;').replace("'", '&apos;').replace('<', '&lt;').replace('>', '&gt;')

    # Dividir as chaves em linhas
    public_key_lines = split_key_into_lines(public_key)
    private_key_lines = split_key_into_lines(private_key)

    # Início do SVG
    svg = '''
<svg width="800" height="300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style type="text/css">
      .key-container {
        font-family: "Roboto Mono", monospace;
        font-size: 10px;
        fill: #00ff00;
      }
      .key-box {
        fill: #000000;
        stroke: #00ff00;
        stroke-width: 2;
        rx: 5;
        ry: 5;
      }
      .key-title {
        font-weight: 900;
        fill: #00ff00;
      }
      .key-content {
        font-weight: 400;
        fill: #00ff00;
      }
    </style>
  </defs>
  
  <!-- Caixa para a Chave Pública -->
  <rect x="10" y="10" width="370" height="230" class="key-box"/>
  <!-- Caixa para a Chave Privada -->
  <rect x="410" y="10" width="370" height="230" class="key-box"/>
  
  <!-- Título da chave pública -->
  <text x="20" y="30" class="key-container key-title">Chave Pública</text>
  <!-- Título da chave privada -->
  <text x="420" y="30" class="key-container key-title">Chave Privada</text>'''

    # Adicionar o conteúdo da chave pública
    y_position = 50  # Iniciar a posição Y
    svg += '<text x="20" y="' + str(y_position) + '" class="key-container key-content">'
    for line in public_key_lines:
        svg += f'<tspan x="20" dy="1.2em">{line}</tspan>'
    svg += '</text>'

    # Adicionar o conteúdo da chave privada
    y_position = 50  # Reiniciar a posição Y para a chave privada
    svg += '<text x="420" y="' + str(y_position) + '" class="key-container key-content">'
    for line in private_key_lines:
        svg += f'<tspan x="420" dy="1.2em">{line}</tspan>'

    svg += '<a href="https://csp.ebs-systems.epizy.com/" target="_blank"><text class="key-container key-content">Onde usar isso?</text></a>'
    svg += '</text>'

    # Fechar o SVG
    svg += '</svg>'

    return svg

# Rota para gerar as chaves
@app.route('/generate-keys', methods=['GET'])
def generate_keys():
    # Coletar as chaves
    keys = get_keys()
    if not keys or 'private_key' not in keys or 'public_key' not in keys:
        return 'Erro ao obter chaves da API.', 500

    private_key = keys['private_key']
    public_key = keys['public_key']

    # Gerar o SVG
    svg_output = generate_matrix_svg(private_key, public_key)

    # Exibir o SVG no navegador
    return Response(svg_output, mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(debug=True)
