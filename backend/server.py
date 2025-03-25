import uvicorn

if __name__ == "__main__":
    print("\n=== Starting INEXORA AI Server ===")
    print("Server will be available at: http://localhost:8002")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8002,
        reload=False
    ) 