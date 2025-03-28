from flask import Flask, request, jsonify, Response, redirect
from bs4 import BeautifulSoup
import requests
from lxml import etree

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


# Função para combinar os SVGs dos usuários em um único SVG
def combine_svgs(usernames):
    # Cria a estrutura base de SVG
    combined_svg = etree.Element("svg", xmlns="http://www.w3.org/2000/svg", width="500", height="500", viewBox="0 0 500 500")
    
    x_offset = 0  # Variável para controlar a posição horizontal
    y_offset = 0  # Variável para controlar a posição vertical

    for username in usernames:
        svg_content = get_github_svg(username)

        # Usar lxml para parsear o conteúdo SVG
        try:
            svg_tree = etree.fromstring(svg_content)
            
            # Iterar sobre os elementos dentro do SVG e adicionar ao SVG combinado
            for elem in svg_tree.iter():
                if isinstance(elem.tag, str):
                    # Ignorar a tag <svg> e adicionar os outros elementos gráficos
                    if elem.tag != "svg":
                        # Ajuste as coordenadas (x e y) de cada elemento para o posicionamento desejado
                        elem.set("x", str(x_offset))
                        elem.set("y", str(y_offset))
                        combined_svg.append(elem)

            # Ajuste o x_offset e y_offset para o próximo SVG (apenas para exemplificação)
            x_offset += 150  # Incrementa para a próxima posição horizontal
            if x_offset > 400:  # Se ultrapassar a largura, reseta para nova linha
                x_offset = 0
                y_offset += 150  # Avança para baixo

        except Exception as e:
            print(f"Erro ao processar o SVG de {username}: {e}")

    # Retorna o SVG combinado
    return etree.tostring(combined_svg, pretty_print=True).decode()

# Rota para gerar um SVG combinado com os usuários
@app.route('/combined_svg', methods=['GET'])
def get_combined_svg():
    usernames = request.args.get('usernames', '').split(',')
    
    if not usernames:
        return jsonify({"error": "No usernames provided"}), 400
    
    # Combina os SVGs de todos os usuários
    combined_svg = combine_svgs(usernames)

    # Retorna o SVG combinado como resposta
    return Response(combined_svg, mimetype="image/svg+xml")


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
