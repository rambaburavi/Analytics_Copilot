from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from core.shared_pipeline import get_pipeline
from core.db_connection_manager import DBConnectionManager

app = FastAPI()

# Enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_manager = DBConnectionManager()


# ===============================
# Upload SQLite Database
# ===============================

@app.post("/upload_sqlite")
async def upload_sqlite(file: UploadFile = File(...)):

    db_path = f"uploaded_{file.filename}"

    with open(db_path, "wb") as f:
        f.write(await file.read())

    pipeline = get_pipeline()
    pipeline.connect_sqlite(db_path)

    return {
        "message": "SQLite database connected successfully"
    }


# ===============================
# Connect MySQL Database
# ===============================

@app.post("/connect_mysql")
def connect_mysql(config: dict):

    engine = db_manager.connect_mysql(
        config["host"],
        config["user"],
        config["password"],
        config["database"]
    )

    pipeline = get_pipeline()
    pipeline.executor.set_engine(engine)

    return {"message": "MySQL connected successfully"}


# ===============================
# Connect PostgreSQL Database
# ===============================

@app.post("/connect_postgres")
def connect_postgres(config: dict):

    engine = db_manager.connect_postgres(
        config["host"],
        config["user"],
        config["password"],
        config["database"]
    )

    pipeline = get_pipeline()
    pipeline.executor.set_engine(engine)

    return {"message": "PostgreSQL connected successfully"}


# ===============================
# Run Natural Language Query
# ===============================

@app.post("/query")
def query(data: dict):

    question = data["question"]

    pipeline = get_pipeline()

    sql, df, explanation, chart_json = pipeline.run(question)

    return {
        "sql": sql,
        "explanation": explanation,
        "columns": df.columns.tolist(),
        "rows": df.to_dict(orient="records"),
        "chart": chart_json
    }