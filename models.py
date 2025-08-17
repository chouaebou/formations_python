from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# créer une classe de base héritée par tous nos modèles de données
Base = declarative_base()

class Warehouse(Base):
    __tablename__ = 'warehouses'

    # noms des champs
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))

    # relation avec la class Stock qui est mappée par 
    stocks = relationship('Stock', back_populates='warehouse')

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    description = Column(String(100))
    price = Column(Float)

    stocks = relationship('Stock', back_populates='product')

class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)

    # définir la FK vers les tables warehouses et products et autres
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    product_id = Column(Integer, ForeignKey('products.id'))

    warehouse = relationship('Warehouse', back_populates='stocks')
    product = relationship('Product', back_populates='stocks')
