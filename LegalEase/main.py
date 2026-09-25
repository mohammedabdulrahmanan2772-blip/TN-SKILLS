from legalEaseAPI.main import app

if __name__ == "__main__":
    import uvicorn
    import config
    uvicorn.run(app, host=config.BACKEND_HOST, port=config.BACKEND_PORT)
