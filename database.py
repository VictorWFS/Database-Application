from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)

# Seu código original começa aqui:
conn = psycopg2.connect (
    dbname = "UNIVERSIDADE",
    user = "postgres",
    password = "150550",
    host = "localhost",
    port = "5432"
)

cursor = conn.cursor()

def AdicionarEstudante(Nome, Idade):
    cursor.execute("INSERT INTO ESTUDANTES (Nome, Idade) VALUES (%s, %s)", (Nome, Idade))
    conn.commit()

def AtualizarEstudante(IdEstudante, Nome=None, Idade=None):
    if Nome:
        cursor.execute("UPDATE ESTUDANTES SET Nome = %s WHERE Matricula = %s", (Nome, IdEstudante))
    if Idade:
        cursor.execute("UPDATE ESTUDANTES SET Idade = %s WHERE Matricula = %s", (Idade, IdEstudante))
    conn.commit()

def RemoverEstudante(IdEstudante):
    cursor.execute("DELETE FROM ESTUDANTES WHERE Matricula = %s", (IdEstudante))
    conn.commit()

def exibir_EstudantesCursos():
    cursor.execute("""
    SELECT ESTUDANTES.Nome, ESTUDANTES.Idade, CURSOS_GRADUAÇAO.NomeCurso
    FROM ESTUDANTES
    LEFT JOIN CURSOS_GRADUAÇAO ON ESTUDANTES.Matricula = CURSOS_GRADUAÇAO.IdEstudante
    """)
    rows = cursor.fetchall()
    print(rows)

def AdicionarCursoEstudante(NomeCurso, IdEstudante):
    cursor.execute("INSERT INTO CURSOS_GRADUAÇAO (NomeCurso, IdEstudante) VALUES (%s, %s)" ,(NomeCurso, IdEstudante))
    conn.commit()

def ExibirCursosEstudantes():
    cursor.execute(""" 
    SELECT CURSOS_GRADUAÇAO.NomeCurso, ESTUDANTES.Nome
    FROM CURSOS_GRADUAÇAO
    RIGHT JOIN ESTUDANTES ON ESTUDANTES.Matricula = CURSOS_GRADUAÇAO.IdEstudante
    """)
    rows = cursor.fetchall()
    print(rows)

def ExibirEstudantesCursos_Mudanças():
    cursor.execute(""" 
    SELECT Nome, Idade FROM ESTUDANTES
    UNION ALL
    SELECT NomeCurso, NULL FROM CURSOS_GRADUAÇAO
    """)
    rows = cursor.fetchall()
    print(rows)


@app.route('/')
def index():
    return render_template('formulario.html')


@app.route('/add_student', methods=['POST'])
def add_student():
    nome = request.form['nome']
    idade = request.form['idade']
    AdicionarEstudante(nome, idade)
    return "Estudante adicionado com sucesso!"

@app.route('/delete_student', methods = ['POST'])
def delete_student():
    id_estudante = request.form['estudante_id']
    RemoverEstudante(id_estudante)
    return "Estudante removido com sucesso!"


@app.route('/update_student', methods=['POST'])
def update_student():
    id_estudante = request.form['id_estudante']
    nome = request.form.get('nome', None)
    idade = request.form.get('idade', None)
    AtualizarEstudante(id_estudante, nome, idade)
    return "Estudante atualizado com sucesso!"

@app.route('/add_course', methods=['POST'])
def add_course():
    nome_curso = request.form['nome_curso']
    id_estudante = request.form['id_estudante']
    AdicionarCursoEstudante(nome_curso, id_estudante)
    return "Curso adicionado com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)

cursor.close()
conn.close()
