from flask import Flask, render_template_string

app = Flask(__name__)

# HTML base com navegação
base_html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App Educativo - Vila Princesa</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }
        header { background: #0066cc; color: white; padding: 15px; text-align: center; }
        nav { background: #004a99; padding: 10px; display: flex; justify-content: center; gap: 20px; }
        nav a { color: white; text-decoration: none; font-weight: bold; }
        nav a:hover { text-decoration: underline; }
        main { padding: 20px; }
        iframe { width: 100%; height: 315px; margin-bottom: 20px; border-radius: 10px; }
        .card { background: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <header>
        <h1>Aplicativo Educativo - Vila Princesa</h1>
    </header>
    <nav>
        <a href="/">Início</a>
        <a href="/videos">Vídeos</a>
        <a href="/jogos">Jogos</a>
        <a href="/contatos">Ajuda</a>
    </nav>
    <main>
        {{ content|safe }}
    </main>
</body>
</html>
"""

@app.route("/")
def home():
    content = """
    <div class="card">
        <h2>Bem-vindo!</h2>
        <p>Este aplicativo foi desenvolvido para apoiar crianças, adolescentes e famílias da comunidade Vila Princesa em Porto Velho.</p>
        <p>Aqui você encontrará vídeos educativos, jogos interativos e informações de contato para ajuda.</p>
    </div>
    """
    return render_template_string(base_html, content=content)

@app.route("/videos")
def videos():
    content = """
    <div class="card">
        <h2>🎥 Vídeos para Adultos</h2>
        <iframe src="https://www.youtube.com/embed/OYYk-DhaoD0" allowfullscreen></iframe>
        <iframe src="https://www.youtube.com/embed/phqr_q1WvZI" allowfullscreen></iframe>
    </div>
    <div class="card">
        <h2>👶 Vídeos para Crianças</h2>
        <iframe src="https://www.youtube.com/embed/yhvHsg8Epso" allowfullscreen></iframe>
        <iframe src="https://www.youtube.com/embed/SoIpR-kbRcA" allowfullscreen></iframe>
    </div>
    """
    return render_template_string(base_html, content=content)

@app.route("/jogos")
def jogos():
    content = """
    <div class="card">
        <h2>🧩 Quiz de Segurança</h2>
        <p><b>Pergunta:</b> O que você deve fazer se um estranho oferecer doces na rua?</p>
        <ul>
            <li>✅ Dizer não e procurar um adulto de confiança</li>
            <li>❌ Aceitar os doces</li>
            <li>❌ Sair com a pessoa</li>
        </ul>
    </div>
    <div class="card">
        <h2>🎮 Jogo da Memória (versão simples)</h2>
        <p>Em breve: arraste e solte cartões para combinar segurança e respeito!</p>
    </div>
    """
    return render_template_string(base_html, content=content)

@app.route("/contatos")
def contatos():
    content = """
    <div class="card">
        <h2>📞 Conselhos Tutelares em Porto Velho</h2>
        <ul>
            <li><b>III Conselho Tutelar</b> – R. Erva Doce – (69) 98473-4966</li>
            <li><b>1º Conselho Tutelar</b> – R. Joaquim Nabuco, 1733 – (69) 99981-0664</li>
            <li><b>II Conselho Tutelar Zona Leste</b> – R. Antônio de Souza, 4730</li>
            <li><b>Casa dos Conselhos Municipais</b> – R. Guanabara, 965 – (69) 98473-4098</li>
        </ul>
    </div>
    """
    return render_template_string(base_html, content=content)

if __name__ == "__main__":
    app.run(debug=True)