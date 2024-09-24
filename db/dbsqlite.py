import sqlite3

class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER,
                descricao TEXT,
                preco_unitario REAL
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
                valor_total REAL,
                forma_pagamento VARCHAR(50) -- (e.g., Cash, Credit, Debit)
            );
        ''')

        self.curso.execute('''
            CREATE TABLE IF NOT EXISTS venda_produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venda_id INTEGER,
                produto_id INTEGER,
                quantidade INTEGER,
                preco_unitario REAL,
                valor_total REAL,
                FOREIGN KEY (venda_id) REFERENCES vendas(id),
                FOREIGN KEY (produto_id) REFERENCES produtos(produto_id)
            );
        ''')

        self.conn.commit()

    def insert_produto(self, produto_id, descricao, preco_unitario):
        self.cursor.execute('''
            INSERT INTO produtos (produto_id, descricao, preco_unitario)
            VALUES (?, ?, ?)
        ''', (produto_id, descricao, preco_unitario))
        self.conn.commit()

    def insert_venda(self, produto_id, quantidade, valor_total):
        self.cursor.execute('''
            INSERT INTO vendas (produto_id, quantidade, valor_total)
            VALUES (?, ?, ?)
        ''', (produto_id, quantidade, valor_total))
        self.conn.commit()

    def fetch_produto(self, produto_id):
        self.cursor.execute('''
            SELECT descricao, preco_unitario FROM produtos WHERE produto_id = ?
        ''', (produto_id,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
