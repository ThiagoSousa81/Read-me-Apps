from flask import Flask, Response, redirect
import requests

app = Flask(__name__)

# Rota principal '/'
@app.route('/')
def home():
    # Redirecionar para o link do GitHub
    return redirect("https://github.com/ThiagoSousa81/Read-me-Apps/#readme", code=302)  

# Função para coletar as chaves da API
def get_keys():
    url = "https://ebs-csp.vercel.app/assimetric/generate?size=1024&raw=0"
    response = requests.get(url)
    return response.json()

# Função para dividir a chave em várias linhas
def split_key_into_lines(key, max_length=60):
    # Dividir a chave em partes de tamanho máximo definido
    lines = [key[i:i + max_length] for i in range(0, len(key), max_length)]
    return lines

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
