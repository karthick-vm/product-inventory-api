from fastapi import FastAPI
from database import session, engine         # for init_db() & engine didn't use because of alembic
from schemas.product import ProductCreate    # for init_db() only
import models.product                        # for init_db() only

# from fastapi.middleware.cors import CORSMiddleware  # for accessing frontend

from routers import product, auth

app = FastAPI()

app.include_router(product.router)
app.include_router(auth.router)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_methods=["*"],
#     allow_headers=["*"],
#     allow_credentials=True
# )

# models.product.Base.metadata.create_all(bind=engine)   # We use alembic for sending Base.metadata to DB

products = [
    ProductCreate(id=1, name="phone", description="budget phone", price=99.0, quantity=5),
    ProductCreate(id=2, name="laptop", description="budget laptop", price=999.99, quantity=3),
    ProductCreate(id=3, name="speaker", description="budget speaker", price=199.1, quantity=4),
    ProductCreate(id=4, name="headset", description="budget headset", price=59.8, quantity=1),
]

def init_db():
    db = session()
    count = db.query(models.product.Product).count()
    if count == 0:
        for product in products:
            db.add(models.product.Product(**product.model_dump()))
        db.commit()
    db.close()
init_db()

