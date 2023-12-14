from flask import Flask, render_template, request, redirect
from flask import Flask, render_template, request,redirect, session, flash

app = Flask(__name__)
app.secret_key= 'Senai'
class cadvolei:
    def __init__(self,nome,idade,posicao,nivel,cidade,dia,horario):
        self.nome = nome
        self.idade = idade
        self.posicao = posicao
        self.nivel = nivel
        self.cidade = cidade
        self.dia = dia
        self.horario = horario

volleyball_players = []


@app.route('/Volei')
def volei():# put application's code here
    if 'Usuario_Logado' not in session:
        return redirect('/')
    else:
        return render_template("Volei.html", Titulo = "Jogadores de volêi", ListaJogadores = volleyball_players)

@app.route('/')
def login():
    session.clear() #assim que eu acessar a rota, limpa oque tem dentro da sessão.
    return render_template('Login.html', Titulo="Faça o seo login")

@app.route('/autenticar', methods=['POST']) #essa rotas é para quando o usuário
# se cadastrar caso não tiver login e se caso tiver o login já entra direto.
def autenticar():
    if request.form['usuario'] == 'Anaju' and request.form['senha'] =='123':
        session['Usuario_Logado'] = request.form['usuario'] #usuarioL é uma parametro
        flash('Usuario Logado com Sucesso')
        return redirect('/Cadastro')
    else:
        flash('Usuário não encontrado') #flash manda uma mensagem
        return redirect('/login')

@app.route('/Cadastro')
def cadastro():
    if 'Usuario_Logado' not in session:
        return redirect('/')
    else:
        return render_template('Cadastro.html', Titulo = "Cadastro dos jogadores")

@app.route("/criar", methods=['POST'])
def criar():
    if 'salvar' in request.form:
        nome = request.form['nome']
        idade = request.form['idade']
        posicao = request.form['posicao']
        nivel = request.form['nivel']
        cidade = request.form['cidade']
        dia = request.form['dia']
        horario = request.form['horario']
        obj = cadvolei(nome,idade,posicao,nivel,cidade,dia,horario)
        volleyball_players.append(obj)
        return redirect('/')
    elif 'deslogar' in request.form:
        session.clear()
        return redirect('/')

@app.route('/excluir/<nome>', methods=['GET','DELETE'])
def excluir(nome):
    for i, joga in enumerate(volleyball_players):
        if joga.nome == nome:
            volleyball_players.pop(i)
            break
    return redirect('/')

@app.route('/editar/<nome>', methods=['GET'])
def editar(nome):
    for i, joga in enumerate(volleyball_players):
        if joga.nome == nome:
            return render_template("Editar.html", volei=joga, Titulo="Alterar Jogador")

@app.route('/alterar', methods=['POST','PUT'])
def alterar():
    nome = request.form['nome']
    for i, joga in enumerate(volleyball_players):
        if joga.nome == nome:
            joga.nome = request.form['nome']
            joga.idade = request.form['idade']
            joga.posicao = request.form['posicao']
            joga.nivel = request.form['nivel']
            joga.cidade = request.form['cidade']
            joga.dia = request.form['dia']
            joga.horario = request.form['horario']
    return redirect('/')

if __name__ == '__main__':
    app.run()