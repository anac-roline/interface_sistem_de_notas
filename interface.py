import tkinter as tk
from tkinter import ttk
import random
import sqlite3

class Application:
    #Função Inicial da aplicação. Executa as demais funções de criação de interface, inicialização do banco de dados e preenchimento de dados
    def __init__(self, root=None):
        #Definindo o título e tamanho da janela que será criada
        root.title("Sistema de notas")
        root.geometry("800x600")

        #Executando função de conexão com o banco de dados e crianda as tabelas do sistema
        self.conexao_db()
        self.criar_tabelas()

        #Executando as funções responsáveis por adicionar os items à interface
        #Criando as tabs(alunos, cursos e notas) e preenchendo com widgtes(Entry, Button, Label, TreeView)
        self.criar_paginas(root)
        self.criar_pagina_alunos()
        self.criar_pagina_cursos()
        self.criar_pagina_notas()

        #Funções que preenchem as tabelas dos alunos, cursos e notas com informações salvas no banco de dados
        self.preencher_tabela_alunos()
        self.preencher_tabela_cursos()
        self.preencher_tabela_notas()

    #
    #Funções de conexão e criação de tabela no banco de dados
    #
    def conexao_db(self):
        self.conexao = sqlite3.connect("sistema_notas.db")
        self.cursor = self.conexao.cursor()

    def criar_tabelas(self): 
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos(
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                matricula TEXT NOT NULL,
                curso_id INTEGER NOT NULL,
                FOREIGN KEY (curso_id) REFERENCES cursos(id)
            );
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notas(
                id INTEGER PRIMARY KEY,
                aluno_id INTEGER NOT NULL,
                nota REAL NOT NULL CHECK (nota >= 0 AND nota <= 10),
                FOREIGN KEY (aluno_id) REFERENCES alunos(id)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cursos(
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL UNIQUE
            );
        """)

        self.conexao.commit()

    #
    #Funções para criação da interface
    #
    def criar_paginas(self, root):
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")

        self.frame1 = tk.Frame(notebook)
        self.frame2 = tk.Frame(notebook)
        self.frame3 = tk.Frame(notebook)


        self.frame1.configure(background="pink")
        self.frame2.configure(background="pink")
        self.frame3.configure(background="pink")
    

        notebook.add(self.frame1, text='Alunos')
        notebook.add(self.frame2, text='Cursos')
        notebook.add(self.frame3, text='Notas')

    def criar_pagina_alunos(self):
        self.input_alunos_nome = tk.Entry(self.frame1, width=22)
        self.input_alunos_matricula = tk.Entry(self.frame1, width=22)
        
        nome_cursos = self.listar_cursos()
        self.selected_option_curso = tk.StringVar()
        if (len(nome_cursos) > 0):
            self.selected_option_curso.set(nome_cursos[0])
            self.input_alunos_curso = tk.OptionMenu(self.frame1, self.selected_option_curso, *nome_cursos)
        else:
            self.input_alunos_curso = tk.OptionMenu(self.frame1, self.selected_option_curso, *nome_cursos, value="")

        tk.Button(self.frame1, width=15, text="Adicionar", command=self.adicionar_aluno).grid(row=0, column=3, padx=5, pady=5)

        self.input_alunos_nome.grid(row=0, column=0, padx=5, pady=5)
        self.input_alunos_matricula.grid(row=0, column=1, padx=5, pady=5)
        self.input_alunos_curso.grid(row=0, column=2, padx=5, pady=5)

        self.table = ttk.Treeview(self.frame1, columns=("col1", "col2", "col3", "col4"), show='headings')

        self.table.heading("col1", text="ID")
        self.table.heading("col2", text="NOME")
        self.table.heading("col3", text="MATRÍCULA")
        self.table.heading("col4", text="ID_CURSO")
        
        self.table.column("col1", anchor=tk.CENTER, width=100)

        self.table.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

    def criar_pagina_cursos(self):
        self.input_cursos_nome = tk.Entry(self.frame2, width=22)
        tk.Button(self.frame2, width=15, text="Adicionar", command=self.adicionar_curso).grid(row=0, column=1, padx=5, pady=5)

        self.input_cursos_nome.grid(row=0, column=0, padx=5, pady=5)

        self.table_cursos = ttk.Treeview(self.frame2, columns=("col1", "col2"), show='headings')

        self.table_cursos.heading("col1", text="ID")
        self.table_cursos.heading("col2", text="NOME")
        
        self.table_cursos.column("col1", anchor=tk.CENTER, width=100)

        self.table_cursos.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

    def criar_pagina_notas(self):
        matricula_alunos = self.listar_alunos_matricula()
        self.selected_option_matricula = tk.StringVar()
        if (len(matricula_alunos) > 0):
            self.selected_option_matricula.set(matricula_alunos[0])
            self.input_notas_aluno_id = tk.OptionMenu(self.frame3, self.selected_option_matricula, *matricula_alunos)
        else:
            self.input_notas_aluno_id = tk.OptionMenu(self.frame3, self.selected_option_matricula, *matricula_alunos, value="")

        self.input_notas_nota = tk.Entry(self.frame3, width=22)
        tk.Button(self.frame3, width=15, text="Adicionar", command=self.adicionar_notas).grid(row=0, column=3, padx=5, pady=5)

        self.input_notas_aluno_id.grid(row=0, column=0, padx=5, pady=5)
        self.input_notas_nota.grid(row=0, column=1, padx=5, pady=5)

        self.table_notas = ttk.Treeview(self.frame3, columns=("col1", "col2", "col3"), show='headings')

        self.table_notas.heading("col1", text="ID")
        self.table_notas.heading("col2", text="ALUNO_ID")
        self.table_notas.heading("col3", text="NOTA")
        
        self.table_cursos.column("col1", anchor=tk.CENTER, width=100)

        self.table_notas.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

    #
    #Funções para preencher as tabelas dos alunos, cursos e notas com os dados salvos no banco de dados
    #
    def preencher_tabela_alunos(self):
        resultado = self.cursor.execute("SELECT * FROM alunos")
        alunos = resultado.fetchall()

        for aluno in alunos:
            self.table.insert("", tk.END, values=(aluno[0], aluno[1], aluno[2], aluno[3]))

    def preencher_tabela_cursos(self):
        resultado = self.cursor.execute("SELECT * FROM cursos")
        cursos = resultado.fetchall()

        for curso in cursos:
            self.table_cursos.insert("", tk.END, values=(curso[0], curso[1]))

    def preencher_tabela_notas(self):
        resultado = self.cursor.execute("SELECT * FROM notas")
        notas = resultado.fetchall()

        for nota in notas:
            self.table_notas.insert("", tk.END, values=(nota[0], nota[1], nota[2]))
    

    #
    #Funções para adicionar aluno, curso e nota tanto nas tabelas da interface como no banco de dados
    #
    def adicionar_aluno(self):
        nome_aluno = self.input_alunos_nome.get()
        matricula_aluno = self.input_alunos_matricula.get()
        curso_aluno = self.selected_option_curso.get()

        self.input_alunos_nome.delete(0, tk.END)
        self.input_alunos_matricula.delete(0, tk.END)

        if (len(nome_aluno) == 0 or len(matricula_aluno) == 0 or len(curso_aluno) == 0):
            return

        if (self.cursor.execute("SELECT id FROM alunos WHERE matricula = ?", (matricula_aluno,)).fetchone() != None):
            print("Matricula já existe!")
            return 

        id = random.randint(0, 100000)

        curso_id = self.curso_nome_para_curso_id(curso_aluno)

        self.table.insert("", tk.END, values=(id, nome_aluno, matricula_aluno, curso_id))

        self.cursor.execute("INSERT INTO alunos(id, nome, matricula, curso_id) VALUES (?, ?, ?, ?)", (id, nome_aluno, matricula_aluno, curso_id))
        self.conexao.commit()

        self.atualizar_lista_matriculas()

    def adicionar_curso(self):
        nome_curso = self.input_cursos_nome.get()
       
        self.input_cursos_nome.delete(0, tk.END)

        if (len(nome_curso) == 0):
            return
        
        if (self.cursor.execute("SELECT id FROM cursos WHERE nome = ?", (nome_curso,)).fetchone() != None):
            print("curso ja existe")
            return

        id = random.randint(0, 100000)

        print(id, nome_curso)

        self.table_cursos.insert("", tk.END, values=(id, nome_curso))

        self.cursor.execute("INSERT INTO cursos(id, nome) VALUES (?, ?)", (id, nome_curso))
        self.conexao.commit()

        self.atualizar_lista_cursos()

    def adicionar_notas(self):
        aluno_matricula = self.selected_option_matricula.get()
        nota = self.input_notas_nota.get()

        self.input_notas_nota.delete(0, tk.END)

        aluno_id = self.matricula_aluno_para_id_aluno(aluno_matricula)

        print(aluno_matricula, aluno_id, nota)

        if (self.cursor.execute("SELECT id FROM alunos WHERE id = ?", (aluno_id, )).fetchone() == None):
            print("Aluno inexistente")
            return
    
        if (float(nota) < 0 or float(nota) > 10):
            print("Insira uma nota válida!")
            return

        id = random.randint(0, 100000)

        self.table_notas.insert("", tk.END, values=(id, aluno_id, nota))

        self.cursor.execute("INSERT INTO notas(id, aluno_id, nota) VALUES (?, ?, ?)", (id, aluno_id, nota))
        self.conexao.commit()

    #
    #Funções de suporte
    #
    def listar_cursos(self):
        resultado = self.cursor.execute("SELECT nome FROM cursos")
        nome_cursos = resultado.fetchall()

        lista = []
        for nome_curso in nome_cursos:
            lista.append(nome_curso[0])

        return lista
    
    def listar_alunos_matricula(self):
        resultado = self.cursor.execute("SELECT matricula FROM alunos")
        matricula_alunos = resultado.fetchall()

        lista = []
        for matricula_aluno in matricula_alunos:
            lista.append(matricula_aluno[0])

        return lista

    def curso_nome_para_curso_id(self, nome_curso):
        resultado = self.cursor.execute("SELECT id FROM cursos WHERE nome = ?", (nome_curso, ))
        return resultado.fetchone()[0]
    
    def matricula_aluno_para_id_aluno(self, matricula):
        resultado = self.cursor.execute("SELECT id FROM alunos WHERE matricula = ?", (matricula,))
        return resultado.fetchone()[0]

    #
    #Funções para atualizar o widget OptionMenu
    #Toda vez que um aluno ou curso é adicionado, é preciso atualizar a lista de matrícula e lista de curso
    #
    def atualizar_lista_matriculas(self):
        matricula_alunos = self.listar_alunos_matricula()
        self.input_notas_aluno_id['menu'].delete(0, 'end')
        for option in matricula_alunos:
            self.input_notas_aluno_id['menu'].add_command(label=option, command=lambda value=option: self.selected_option_matricula.set(value))
        
    def atualizar_lista_cursos(self):
        nome_cursos = self.listar_cursos()
        self.input_alunos_curso['menu'].delete(0, 'end')
        for option in nome_cursos:
            self.input_alunos_curso['menu'].add_command(label=option, command=lambda value=option: self.selected_option_curso.set(value))

    #
    #Função para fechar a conexão com o banco de dados. Executada no final do programa
    #
    def fechar_conexao(self):
        self.conexao.close()

#
#Criação a interface em si
#
root = tk.Tk()
application = Application(root)
root.mainloop()
application.fechar_conexao()
