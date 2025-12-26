
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.classify import router as classify_router
from app.routes.rag import router as rag_router

app = FastAPI(
	title="JusticeLens Backend",
	description="Backend API for the JusticeLens AI legal assistant.",
	version="1.0.0"
)

# Enable CORS for all origins
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/ping")
async def ping():
	return {
		"status": "alive",
		"message": "JusticeLens backend is running"
	}


# Include classify and rag routers with /api prefix
app.include_router(classify_router, prefix="/api")
app.include_router(rag_router, prefix="/api")
