from flask import request, jsonify
from db import conecta_db

class Locais:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        @self.app.route('/locais', methods=['GET'])
        def listar_locais():
            conn = None
            cursor = None
            try:
                conn = conecta_db()
                cursor = conn.cursor(dictionary=True)
                
                # Buscando todos os locais
                cursor.execute("SELECT * FROM locais_turisticos")
                locais = cursor.fetchall()

                # Para cada local, vamos buscar as imagens associadas
                for local in locais:
                    cursor.execute("SELECT url FROM imagens_local WHERE local_id = %s", (local['id'],))
                    imagens = cursor.fetchall()
                    local['imagens'] = [img['url'] for img in imagens]

                return jsonify(locais), 200

            except Exception as e:
                print(f"Erro ao listar locais: {e}")
                return jsonify({'erro': 'Erro interno do servidor'}), 500

            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()


        @self.app.route('/locais/<int:id>', methods=['GET'])
        def listar_por_id(id):
            conn = conecta_db()
            cursor = conn.cursor(dictionary=True)

            try:
                # Buscar o local
                cursor.execute("SELECT * FROM locais_turisticos WHERE id = %s", (id,))
                local = cursor.fetchone()

                if not local:
                    return jsonify({'erro': 'Local não encontrado'}), 404

                # Buscar imagens do local
                cursor.execute("SELECT url FROM imagens_local WHERE local_id = %s", (id,))
                imagens = [img['url'] for img in cursor.fetchall()]
                local['imagens'] = imagens

               
                return jsonify(local)

            finally:
                cursor.close()
                conn.close()
