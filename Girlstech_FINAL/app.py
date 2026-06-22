from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "girlstech_secret_key_v2"
DB_PATH = os.path.join("database", "girlstech.db")

LEVELS = [
    {
        "id": 1,
        "title": "Qu'est-ce qu'un programme ?",
        "concept": "Un programme est une suite d'instructions données à un ordinateur.",
        "lesson_steps": [
            "Salut, moi c'est Ada ! Aujourd'hui, on commence par la base : un programme.",
            "Un programme, c'est comme une recette : on donne des étapes à suivre dans un ordre précis.",
            "Exemple : afficher un message, calculer un score ou vérifier une réponse.",
            "Dans ce niveau, tu vas apprendre à reconnaître ce qu'est une instruction."
        ],
        "woman": "Ada Lovelace",
        "story": "Ada Lovelace est considérée comme la première programmeuse de l'histoire.",
        "question": "Qu'est-ce qu'un programme ?",
        "choices": ["Une suite d'instructions", "Une image", "Un câble informatique", "Un écran"],
        "answer": "Une suite d'instructions",
        "explanation": "Un programme indique à l'ordinateur ce qu'il doit faire, étape par étape."
    },
    {
        "id": 2,
        "title": "Les variables",
        "concept": "Une variable permet de stocker une information pour la réutiliser plus tard.",
        "lesson_steps": [
            "Aujourd'hui, on découvre les variables.",
            "Imagine une variable comme une petite boîte avec une étiquette.",
            "Exemple : prenom = 'Emma'. La boîte s'appelle prenom et contient Emma.",
            "Les variables permettent de garder des informations en mémoire."
        ],
        "woman": "Grace Hopper",
        "story": "Grace Hopper a contribué à rendre la programmation plus compréhensible.",
        "question": "À quoi sert une variable ?",
        "choices": ["À stocker une information", "À éteindre un ordinateur", "À changer la couleur de l'écran", "À imprimer une page"],
        "answer": "À stocker une information",
        "explanation": "Une variable peut contenir un nombre, un texte ou une autre information."
    },
    {
        "id": 3,
        "title": "Les conditions",
        "concept": "Une condition permet à un programme de prendre une décision.",
        "lesson_steps": [
            "Dans ce niveau, on apprend les conditions.",
            "Une condition permet au programme de choisir entre plusieurs actions.",
            "Exemple : si le score est supérieur à 10, alors on affiche Bravo.",
            "En Python, on utilise souvent if, elif et else."
        ],
        "woman": "Katherine Johnson",
        "story": "Katherine Johnson était mathématicienne à la NASA.",
        "question": "Que permet une condition en programmation ?",
        "choices": ["Prendre une décision", "Dessiner une mascotte", "Créer un clavier", "Supprimer Internet"],
        "answer": "Prendre une décision",
        "explanation": "Avec if, elif et else, un programme peut réagir selon une situation."
    },
    {
        "id": 4,
        "title": "Les boucles",
        "concept": "Une boucle permet de répéter plusieurs fois une instruction.",
        "lesson_steps": [
            "Les boucles servent à répéter des actions sans recopier le même code.",
            "Exemple : afficher les nombres de 1 à 5.",
            "En Python, on peut utiliser for ou while.",
            "Les boucles sont très utiles dans les jeux, les scores et les listes."
        ],
        "woman": "Margaret Hamilton",
        "story": "Margaret Hamilton a dirigé le logiciel embarqué du programme Apollo.",
        "question": "À quoi sert une boucle ?",
        "choices": ["À répéter des instructions", "À créer un mot de passe", "À ouvrir une fenêtre", "À brancher un ordinateur"],
        "answer": "À répéter des instructions",
        "explanation": "Les boucles for et while permettent de répéter un bloc de code."
    },
    {
        "id": 5,
        "title": "Les fonctions",
        "concept": "Une fonction regroupe des instructions que l'on peut réutiliser.",
        "lesson_steps": [
            "Une fonction, c'est un petit bloc de code avec un nom.",
            "Elle permet de ranger une action pour pouvoir la réutiliser.",
            "Exemple : def dire_bonjour(): print('Bonjour')",
            "Les fonctions rendent le code plus propre et plus facile à comprendre."
        ],
        "woman": "Radia Perlman",
        "story": "Radia Perlman est connue pour ses travaux majeurs dans les réseaux.",
        "question": "Pourquoi utilise-t-on une fonction ?",
        "choices": ["Pour réutiliser du code", "Pour casser un programme", "Pour fermer Python", "Pour colorier une page"],
        "answer": "Pour réutiliser du code",
        "explanation": "Une fonction évite de réécrire plusieurs fois les mêmes instructions."
    },
    {
        "id": 6,
        "title": "Les listes",
        "concept": "Une liste permet de stocker plusieurs valeurs dans une seule variable.",
        "lesson_steps": [
            "Une liste est une collection d'éléments.",
            "Exemple : langages = ['Python', 'HTML', 'CSS']",
            "On peut accéder aux éléments, les ajouter ou les supprimer.",
            "Les listes sont très utiles pour organiser plusieurs informations."
        ],
        "woman": "Ada Lovelace",
        "story": "Ada Lovelace a imaginé qu'une machine pouvait manipuler des symboles et pas seulement des nombres.",
        "question": "Quel exemple représente une liste Python ?",
        "choices": ["fruits = ['pomme', 'banane']", "fruit = pomme", "print = fruits", "if fruits"],
        "answer": "fruits = ['pomme', 'banane']",
        "explanation": "En Python, une liste s'écrit avec des crochets."
    },
    {
        "id": 7,
        "title": "Les dictionnaires",
        "concept": "Un dictionnaire associe une clé à une valeur.",
        "lesson_steps": [
            "Un dictionnaire est comme une fiche d'identité.",
            "Exemple : eleve = {'nom': 'Lina', 'age': 13}",
            "La clé 'nom' permet de retrouver la valeur 'Lina'.",
            "C'est très pratique pour organiser des données."
        ],
        "woman": "Grace Hopper",
        "story": "Grace Hopper a participé à la création de COBOL, un langage pensé pour être plus proche de l'anglais.",
        "question": "Dans un dictionnaire, on associe...",
        "choices": ["Une clé à une valeur", "Un écran à une souris", "Une image à un son", "Un bug à un câble"],
        "answer": "Une clé à une valeur",
        "explanation": "Les dictionnaires utilisent des paires clé/valeur."
    },
    {
        "id": 8,
        "title": "Les erreurs",
        "concept": "Une erreur n'est pas un échec : c'est une information pour améliorer le code.",
        "lesson_steps": [
            "En programmation, tout le monde fait des erreurs.",
            "Le plus important est d'apprendre à lire le message d'erreur.",
            "Un bug indique souvent où le programme bloque.",
            "Corriger une erreur, c'est progresser comme une vraie développeuse."
        ],
        "woman": "Katherine Johnson",
        "story": "La précision des calculs de Katherine Johnson a été essentielle pour la sécurité des missions spatiales.",
        "question": "Que faut-il faire face à une erreur ?",
        "choices": ["Lire le message et corriger", "Tout supprimer", "Éteindre l'ordinateur", "Ignorer le problème"],
        "answer": "Lire le message et corriger",
        "explanation": "Les erreurs aident à comprendre ce qu'il faut améliorer."
    },
    {
        "id": 9,
        "title": "Les mini-projets",
        "concept": "Un mini-projet permet de combiner plusieurs notions dans un programme concret.",
        "lesson_steps": [
            "Maintenant, on assemble plusieurs notions.",
            "Un mini-projet peut utiliser variables, conditions, boucles et fonctions.",
            "Exemple : créer un quiz avec score.",
            "C'est comme cela qu'on passe de la théorie à une vraie application."
        ],
        "woman": "Margaret Hamilton",
        "story": "Margaret Hamilton a montré l'importance du logiciel dans les grands projets scientifiques.",
        "question": "Un mini-projet sert surtout à...",
        "choices": ["Combiner plusieurs notions", "Supprimer le code", "Écrire sans tester", "Ne faire que du design"],
        "answer": "Combiner plusieurs notions",
        "explanation": "Un projet permet de pratiquer plusieurs compétences en même temps."
    },
    {
        "id": 10,
        "title": "Défi final GIRLSTECH",
        "concept": "Le défi final vérifie les bases de Python et la culture tech acquises.",
        "lesson_steps": [
            "Bravo, tu arrives au défi final !",
            "Tu vas mobiliser ce que tu as appris : variables, conditions, boucles et logique.",
            "Rappelle-toi : l'objectif n'est pas d'être parfaite, mais de progresser.",
            "Prête à valider ton parcours GIRLSTECH ?"
        ],
        "woman": "Radia Perlman",
        "story": "Radia Perlman a contribué à rendre les réseaux modernes plus fiables.",
        "question": "Quelle attitude est la plus importante en programmation ?",
        "choices": ["Tester, apprendre et corriger", "Ne jamais se tromper", "Éviter les exercices", "Copier sans comprendre"],
        "answer": "Tester, apprendre et corriger",
        "explanation": "La programmation repose beaucoup sur les tests, la logique et l'amélioration continue."
    },
]

