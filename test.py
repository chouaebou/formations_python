# source: https://www.youtube.com/watch?v=g0-7TrVCNtg

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utilitaires import ConnectionHandler
from models import Base, Product, Warehouse, Stock


host = "localhost"
port = "1433"
user = "sa"
password = "20111025"
dbname = "test_alchemy"
driver = "ODBC Driver 17 for SQL Server"    # "SQL Server"

try:    
    conhand = ConnectionHandler(host, port, user, password, dbname, driver)
    engine = conhand.connectionDB()    
    print("Success!")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # créer instamce session pour manipuler les objet
    Session = sessionmaker(bind=engine)
    session = Session()

    # I. INSÉRER LES DONNÉES EN BDD

    # créer les différents instances (chaussure, warehouse, stock) en BDD et committer
    created_product = Product(name='Chaussure', description='Une belle paire de chaussures', price=2.99)
    session.add(created_product)

    created_warehouse = Warehouse(name='Entrepôt A')
    session.add(created_warehouse)

    created_stock = Stock(quantity=100, product=created_product, warehouse=created_warehouse)
    session.add(created_stock)
    
    # Committer en BDD
    session.commit()

    # II. EXTRAIRE LES DONNÉES DANS LA BDD en utilisant la session
    print("EXTRAIRE LES DONNÉES EN BDD")
    print('-----------------------------')

    search_product = session.query(Product).filter(Product.name=='chaussure').first()
    print(f"Nom du Produit: {search_product.name}, Prix: {search_product.price}")

    search_warehouse = session.query(Warehouse).filter(Warehouse.name=='Entrepôt A').first()
    print(f"Nom du Warehouse: {search_warehouse.name}")

    # Extraire la valeur du stock du produit dont id = 1
    v_produit_id = 1
    #search_stock = session.query(Stock).filter(Stock.product_id==v_produit_id).first()
    search_stock = session.query(Stock).join(Warehouse).join(Product).filter(Product.id==Stock.product_id and Stock.warehouse_id==Warehouse.id).first()
    print(f"La valeur du stock du produit {search_stock.product.name} dans {search_stock.warehouse.name} est de {search_stock.quantity}")

    print()

    # III. MODIFIER LES DONNÉES EN BDD
    print("MODIFIER LES DONNÉES EN BDD")
    print('-----------------------------')

    created_product.price = 30.99
    modify_product = session.query(Product).filter(Product.name=='chaussure').first()
    print(f"Produit modifié: {modify_product.name}, Prix: {modify_product.price}")

    # IV. EXTRAIRE TOUTES LES DONNÉES DE LA TABLE Product
    print('Liste des produits')
    result = session.query(Product).all()
    print([p.name for p in result])

    print('Liste des produits dont le prix < 50')
    result = session.query(Product).filter(Product.price < 50).all()
    print([p.name for p in result])

    #print('Supprimer des produits dont le prix < 50')
    #result = session.query(Product).filter(Product.price < 50).delete()
    #print([p.name for p in result])

    #print('Modifier des produits dont le nom = Tennis')
    #result = session.query(Product).filter(Product.id==1 ).update({'name': 'Tennis'})
    #print([p.name for p in result])






    conhand.__del__()

except Exception as ex:
    print(ex)