# app.py (substitua todo o seu app.py por este arquivo)
from flask import Flask, render_template_string, request, redirect, url_for
import feedparser
import time
from datetime import datetime

app = Flask(__name__)

# -------------------------
# Configurações de notícias
# -------------------------
NEWS_FEEDS = [
    ("G1", "https://g1.globo.com/rss/g1/"),  # feed G1 (categoria geral)
    ("Agência Brasil", "https://agenciabrasil.ebc.com.br/rss.xml")  # feed Agência Brasil
]
KEYWORDS = ["criança", "crianças", "infância", "adolescente", "adolescentes", "ECA", "conselho", "conselho tutelar", "infantil", "jovem", "juventude"]
NEWS_CACHE = []
NEWS_LAST_FETCH = 0
NEWS_CACHE_TTL = 24 * 3600  # segundos (24 horas)

# -------------------------
# Layout base (mantém seu estilo original)
# -------------------------
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
        nav { background: #004a99; padding: 10px; display: flex; justify-content: center; gap: 20px; flex-wrap:wrap; }
        nav a { color: white; text-decoration: none; font-weight: bold; }
        nav a:hover { text-decoration: underline; }
        main { padding: 20px; max-width: 1000px; margin: 0 auto;}
        iframe { width: 100%; height: 360px; margin-bottom: 20px; border-radius: 10px; }
        .card { background: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .video-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }
        .video-card img { width: 100%; height: 220px; object-fit: cover; border-radius: 8px; display:block; }
        .video-title { font-weight: bold; margin-top: 6px; }
        .news-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px,1fr)); gap:12px; }
        .news-card { background:#fff;padding:12px;border-radius:8px;border:1px solid #ddd; }
        .games-grid { display:flex; gap:12px; flex-wrap:wrap; }
        .btn { background:#0066cc;color:#fff;padding:8px 12px;border-radius:6px;text-decoration:none;display:inline-block; }
        .small { font-size:0.9rem; color:#555; }
        .scoreboard { display:flex; gap:12px; align-items:center; margin-bottom:10px; }
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
        <a href="/feedback">Feedback</a>
    </nav>
    <main>
        {{ content|safe }}
    </main>
</body>
</html>
"""

# -------------------------
# Helper: buscar notícias (cache 24h)
# -------------------------
def fetch_news():
    global NEWS_CACHE, NEWS_LAST_FETCH
    now = time.time()
    if NEWS_CACHE and (now - NEWS_LAST_FETCH) < NEWS_CACHE_TTL:
        return NEWS_CACHE

    items = []
    for source_name, url in NEWS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries:
                title = e.get("title", "")
                link = e.get("link", "")
                summary = e.get("summary", "") if "summary" in e else ""
                published_parsed = e.get("published_parsed")  # tuple or None
                pub_ts = time.mktime(published_parsed) if published_parsed else 0
                # filtrar por palavras-chave no título ou resumo (se houver)
                txt = (title + " " + summary).lower()
                matched = any(k in txt for k in KEYWORDS)
                items.append({
                    "source": source_name,
                    "title": title,
                    "link": link,
                    "pub_ts": pub_ts,
                    "matched": matched
                })
        except Exception as ex:
            # falha ao ler feed; apenas ignore (não trava)
            print("Erro ao ler feed", url, ex)

    # prioriza itens que combinaram com as palavras-chave; então ordena por data
    items.sort(key=lambda x: (0 if x["matched"] else 1, -x["pub_ts"]))
    # pega top 8 (mistura fontes)
    NEWS_CACHE = items[:8]
    NEWS_LAST_FETCH = now
    return NEWS_CACHE

# -------------------------
# Página inicial (inclui notícias)
# -------------------------
@app.route("/")
def home():
    news = fetch_news()
    news_html = ""
    if news:
        news_html += "<div class='card'><h2>📢 Últimas notícias sobre crianças e jovens</h2><div class='news-grid'>"
        for n in news:
            # formata data
            dt = ""
            if n["pub_ts"]:
                dt = datetime.utcfromtimestamp(n["pub_ts"]).strftime("%d/%m/%Y %H:%M")
            news_html += f"""
            <div class='news-card'>
                <div class='small'><b>{n['source']}</b> - {dt}</div>
                <div style='margin:8px 0; font-weight:600;'>{n['title']}</div>
                <a class='btn' href="{n['link']}" target="_blank">Ler no site</a>
            </div>
            """
        news_html += "</div></div>"
    else:
        news_html = "<div class='card'><h2>📢 Notícias</h2><p>Nenhuma notícia disponível no momento.</p></div>"

    content = f"""
    <div class='card'>
        <h2>Bem-vindo!</h2>
        <p>Este aplicativo foi desenvolvido para apoiar crianças, adolescentes e famílias da comunidade Vila Princesa em Porto Velho.</p>
        <p>Aqui você encontrará vídeos educativos, jogos interativos e informações de contato para ajuda.</p>
    </div>
    {news_html}
    <div class='card'>
        <h2>📌 Ações rápidas</h2>
        <div class='games-grid'>
            <a class='btn' href='/videos'>Ver Vídeos</a>
            <a class='btn' href='/jogos'>Ir para Jogos</a>
            <a class='btn' href='/contatos'>Contatos</a>
        </div>
    </div>
    """
    return render_template_string(base_html, content=content)

# -------------------------
# Página vídeos (mais vídeos, thumbnails mais altos)
# -------------------------
ADULT_VIDEOS = [
    ("Direitos previstos no ECA", "OYYk-DhaoD0"),
    ("Direitos e deveres (ECA)", "nJkczMArpwk"),
    ("Como acionar o Conselho Tutelar", "R8y5JZuIuVc"),
    ("Prevenção de violência e abusos", "phqr_q1WvZI"),
    ("Prevenção de violência (2)", "1n5QZDbpT4o")
]
KIDS_VIDEOS = [
    ("Segurança e prevenção (infantil)", "yhvHsg8Epso"),
    ("Respeito e convivência (infantil)", "SoIpR-kbRcA"),
    ("Associação educativa (infantil)", "OQ3VKHVtilk"),
    ("Higiene para crianças", "b95-WF1f5HY"),
    ("Convivência e valores", "3bQvNjmKAvA"),
    ("Histórias educativas", "YB0xif-dU9o")
]

@app.route("/videos")
def videos():
    def make_video_card(title, vid):
        thumb = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
        embed = f"https://www.youtube.com/embed/{vid}"
        return f"""
        <div class="video-card card">
            <a href="{embed}" target="_blank"><img src="{thumb}" alt="{title}"></a>
            <div class="video-title">{title}</div>
            <div class="small"><a href="{embed}" target="_blank">Assistir (YouTube)</a></div>
        </div>
        """

    adult_html = "<div class='card'><h2>🎥 Vídeos para Adultos</h2><div class='video-grid'>"
    for t, v in ADULT_VIDEOS:
        adult_html += make_video_card(t, v)
    adult_html += "</div></div>"

    kids_html = "<div class='card'><h2>👶 Vídeos para Crianças</h2><div class='video-grid'>"
    for t, v in KIDS_VIDEOS:
        kids_html += make_video_card(t, v)
    kids_html += "</div></div>"

    content = adult_html + kids_html + "<a href='/'>⬅ Voltar</a>"
    return render_template_string(base_html, content=content)

# -------------------------
# PÁGINA JOGOS - opção /jogos (menu) e rotas específicas
# -------------------------
@app.route("/jogos")
def jogos():
    content = """
    <div class='card'>
        <h2>🎮 Jogos Interativos</h2>
        <p>Escolha um jogo educativo. Cada jogo tem fases (1 a 10) e sistema de pontuação.</p>
        <ul>
            <li><a href='/jogos/memoria'>🧠 Jogo da Memória (fases & pontuação)</a></li>
            <li><a href='/jogos/certoerrado'>✅❌ Certo ou Errado (fases & pontuação)</a></li>
        </ul>
    </div>
    <a href='/'>⬅ Voltar</a>
    """
    return render_template_string(base_html, content=content)

# -------------------------
# Jogo da Memória (com fases 1..10 e sistema de pontuação + combo)
# -------------------------
@app.route("/jogos/memoria")
def jogos_memoria():
    return render_template_string(base_html, content="""
    <div class='card'>
    <h2>🧠 Jogo da Memória - Saúde e Direitos (Fases 1 a 10)</h2>
    <div class="scoreboard">
        <div>Fase: <span id="fase">1</span></div>
        <div>Pontuação: <b id="score">0</b></div>
        <div>Combo: x<span id="combo">1</span></div>
    </div>
    <div id="board" style="display:flex;flex-wrap:wrap;gap:8px;"></div>
    <div style="margin-top:12px;">
        <button class="btn" onclick="restart()">Reiniciar Fase</button>
        <button class="btn" onclick="nextPhase()">Próxima Fase</button>
    </div>

    <!-- Sons -->
    <audio id="som-acerto" src="/static/sounds/acerto.mp3"></audio>
    <audio id="som-erro" src="/static/sounds/erro.mp3"></audio>
    <audio id="som-aplausos" src="/static/sounds/aplausos.mp3"></audio>

    <p class="small">Objetivo: combine todos os pares. Cada par vale pontos; combos duplicam os pontos por sequência de acertos.</p>
    </div>

    <script>
    // emojis possíveis (temas: saúde, educação, proteção, higiene)
    const EMOJIS = ["💉","🍎","🧼","🚰","📚","🛡","👨‍👩‍👧","🩺","🦺","🤝","🧴","🧷"];
    let phase = 1;
    let score = 0;
    let combo = 1;
    let pairsNeeded = 4; // inicial (fase 1)
    let matchedPairs = 0;
    let board = document.getElementById("board");

    function buildBoard() {
        board.innerHTML = "";
        document.getElementById("fase").innerText = phase;
        document.getElementById("score").innerText = score;
        document.getElementById("combo").innerText = combo;
        // define pares conforme a fase: pares = min(3 + phase, EMOJIS.length)
        pairsNeeded = Math.min(3 + phase, EMOJIS.length);
        let items = EMOJIS.slice(0, pairsNeeded);
        let cards = [];
        items.forEach(i => { cards.push(i); cards.push(i); });
        // embaralha
        cards.sort(() => 0.5 - Math.random());
        cards.forEach((val, idx) => {
            let b = document.createElement("button");
            b.className = "card";
            b.style.width = "80px";
            b.style.height = "80px";
            b.style.fontSize = "36px";
            b.style.display = "flex";
            b.style.alignItems = "center";
            b.style.justifyContent = "center";
            b.style.cursor = "pointer";
            b.dataset.value = val;
            b.dataset.revealed = "false";
            b.innerText = "❓";
            b.onclick = () => flip(b);
            board.appendChild(b);
        });
        matchedPairs = 0;
    }

    let revealed = [];

    function flip(button) {
        if (button.dataset.revealed == "true") return;
        if (revealed.length == 2) return;
        button.innerText = button.dataset.value;
        revealed.push(button);
        if (revealed.length == 2) {
            if (revealed[0].dataset.value === revealed[1].dataset.value) {
                // acerto
                document.getElementById("som-acerto").play();
                revealed.forEach(x => { x.dataset.revealed = "true"; x.style.background = "#4CAF50"; x.style.color = "#fff"; });
                matchedPairs++;
                // pontos: base 10, multiplicador de combo
                let base = 10;
                score += base * combo;
                combo = combo * 2; // dobra o multiplicador para próximo acerto em sequência
                updateHUD();
                revealed = [];
                if (matchedPairs == pairsNeeded) {
                    // fase completa
                    document.getElementById("som-aplausos").play();
                    alert("🎉 Fase completa! Clique em Próxima Fase para avançar.");
                }
            } else {
                // erro
                document.getElementById("som-erro").play();
                combo = 1; // zera o combo
                updateHUD();
                setTimeout(() => {
                    revealed.forEach(x => { x.innerText = "❓"; });
                    revealed = [];
                }, 700);
            }
        }
    }

    function updateHUD() {
        document.getElementById("score").innerText = score;
        document.getElementById("combo").innerText = combo;
    }

    function restart() {
        combo = 1;
        matchedPairs = 0;
        updateHUD();
        buildBoard();
    }

    function nextPhase() {
        if (phase < 10) phase++;
        else { alert("Você já está na fase máxima (10)! Continue jogando para aumentar pontuação."); }
        buildBoard();
    }

    // inicializa
    buildBoard();
    </script>
    """)

# -------------------------
# Jogo Certo ou Errado (fases e pontuação)
# -------------------------
@app.route("/jogos/certoerrado")
def jogos_certoerrado():
    # perguntas exemplo (verdadeiro == true)
    questions = [
        {"q":"Lavar as mãos ajuda a prevenir doenças.", "a":True},
        {"q":"Crianças não precisam ir à escola todos os dias.", "a":False},
        {"q":"Vacinar as crianças protege a comunidade.", "a":True},
        {"q":"Uma criança pode trabalhar livremente sem regras.", "a":False},
        {"q":"Uma boa alimentação ajuda no aprendizado.", "a":True},
        {"q":"Violência dentro de casa é normal e não deve ser denunciada.", "a":False},
        {"q":"Conselho Tutelar atua na proteção de direitos.", "a":True},
        {"q":"É correto compartilhar fotos íntimas de crianças.", "a":False},
        {"q":"Praticar esportes ajuda na saúde mental e física.", "a":True},
        {"q":"A escola atrapalha a infância.", "a":False}
    ]

    import json
    questions_js = json.dumps(questions)

    # Construímos o conteúdo como string normal (não f-string),
    # concatenando questions_js para evitar conflito com { } do JS.
    content = """
    <div class='card'>
    <h2>✅❌ Certo ou Errado - Fases 1 a 10</h2>
    <div class="scoreboard">
        <div>Fase: <span id="fase">1</span></div>
        <div>Pontuação: <b id="score">0</b></div>
        <div>Combo: x<span id="combo">1</span></div>
    </div>

    <div id="questao" style="margin-bottom:12px; font-size:1.1rem;"></div>
    <button class="btn" onclick="responder(true)">✅ Certo</button>
    <button class="btn" onclick="responder(false)">❌ Errado</button>
    <div style="margin-top:12px;">
        <button class="btn" onclick="proximaFase()">Próxima Fase</button>
        <button class="btn" onclick="reiniciar()">Reiniciar Fase</button>
    </div>

    <!-- sons -->
    <audio id="som-acerto" src="/static/sounds/acerto.mp3"></audio>
    <audio id="som-erro" src="/static/sounds/erro.mp3"></audio>
    <audio id="som-aplausos" src="/static/sounds/aplausos.mp3"></audio>

    <p class="small">Responda corretamente para ganhar pontos. Sequências corretas aumentam o combo (multiplicador).</p>
    </div>

    <script>
    const QUESTIONS = """ + questions_js + """;
    let fase = 1;
    let score = 0;
    let combo = 1;
    let index = 0;
    // cada fase usa 3 perguntas (pode ajustar)
    function montarFase() {
        index = 0;
        document.getElementById("fase").innerText = fase;
        // embaralha e pega subset
        let pool = QUESTIONS.slice();
        pool.sort(() => 0.5 - Math.random());
        window.phaseQuestions = pool.slice(0, Math.min(5, pool.length)); // 5 perguntas por fase
        mostrarQuestao();
    }
    function mostrarQuestao() {
        if (index >= window.phaseQuestions.length) {
            document.getElementById("questao").innerText = "Fase concluída! Clique em Próxima Fase para avançar.";
            document.getElementById("questao").style.fontWeight = "600";
            document.getElementById("questao").style.color = "#2a7";
            return;
        }
        document.getElementById("questao").innerText = window.phaseQuestions[index].q;
        document.getElementById("questao").style.color = "#000";
    }
    function responder(resposta) {
        if (index >= window.phaseQuestions.length) return alert("Fase concluída!");
        const correto = window.phaseQuestions[index].a;
        if (resposta === correto) {
            document.getElementById("som-acerto").play();
            let base = 10;
            score += base * combo;
            combo = combo * 2; // dobra próxima pontuação se seguir acertos
            index++;
            mostrarQuestao();
        } else {
            document.getElementById("som-erro").play();
            combo = 1; // reset combo
            index++;
            mostrarQuestao();
        }
        document.getElementById("score").innerText = score;
        document.getElementById("combo").innerText = combo;
    }
    function proximaFase() {
        if (fase < 10) fase++;
        else alert("Você já está na fase 10!");
        montarFase();
    }
    function reiniciar() {
        combo = 1;
        montarFase();
        document.getElementById("score").innerText = score;
        document.getElementById("combo").innerText = combo;
    }
    // inicializa
    montarFase();
    </script>
    """

    return render_template_string(base_html, content=content)

# -------------------------
# Contatos (mantém os contatos originais)
# -------------------------
@app.route("/contatos")
def contatos():
    content = """
    <div class="card">
        <h2>📞 Conselhos Tutelares em Porto Velho</h2>
        <ul>
            <li><b>III Conselho Tutelar</b> – R. Erva Doce – (69) 98473-4966</li>
            <li><b>1º Conselho Tutelar</b> – R. Joaquim Nabuco, 1733 – (69) 99981-0664</li>
            <li><b>II Conselho Tutelar Zona Leste</b> – R. Antônio de Souza, 4730 - (69) 76829-382</li>
            <li><b>Casa dos Conselhos Municipais</b> – R. Guanabara, 965 – (69) 98473-4098</li>
        </ul>
    </div>
    """
    return render_template_string(base_html, content=content)

# -------------------------
# Feedback - mantém forma simples (envia e mostra)
# -------------------------
@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        text = request.form.get("sugestao", "")
        # aqui podemos salvar em arquivo/banco; por enquanto mostramos na tela
        return render_template_string(base_html, content=f"<div class='card'><h2>Obrigado!</h2><p>Recebemos: {text}</p><a href='/'>⬅ Voltar</a></div>")
    return render_template_string(base_html, content="""
    <div class="card">
    <h2>📝 Feedback dos Servidores</h2>
    <form method="post">
        <textarea name="sugestao" rows="5" cols="60" placeholder="Sugestões e comentários..."></textarea><br>
        <button class="btn" type="submit">Enviar</button>
    </form>
    <a href="/">⬅ Voltar</a>
    </div>
    """)

# -------------------------
# Executar
# -------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")