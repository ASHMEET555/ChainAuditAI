from fastapi import FastAPI
from core.database import engine, Base
from routers import dash, test

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FraudProof Ledger Backend")

app.include_router(dash.router)
app.include_router(test.router)
