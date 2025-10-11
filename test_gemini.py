import google.generativeai as genai

API_KEY = "AIzaSyAIzZKCd82Efe1gqknrvpx3PW9jrFgzSiA"  
genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel("gemini-1.5-pro")

    response = model.generate_content("Say hello!")
    print("✅ API working! Response:", response.text)
except Exception as e:
    print("❌ API or model error:", e)