WOMEN = [
    {
        "id": 1,
        "name": "Ada Lovelace",
        "image": "ada_lovelace.jpeg",
        "role": "Première programmeuse",
        "description": "Elle est considérée comme la première programmeuse de l'histoire. Au XIXe siècle, elle a imaginé un algorithme destiné à être exécuté par une machine.",
        "choices": ["Ada Lovelace", "Grace Hopper", "Katherine Johnson", "Radia Perlman"],
        "answer": "Ada Lovelace"
    },
    {
        "id": 2,
        "name": "Grace Hopper",
        "image": "grace_hopper.jpeg",
        "role": "Pionnière des compilateurs",
        "description": "Elle a participé au développement des premiers langages modernes et créé l'un des premiers compilateurs.",
        "choices": ["Margaret Hamilton", "Grace Hopper", "Ada Lovelace", "Katherine Johnson"],
        "answer": "Grace Hopper"
    },
    {
        "id": 3,
        "name": "Katherine Johnson",
        "image": "katherine_johnson.jpeg",
        "role": "Mathématicienne à la NASA",
        "description": "Ses calculs ont aidé à assurer la réussite des premières missions spatiales américaines habitées.",
        "choices": ["Radia Perlman", "Ada Lovelace", "Katherine Johnson", "Grace Hopper"],
        "answer": "Katherine Johnson"
    },
    {
        "id": 4,
        "name": "Margaret Hamilton",
        "image": "margaret_hamilton.jpeg",
        "role": "Ingénieure logiciel Apollo",
        "description": "Elle a dirigé l'équipe qui a développé le logiciel embarqué du programme Apollo.",
        "choices": ["Margaret Hamilton", "Grace Hopper", "Radia Perlman", "Katherine Johnson"],
        "answer": "Margaret Hamilton"
    },
    {
        "id": 5,
        "name": "Radia Perlman",
        "image": "radia_perlman.webp",
        "role": "Pionnière des réseaux",
        "description": "Elle est connue pour ses travaux sur le protocole Spanning Tree, essentiel dans les réseaux informatiques.",
        "choices": ["Katherine Johnson", "Ada Lovelace", "Radia Perlman", "Margaret Hamilton"],
        "answer": "Radia Perlman"
    },
]

