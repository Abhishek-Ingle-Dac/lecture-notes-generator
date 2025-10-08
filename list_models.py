import google.generativeai as genai

API_KEY = "AIzaSyArJGb_6PUlZRKRgFl-r0ya9Yb1gYUu8no"
genai.configure(api_key=API_KEY)

try:
    models = genai.list_models()
    for m in models:
        print(f"MODEL: {m.name} | Supported methods: {m.supported_generation_methods}")
except Exception as e:
    print("❌ Could not list models:", e)
