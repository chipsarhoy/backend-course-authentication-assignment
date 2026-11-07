import marshmallow as ma
import uuid

from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.product_category_xref import products_categories_association_table

class Products(db.Model):
    __tablename__ = "Products"

    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Companies.company_id"), nullable=False)
    product_name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String())
    price = db.Column(db.Float(), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    company = db.relationship("Companies", back_populates="products")
    categories = db.relationship("Categories", secondary=products_categories_association_table, back_populates="products")
    warranty = db.relationship("Warranties", back_populates="product", uselist=False, cascade="all, delete-orphan")

    def __init__(self, company_id, product_name, price, description=None, active=True):
        self.company_id = company_id
        self.product_name = product_name
        self.price = price
        self.description = description
        self.active = active

    def new_product_obj():
        return Products("", "", 0.0, None, True)

class ProductsSchema(ma.Schema):
    class Meta:
        fields = ['product_id',
        'product_name', 'description', 'price', 'active', 'company', 'categories', 'warranty']

    product_id = ma.fields.UUID()
    product_name = ma.fields.String(required=True)
    description = ma.fields.String(allow_none=True)
    price = ma.fields.Float(required=True)
    active = ma.fields.Boolean(dump_default=True)
    company = ma.fields.Nested('CompaniesSchema', exclude=['products'])
    categories = ma.fields.Nested('CategoriesSchema', many=True, exclude=['products'])
    warranty = ma.fields.Nested('WarrantiesSchema', exclude=['product'])

class MiniProductsSchema(ma.Schema):
    class Meta:
        fields = ['product_id', 'product_name', 'description', 'price', 'active', 'categories', 'warranty']
    
    product_id = ma.fields.UUID()
    product_name = ma.fields.String(required=True)
    description = ma.fields.String(allow_none=True)
    price = ma.fields.Float(required=True)
    active = ma.fields.Boolean(dump_default=True)
    categories = ma.fields.Nested('CategoriesSchema', many=True, exclude=['products'])
    warranty = ma.fields.Nested('WarrantiesSchema', exclude=['product'])

product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)
mini_products_schema = MiniProductsSchema(many=True)