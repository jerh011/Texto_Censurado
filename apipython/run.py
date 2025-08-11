from src.app import create_app

app = create_app()

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=bool(int(os.getenv("FLASK_DEBUG", "1"))))
