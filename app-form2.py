import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('clientes.db')
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT NOT NULL
)
""")
conn.commit()


# Função para limpar o formulário
def limpar_formulario():
  entry_nome.delete(0, tk.END)
  entry_email.delete(0, tk.END)
  entry_telefone.delete(0, tk.END)


# Função para salvar os dados do cliente no banco de dados
def salvar_cliente():
  nome = entry_nome.get().strip()
  email = entry_email.get().strip()
  telefone = entry_telefone.get().strip()

  if nome and email and telefone:
    cursor.execute(
        'INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)',
        (nome, email, telefone),
    )
    conn.commit()
    messagebox.showinfo('Sucesso', 'Cliente salvo com sucesso!')
    limpar_formulario()
  else:
    messagebox.showwarning('Atenção', 'Todos os campos devem ser preenchidos!')


# Função para visualizar os dados dos clientes em uma nova janela
def visualizar_clientes():
  janela_visualizacao = tk.Toplevel(root)
  janela_visualizacao.title('Clientes Cadastrados')
  janela_visualizacao.geometry('500x300')

  tree = ttk.Treeview(
      janela_visualizacao,
      columns=('ID', 'Nome', 'Email', 'Telefone'),
      show='headings',
  )
  tree.heading('ID', text='ID')
  tree.heading('Nome', text='Nome')
  tree.heading('Email', text='Email')
  tree.heading('Telefone', text='Telefone')

  tree.column('ID', width=40, anchor=tk.CENTER)
  tree.column('Nome', width=150)
  tree.column('Email', width=180)
  tree.column('Telefone', width=110)

  tree.pack(fill=tk.BOTH, expand=True)

  cursor.execute('SELECT * FROM clientes')
  for row in cursor.fetchall():
    tree.insert('', tk.END, values=row)


# Configuração da janela principal
root = tk.Tk()
root.title('Cadastro de Clientes')
root.geometry('350x220')

# Rótulos e campos de entrada
tk.Label(root, text='Nome:').pack(pady=(10, 0))
entry_nome = tk.Entry(root, width=40)
entry_nome.pack(pady=2)

tk.Label(root, text='Email:').pack(pady=(5, 0))
entry_email = tk.Entry(root, width=40)
entry_email.pack(pady=2)

tk.Label(root, text='Telefone:').pack(pady=(5, 0))
entry_telefone = tk.Entry(root, width=40)
entry_telefone.pack(pady=2)

# Frame para os botões
frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=15)

btn_salvar = tk.Button(frame_botoes, text='Salvar', command=salvar_cliente)
btn_salvar.pack(side=tk.LEFT, padx=5)

btn_limpar = tk.Button(frame_botoes, text='Limpar', command=limpar_formulario)
btn_limpar.pack(side=tk.LEFT, padx=5)

btn_visualizar = tk.Button(
    frame_botoes, text='Visualizar Clientes', command=visualizar_clientes
)
btn_visualizar.pack(side=tk.LEFT, padx=5)

# Iniciar loop da interface
root.mainloop()

# Fechar a conexão com o banco de dados ao encerrar o programa
conn.close()
