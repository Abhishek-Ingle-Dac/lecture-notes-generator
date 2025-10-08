import google.generativeai as genai

API_KEY = "AIzaSyArJGb_6PUlZRKRgFl-r0ya9Yb1gYUu8no"  
genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel("gemini-1.5-pro")

    response = model.generate_content("Say hello!")
    print("✅ API working! Response:", response.text)
except Exception as e:
    print("❌ API or model error:", e)
