from flask import Flask, render_template_string, request

app = Flask(__name__)

# ================== PÁGINA INICIAL ==================
@app.route('/')
def index():
    return render_template_string("""
    <h1>🌐 Portal Educativo da Saúde</h1>
    <p>Bem-vindo ao site de apoio aos agentes do posto de saúde.</p>
    <ul>
        <li><a href="/videos">📺 Vídeos Educativos</a></li>
        <li><a href="/quiz">❓ Quiz Educativo</a></li>
        <li><a href="/memoria">🧠 Jogo da Memória</a></li>
        <li><a href="/certo_errado">✅❌ Certo ou Errado</a></li>
        <li><a href="/feedback">📝 Deixar Feedback</a></li>
        <li><a href="/contato">☎️ Contato</a></li>
    </ul>
    """)

# ================== VÍDEOS ==================
@app.route('/videos')
def videos():
    return render_template_string("""
    <h2>📺 Vídeos Educativos</h2>
    <ul>
        <li><a href="https://www.youtube.com/watch?v=VYOjWnS4cMY" target="_blank">Vacinação Infantil</a></li>
        <li><a href="https://www.youtube.com/watch?v=abcd" target="_blank">Higiene Pessoal</a></li>
        <li><a href="https://www.youtube.com/watch?v=efgh" target="_blank">Alimentação Saudável</a></li>
    </ul>
    <a href="/">⬅️ Voltar</a>
    """)

# ================== QUIZ ==================
@app.route('/quiz')
def quiz():
    return render_template_string("""
    <h2>❓ Quiz Educativo</h2>

    <audio id="acerto" src="/static/sounds/acerto.mp3"></audio>
    <audio id="erro" src="/static/sounds/erro.mp3"></audio>

    <form id="quizForm">
        <p>1) A vacinação é importante para prevenir doenças?</p>
        <input type="radio" id="q1a" name="q1"> Sim <br>
        <input type="radio" name="q1"> Não <br>

        <p>2) Escovar os dentes deve ser feito apenas uma vez ao dia?</p>
        <input type="radio" name="q2"> Sim <br>
        <input type="radio" id="q2a" name="q2"> Não <br>

        <p>3) Beber água ajuda a manter a saúde?</p>
        <input type="radio" id="q3a" name="q3"> Sim <br>
        <input type="radio" name="q3"> Não <br>

        <button type="button" onclick="resultado()">Enviar Respostas</button>
    </form>

    <script>
    function resultado() {
        let pontos = 0;
        if (document.getElementById("q1a").checked) pontos++;
        if (document.getElementById("q2a").checked) pontos++;
        if (document.getElementById("q3a").checked) pontos++;

        if (pontos == 3) {
            document.getElementById("acerto").play();
            alert("🎉 Parabéns! Você acertou todas!");
        } else {
            document.getElementById("erro").play();
            alert("Você acertou " + pontos + " de 3 perguntas. Continue tentando!");
        }
    }
    </script>

    <a href="/">⬅️ Voltar</a>
    """)

# ================== JOGO DA MEMÓRIA ==================
@app.route('/memoria')
def memoria():
    return render_template_string("""
    <h2>🧠 Jogo da Memória - Saúde</h2>

    <audio id="acerto" src="/static/sounds/acerto.mp3"></audio>
    <audio id="erro" src="/static/sounds/erro.mp3"></audio>

    <div id="tabuleiro"></div>

    <script>
    const cartas = ["💉","💉","🍎","🍎","🧼","🧼","🚰","🚰"];
    let selecionadas = [];

    cartas.sort(() => 0.5 - Math.random());

    const tabuleiro = document.getElementById("tabuleiro");
    cartas.forEach((c, i) => {
        let div = document.createElement("div");
        div.dataset.valor = c;
        div.innerHTML = "❓";
        div.style.display = "inline-block";
        div.style.width = "80px";
        div.style.height = "80px";
        div.style.margin = "10px";
        div.style.fontSize = "40px";
        div.style.textAlign = "center";
        div.style.verticalAlign = "middle";
        div.style.lineHeight = "80px";
        div.style.border = "2px solid #444";
        div.style.cursor = "pointer";
        div.onclick = () => revelar(div);
        tabuleiro.appendChild(div);
    });

    function revelar(div) {
        if (div.classList.contains("revelado") || selecionadas.length == 2) return;
        div.innerHTML = div.dataset.valor;
        selecionadas.push(div);

        if (selecionadas.length == 2) {
            if (selecionadas[0].dataset.valor === selecionadas[1].dataset.valor) {
                document.getElementById("acerto").play();
                selecionadas.forEach(d => d.classList.add("revelado"));
                selecionadas = [];
            } else {
                document.getElementById("erro").play();
                setTimeout(() => {
                    selecionadas.forEach(d => d.innerHTML = "❓");
                    selecionadas = [];
                }, 800);
            }
        }
    }
    </script>

    <a href="/">⬅️ Voltar</a>
    """)

# ================== CERTO OU ERRADO ==================
@app.route('/certo_errado')
def certo_errado():
    return render_template_string("""
    <h2>✅❌ Jogo: Certo ou Errado</h2>

    <audio id="acerto" src="/static/sounds/acerto.mp3"></audio>
    <audio id="erro" src="/static/sounds/erro.mp3"></audio>

    <p>🚰 Beber água ajuda na hidratação do corpo.</p>
    <button onclick="verificar(true, true)">Certo</button>
    <button onclick="verificar(false, true)">Errado</button>

    <p>🍭 Comer doces em excesso faz bem para os dentes.</p>
    <button onclick="verificar(true, false)">Certo</button>
    <button onclick="verificar(false, false)">Errado</button>

    <script>
    function verificar(resposta, correto) {
        if (resposta == correto) {
            document.getElementById("acerto").play();
            alert("✅ Muito bem, resposta correta!");
        } else {
            document.getElementById("erro").play();
            alert("❌ Ops, tente novamente!");
        }
    }
    </script>

    <a href="/">⬅️ Voltar</a>
    """)

# ================== FEEDBACK ==================
@app.route('/feedback', methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        sugestao = request.form["sugestao"]
        return f"<h2>Obrigado pelo feedback! Você escreveu:</h2><p>{sugestao}</p><a href='/'>⬅️ Voltar</a>"
    return render_template_string("""
    <h2>📝 Deixe seu Feedback</h2>
    <form method="post">
        <textarea name="sugestao" rows="5" cols="40" placeholder="Escreva aqui..."></textarea><br>
        <button type="submit">Enviar</button>
    </form>
    <a href="/">⬅️ Voltar</a>
    """)

# ================== CONTATO ==================
@app.route('/contato')
def contato():
    return render_template_string("""
    <h2>☎️ Contato</h2>
    <p>Email: suporte@posto.com</p>
    <p>Telefone: (69) 99999-9999</p>
    <a href="/">⬅️ Voltar</a>
    """)

# ================== EXECUTAR ==================
if __name__ == "__main__":
    app.run(debug=True)