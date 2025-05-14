from flask import request, jsonify
from db import conecta_db

class BuscaComentarios:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        # Listar comentários (GET)
        @self.app.route('/feedbacks', methods=['GET'])
        def listar_comentarios():
            try:
                conn = conecta_db()
                cursor = conn.cursor()
                cursor.execute("SELECT id, comentario, criado_em FROM feedbacks ORDER BY criado_em DESC")
                dados = cursor.fetchall()
                feedbacks = [{'id': row[0], 'comentario': row[1], 'criado_em': row[2]} for row in dados]
                return jsonify(feedbacks)
            except Exception as e:
                return jsonify({'erro': str(e)})

        # Deletar comentário (DELETE)
        @self.app.route('/feedbacks/<int:id>', methods=['DELETE'])
        def deletar_comentario(id):
            try:
                conn = conecta_db()
                cursor = conn.cursor()

                cursor.execute('DELETE FROM feedbacks WHERE id = %s', (id,))
                conn.commit()

                cursor.close()
                conn.close()

                return jsonify({'mensagem': 'Comentário deletado com sucesso'}), 200

            except Exception as e:
                return jsonify({'erro': str(e)}), 500