AVATARS = [
    {"id": "emma", "name": "Emma", "emoji": "👩🏽‍💻", "field": "Développement"},
    {"id": "lina", "name": "Lina", "emoji": "👩🏼‍🔬", "field": "Cybersécurité"},
    {"id": "maya", "name": "Maya", "emoji": "👩🏾‍🚀", "field": "IA"},
    {"id": "jade", "name": "Jade", "emoji": "👩🏻‍🎨", "field": "Web Design"},
    {"id": "ines", "name": "Inès", "emoji": "👩🏿‍🎓", "field": "Data"},
    {"id": "zoe", "name": "Zoé", "emoji": "👩🏼‍🚀", "field": "Robotique"},
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs("database", exist_ok=True)
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        avatar TEXT DEFAULT 'emma',
        points INTEGER DEFAULT 0,
        current_level INTEGER DEFAULT 1
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        level_id INTEGER NOT NULL,
        success INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS women_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        woman_id INTEGER NOT NULL,
        success INTEGER DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()


@app.before_request
def before_request():
    init_db()


def current_user():
    if "user_id" not in session:
        return None
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    conn.close()
    return user


@app.route("/")
def home():
    return render_template("index.html", user=current_user())


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        avatar = request.form.get("avatar", "emma")
        if not username:
            flash("Merci d'entrer un prénom ou pseudo.")
            return redirect(url_for("register"))
        conn = get_db()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, avatar) VALUES (?, ?)", (username, avatar))
            conn.commit()
            session["user_id"] = cur.lastrowid
            return redirect(url_for("dashboard"))
        except sqlite3.IntegrityError:
            flash("Ce pseudo existe déjà.")
        finally:
            conn.close()
    return render_template("register.html", user=current_user(), avatars=AVATARS)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    if user:
        session["user_id"] = user["id"]
        return redirect(url_for("dashboard"))
    flash("Utilisateur introuvable.")
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    user = current_user()
    if not user:
        return redirect(url_for("home"))
    return render_template("dashboard.html", user=user, levels=LEVELS)


