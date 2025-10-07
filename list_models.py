import google.generativeai as genai

API_KEY = "AIzaSyBzYBd1cUjmxaJ4NASN5xFJRPMAa_ID1hE"
genai.configure(api_key=API_KEY)

try:
    models = genai.list_models()
    for m in models:
        print(f"MODEL: {m.name} | Supported methods: {m.supported_generation_methods}")
except Exception as e:
    print("❌ Could not list models:", e)
