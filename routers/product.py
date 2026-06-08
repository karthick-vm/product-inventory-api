from fastapi import APIRouter, HTTPException, Depends
from schemas.product import ProductCreate
from database import db_dependency
from models.product import Product, User
from security import get_current_user, admin_required

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("")
def get_all_products(db: db_dependency):
    db_products = db.query(Product).all()
    return db_products

@router.get("/{id}")
def get_product_by_id(id: int, db: db_dependency, current_user: User = Depends(get_current_user)):
    db_product = db.query(Product).filter(Product.id == id).first()
    if db_product:
        return db_product
    raise HTTPException(status_code=404, detail="product not found")

@router.post("")
def add_product(new_product: ProductCreate, db: db_dependency):
    db_product = Product(**new_product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return new_product

@router.put("/{id}")
def update_product(id: int, updated_product: ProductCreate, db: db_dependency):
    db_product = db.query(Product).filter(Product.id == id).first()
    if db_product:
        db_product.name = updated_product.name
        db_product.description = updated_product.description
        db_product.price = updated_product.price
        db_product.quantity = updated_product.quantity
        db.commit()
        return "product updated"
    raise HTTPException(status_code=404, detail="product not found")

@router.delete("")
def delete_product(id: int, db: db_dependency, current_user: User = Depends(admin_required)):
    db_product = db.query(Product).filter(Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted"
    raise HTTPException(status_code=404, detail="product not found")