@app.route("/level/<int:level_id>", methods=["GET", "POST"])
def level(level_id):
    user = current_user()
    if not user:
        return redirect(url_for("home"))
    level_data = next((l for l in LEVELS if l["id"] == level_id), None)
    if not level_data:
        return redirect(url_for("dashboard"))
    result = None
    if request.method == "POST":
        selected = request.form.get("answer")
        success = selected == level_data["answer"]
        result = {"success": success, "correct": level_data["answer"], "explanation": level_data["explanation"]}
        conn = get_db()
        cur = conn.cursor()
        existing = cur.execute("SELECT * FROM progress WHERE user_id=? AND level_id=?", (user["id"], level_id)).fetchone()
        if success:
            if not existing:
                cur.execute("INSERT INTO progress (user_id, level_id, success) VALUES (?, ?, 1)", (user["id"], level_id))
                cur.execute("UPDATE users SET points=points+30, current_level=CASE WHEN current_level<=? THEN ? ELSE current_level END WHERE id=?", (level_id, level_id + 1, user["id"]))
            elif existing["success"] == 0:
                cur.execute("UPDATE progress SET success=1 WHERE user_id=? AND level_id=?", (user["id"], level_id))
                cur.execute("UPDATE users SET points=points+30 WHERE id=?", (user["id"],))
        else:
            if not existing:
                cur.execute("INSERT INTO progress (user_id, level_id, success) VALUES (?, ?, 0)", (user["id"], level_id))
        conn.commit()
        conn.close()
    return render_template("level.html", user=user, level=level_data, result=result)


