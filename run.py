print("RUN.PY STARTING")

try:
    from app import app
    print("APP IMPORTED SUCCESSFULLY")
except Exception as e:
    print("ERROR IMPORTING APP:")
    print(e)
    raise

from waitress import serve

print("STARTING SERVER")

serve(app, host='0.0.0.0', port=10000)