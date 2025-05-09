# adiciona_locais.py
from flask import request, jsonify
from db import conecta_db
import html

class AdicionaLocais:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        @self.app.route('/adiciona-local', methods=['POST'])
        def adiciona():
            try:
                data = request.get_json()

                if not data:
                    return jsonify({'erro': 'Dados ausentes ou inválidos'}), 400

                titulo = html.escape(data.get('titulo', '').strip())
                descricao = html.escape(data.get('descricao', '').strip())
                mapa_url = html.escape(data.get('mapa_url', '').strip())
                tipo = data.get('tipo')
                imagens = data.get('imagens', [])  # agora é uma lista

                if isinstance(tipo, list):
                    tipo = ','.join(tipo)

                if not all([titulo, descricao, mapa_url]) or not imagens:
                    return jsonify({'erro': 'Todos os campos são obrigatórios, incluindo pelo menos uma imagem'}), 400

                conn = conecta_db()
                cursor = conn.cursor()

                # Inserir local
                cursor.execute(
                    """
                    INSERT INTO locais_turisticos (titulo, descricao, mapa_url, tipo)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (titulo, descricao, mapa_url, tipo)
                )
                local_id = cursor.lastrowid

                # Inserir imagens
                for url in imagens:
                    cursor.execute(
                        "INSERT INTO imagens_local (local_id, url) VALUES (%s, %s)",
                        (local_id, html.escape(url.strip()))
                    )

                conn.commit()
                cursor.close()
                conn.close()

                return jsonify({'mensagem': 'Local turístico e imagens adicionados com sucesso!'}), 201

            except Exception as e:
                print(f"[ERRO] {e}")
                return jsonify({'erro': 'Erro interno no servidor'}), 500



