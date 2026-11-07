from db import db


products_categories_association_table = db.Table(
    "ProductsCategoriesAssociation",
    db.Model.metadata,
    db.Column("product_id", db.ForeignKey("Products.product_id", ondelete="CASCADE"), primary_key=True),
    db.Column("category_id", db.ForeignKey("Categories.category_id", ondelete="CASCADE"), primary_key=True)
)