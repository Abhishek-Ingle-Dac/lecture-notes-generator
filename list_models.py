import google.generativeai as genai

API_KEY = "AIzaSyAIzZKCd82Efe1gqknrvpx3PW9jrFgzSiA"
genai.configure(api_key=API_KEY)

try:
    models = genai.list_models()
    for m in models:
        print(f"MODEL: {m.name} | Supported methods: {m.supported_generation_methods}")
except Exception as e:
    print("❌ Could not list models:", e)
