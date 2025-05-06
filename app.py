from flask import Flask, request, jsonify, render_template
from database import DatabaseConnection, Categorie, Produit, Fournisseur, Approvisionnement
import uuid
from datetime import datetime

app = Flask(__name__)
db = DatabaseConnection()

# Route pour la page d'approvisionnements
@app.route('/')
@app.route('/approvisionnements')
def approvisionnements_page():
    return render_template('approvisionnements.html')

# Route pour la page des produits
@app.route('/produits')
def produits_page():
    return render_template('produits.html')

# Route pour la page des fournisseurs
@app.route('/fournisseurs')
def fournisseurs_page():
    return render_template('fournisseurs.html')

# API: Récupérer tous les approvisionnements
@app.route('/api/approvisionnements', methods=['GET'])
def get_approvisionnements():
    conn = db.get_connection()
    appro_table = Approvisionnement(str(uuid.uuid4()), datetime.now().isoformat(), 0, 0.0).db_table
    approvisionnements = appro_table.select_all(conn)
    conn.close()
    return jsonify(approvisionnements)

# API: Ajouter un approvisionnement
@app.route('/api/approvisionnements', methods=['POST'])
def add_approvisionnement():
    data = request.get_json()
    approvisionnement = Approvisionnement(
        approv_id=str(uuid.uuid4()),
        date_approv=datetime.now().isoformat(),
        qte=int(data.get('qte')),
        prix_acquis=float(data.get('prix_acquis'))
    )
    conn = db.get_connection()
    approvisionnement.db_table.insert_one(conn, approvisionnement.format_dict())
    conn.close()
    return jsonify({'message': 'Approvisionnement ajouté avec succès'}), 201

# API: Récupérer tous les produits
@app.route('/api/produits', methods=['GET'])
def get_produits():
    conn = db.get_connection()
    produit_table = Produit(str(uuid.uuid4()), "", 0, 0.0).db_table
    produits = produit_table.select_all(conn)
    conn.close()
    return jsonify(produits)

# API: Ajouter un produit
@app.route('/api/produits', methods=['POST'])
def add_produit():
    data = request.get_json()
    produit = Produit(
        produit_id=str(uuid.uuid4()),
        libelle=data.get('libelle'),
        qte_stock=int(data.get('qte_stock')),
        prix_unitaire=float(data.get('prix_unitaire'))
    )
    conn = db.get_connection()
    produit.db_table.insert_one(conn, produit.format_dict())
    conn.close()
    return jsonify({'message': 'Produit ajouté avec succès'}), 201

# API: Récupérer tous les fournisseurs
@app.route('/api/fournisseurs', methods=['GET'])
def get_fournisseurs():
    conn = db.get_connection()
    fournisseur_table = Fournisseur(str(uuid.uuid4()), "", "", "").db_table
    fournisseurs = fournisseur_table.select_all(conn)
    conn.close()
    return jsonify(fournisseurs)

# API: Ajouter un fournisseur
@app.route('/api/fournisseurs', methods=['POST'])
def add_fournisseur():
    data = request.get_json()
    fournisseur = Fournisseur(
        fournisseur_id=str(uuid.uuid4()),
        nom=data.get('nom'),
        numero=data.get('numero'),
        email=data.get('email')
    )
    conn = db.get_connection()
    fournisseur.db_table.insert_one(conn, fournisseur.format_dict())
    conn.close()
    return jsonify({'message': 'Fournisseur ajouté avec succès'}), 201

if __name__ == '__main__':
    db.initialize()  # Créer la base de données et les tables si elles n'existent pas
    app.run(debug=True)