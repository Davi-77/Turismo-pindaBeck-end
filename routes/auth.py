from flask import request, jsonify
from db import conecta_db
import bcrypt 

class auth_user:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        @self.app.route('/login', methods=['POST'])
        def login():
            data = request.get_json()
            email = data.get('email')
            senha = data.get('senha')

            if not email or not senha:
                return jsonify({'erro': 'Todos os campos devem estar preenchidos'}), 400

            conn = None
            cursor = None
            try:
                conn = conecta_db()
                cursor = conn.cursor(dictionary=True)

                # Busca o usuário apenas pelo email
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                usuario = cursor.fetchone()

                if not usuario:
                    return jsonify({'erro': 'Email ou senha inválidos'}), 401

                senha_hash_armazenada = usuario['senha'].encode('utf-8')

                # Verifica se a senha está correta
                if not bcrypt.checkpw(senha.encode('utf-8'), senha_hash_armazenada):
                    return jsonify({'erro': 'Email ou senha inválidos'}), 401

                # Sucesso
                return jsonify({'mensagem': 'sucesso!', 'usuario': usuario['email']}), 200

            except Exception as e:
                print(f"Erro no login: {e}")
                return jsonify({'erro': 'Erro interno do servidor'}), 500

            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()


        @self.app.route('/cadastro', methods=['POST'])      
        def cadastra_user():
            data = request.get_json()
            email = data.get('email')
            senha = data.get('senha')

            # Verificando se o email e a senha foram fornecidos
            if not email or not senha:
                return jsonify({'erro': 'Os campos devem estar preenchidos'}), 400
            
            # Validação simples de email
            if "@" not in email or "." not in email:
                return jsonify({'erro': 'E-mail inválido'}), 400
            
            # Validação simples de senha
            if len(senha) < 8:
                return jsonify({'erro': 'A senha deve ter pelo menos 8 caracteres'}), 400

            try:
                conn = conecta_db()
                cursor = conn.cursor()

                # Gerando o hash da senha
                senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

                # Inserindo no banco de dados
                cursor.execute('INSERT INTO users (email, senha) VALUES (%s, %s)', (email, senha_hash))

                if cursor.rowcount == 0:
                    return jsonify({'erro': 'Usuário não cadastrado'}), 500
                
                # Commitando as mudanças
                conn.commit()

                # Fechando a conexão e o cursor
                cursor.close()
                conn.close()

                return jsonify({'sucesso': 'Usuário cadastrado com sucesso!'}), 201

            except Exception as e:
                print(e)
                return jsonify({'erro': f'Erro: {str(e)}'}), 500


                        