@app.route("/women", methods=["GET", "POST"])
def women():
    user = current_user()
    result = None
    selected_card = WOMEN[0]
    if request.method == "POST" and user:
        woman_id = int(request.form.get("woman_id", 1))
        selected_card = next((w for w in WOMEN if w["id"] == woman_id), WOMEN[0])
        answer = request.form.get("answer")
        success = answer == selected_card["answer"]
        result = {"success": success, "correct": selected_card["answer"], "role": selected_card["role"]}
        conn = get_db()
        cur = conn.cursor()
        existing = cur.execute("SELECT * FROM women_progress WHERE user_id=? AND woman_id=?", (user["id"], woman_id)).fetchone()
        if success and not existing:
            cur.execute("INSERT INTO women_progress (user_id, woman_id, success) VALUES (?, ?, 1)", (user["id"], woman_id))
            cur.execute("UPDATE users SET points=points+50 WHERE id=?", (user["id"],))
        elif not existing:
            cur.execute("INSERT INTO women_progress (user_id, woman_id, success) VALUES (?, ?, 0)", (user["id"], woman_id))
        conn.commit()
        conn.close()
    return render_template("women.html", user=user, women=WOMEN, result=result, selected_card=selected_card)


@app.route("/lab", methods=["GET", "POST"])
def lab():
    user = current_user()
    if not user:
        return redirect(url_for("home"))
    code = request.form.get("code", "print('Bienvenue dans le labo Python GIRLSTECH !')")
    output = ""
    if request.method == "POST":
        allowed_examples = {
            "print('Hello')": "Hello",
            "print('Bienvenue dans le labo Python GIRLSTECH !')": "Bienvenue dans le labo Python GIRLSTECH !",
            "prenom = 'Ada'\nprint(prenom)": "Ada",
            "for i in range(3):\n    print(i)": "0\n1\n2"
        }
        output = allowed_examples.get(code.strip(), "Mode sécurisé : pour la démo, seuls les exemples proposés sont exécutés.")
    return render_template("lab.html", user=user, code=code, output=output)


@app.route("/profile")
def profile():
    user = current_user()
    if not user:
        return redirect(url_for("home"))
    conn = get_db()
    completed = conn.execute("SELECT COUNT(*) AS total FROM progress WHERE user_id=? AND success=1", (user["id"],)).fetchone()["total"]
    women_done = conn.execute("SELECT COUNT(*) AS total FROM women_progress WHERE user_id=? AND success=1", (user["id"],)).fetchone()["total"]
    conn.close()
    badges = []
    if completed >= 1: badges.append("Premiers pas")
    if completed >= 5: badges.append("Codeuse curieuse")
    if completed >= 10: badges.append("Défi GIRLSTECH")
    if women_done >= 3: badges.append("Historienne de la Tech")
    if women_done >= 5: badges.append("Femmes pionnières")
    return render_template("profile.html", user=user, completed=completed, total=len(LEVELS), women_done=women_done, badges=badges)


@app.route("/chatbot", methods=["POST"])
def chatbot():
    question = request.json.get("question", "").lower()
    answers = {
        "variable": "Une variable est comme une boîte : elle garde une information pour que ton programme puisse la réutiliser.",
        "boucle": "Une boucle sert à répéter une action plusieurs fois. En Python, on utilise souvent for ou while.",
        "condition": "Une condition permet au programme de prendre une décision avec if, elif et else.",
        "python": "Python est un langage de programmation connu pour être clair et accessible aux débutants.",
        "ada": "Ada Lovelace est souvent considérée comme la première programmeuse de l'histoire.",
        "grace": "Grace Hopper a travaillé sur les compilateurs et les langages de programmation.",
        "points": "Tu gagnes des points en validant les niveaux et en répondant aux quiz Femmes de la Tech.",
        "bloquée": "Pas de panique ! Relis la bulle d'Ada, regarde l'exemple, puis essaie d'éliminer les réponses impossibles.",
        "bloque": "Pas de panique ! Relis la bulle d'Ada, regarde l'exemple, puis essaie d'éliminer les réponses impossibles."
    }
    for key, value in answers.items():
        if key in question:
            return jsonify({"answer": value})
    return jsonify({"answer": "Je peux t'aider sur Python, les variables, les boucles, les conditions, Ada Lovelace, Grace Hopper ou les points."})


if __name__ == "__main__":
    app.run(debug=True)
