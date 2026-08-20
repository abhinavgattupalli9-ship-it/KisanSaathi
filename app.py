import os
import json
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Load mock database
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'mock_db.json')
mock_db = {}
if os.path.exists(DB_PATH):
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            mock_db = json.load(f)
    except Exception as e:
        print(f"Error loading mock database: {e}")

# Helper to read environment variables from .env manually
def load_env_api_key():
    # Check project directory env file first
    env_paths = ['.env']
    try:
        env_paths.append(os.path.expanduser('~/.env'))
    except Exception:
        pass
    for path in env_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    for line in f:
                        if line.strip().startswith('GEMINI_API_KEY='):
                            return line.split('=', 1)[1].strip().strip('"').strip("'")
        except Exception as e:
            print(f"Error reading env path {path}: {e}")
    # Fallback to standard environment variable
    return os.environ.get('GEMINI_API_KEY', '')

GEMINI_API_KEY = load_env_api_key()
if GEMINI_API_KEY:
    print("Gemini API key loaded. Live AI responses enabled.")
else:
    print("No Gemini API key found. Using simulated local AI engine.")

# Simulated local AI engine responses based on keywords
def get_simulated_ai_response(query, lang):
    q = query.lower()
    is_hi = lang == 'hi' or any(word in q for word in ['कहाँ', 'कैसे', 'क्या', 'कब', 'यूरिया', 'गेहूं', 'धान', 'कपास', 'लोन', 'पैसा', 'पानी', 'सिंचाई', 'खाद', 'बीज', 'मंडी'])
    
    if 'wheat' in q or 'गेहूं' in q:
        if 'sow' in q or 'बुवाई' in q:
            return (
                "🌱 **Wheat Sowing Guide**:\n"
                "1. Sowing time: Nov 1 to Nov 25 is best.\n"
                "2. Seed rate: 40-45 kg per acre.\n"
                "3. Treat seeds with Trichoderma (4g/kg seed) to prevent root diseases.\n"
                "🔊 *Tap the speaker icon to listen to this in Hindi or English.*"
                if not is_hi else
                "🌱 **गेहूं बुवाई गाइड**:\n"
                "1. बुवाई का समय: 1 नवंबर से 25 नवंबर सबसे अच्छा है।\n"
                "2. बीज दर: 40-45 किलोग्राम प्रति एकड़।\n"
                "3. जड़ रोगों से बचाव के लिए बुवाई से पहले बीजोपचार (ट्राइकोडरमा 4 ग्राम/किलो) अवश्य करें।"
            )
        elif 'rust' in q or 'रतुआ' in q or 'रोग' in q:
            return (
                "🍂 **Wheat Yellow Rust Alert**:\n"
                "Yellow rust shows as yellow powder stripes on leaves. If seen, spray Propiconazole 25 EC (200 ml/200L water per acre). You can also use sour lassi mixed with copper sulphate as a cheap organic repellent."
                if not is_hi else
                "🍂 **पीला रतुआ रोग चेतावनी**:\n"
                "पत्तियों पर पीले रंग की पाउडर वाली धारियां दिखती हैं। दिखने पर प्रोपिकोनाज़ोल 25 EC (200 मिली/200 लीटर पानी प्रति एकड़) का छिड़काव करें। जैविक उपाय के रूप में तांबे के बर्तन में रखी खट्टी लस्सी का छिड़काव भी कर सकते हैं।"
            )
        else:
            return (
                "🌾 **Wheat Advisory Overview**:\n"
                "Keep soil moist during Crown Root Initiation (21-25 days). Use balanced fertilizers: Urea (110 kg/acre), DAP (50 kg/acre). Avoid over-application of Urea as it harms soil health."
                if not is_hi else
                "🌾 **गेहूं सामान्य सलाह**:\n"
                "बुवाई के 21-25 दिनों बाद (मुकुट जड़ प्रारंभ समय) सिंचाई अत्यंत महत्वपूर्ण है। संतुलित मात्रा में उर्वरक डालें: यूरिया (110 किग्रा), डीएपी (50 किग्रा) प्रति एकड़। यूरिया के अत्यधिक उपयोग से बचें।"
            )

    elif 'rice' in q or 'paddy' in q or 'धान' in q or 'चावल' in q:
        if 'water' in q or 'irrigation' in q or 'पानी' in q or 'सिंचाई' in q:
            return (
                "💧 **Paddy Water Saving Advice**:\n"
                "Do not keep the field flooded constantly. Use Alternate Wetting and Drying (AWD) method. Let the water dry for 1-2 days before watering again. This saves 30% water and increases yield!"
                if not is_hi else
                "💧 **धान में पानी की बचत की सलाह**:\n"
                "खेत को हमेशा पानी से भरा न रखें। वैकल्पिक गीला और सूखा (AWD) तरीका अपनाएं। दोबारा सिंचाई करने से पहले पानी को 1-2 दिनों के लिए सूखने दें। इससे 30% पानी की बचत होती है!"
            )
        else:
            return (
                "🌾 **Paddy Cultivation Summary**:\n"
                "Transplanting should be done when nursery is 25-30 days old. Apply 10kg Zinc Sulphate per acre to prevent Khaira disease. Monitor for leaf folders and stem borers."
                if not is_hi else
                "🌾 **धान की खेती की मुख्य बातें**:\n"
                "रोपनी 25-30 दिन की नर्सरी होने पर करें। खैरा रोग से बचाव के लिए प्रति एकड़ 10 किग्रा जिंक सल्फेट डालें। पत्ती लपेटक और तना छेदक कीटों पर नजर रखें।"
            )

    elif 'cotton' in q or 'कपास' in q:
        if 'pest' in q or 'worm' in q or 'कीड़ा' in q or 'सूंडी' in q:
            return (
                "🐛 **Cotton Pink Bollworm Advice**:\n"
                "Use 5 pheromone traps per acre for early detection. Spray Neem Seed Kernel Extract (NSKE 5%) at early stage. If infestation crosses 10%, spray Profenofos 50 EC @ 400ml/acre."
                if not is_hi else
                "🐛 **कपास गुलाबी सूंडी (पिंक बॉलवर्म) सलाह**:\n"
                "शुरुआती पहचान के लिए प्रति एकड़ 5 फेरोमोन ट्रैप लगाएं। शुरुआती चरण में नीम बीज अर्क (NSKE 5%) का छिड़काव करें। प्रकोप 10% से अधिक होने पर प्रोफेनोफॉस 50 EC @ 400 मिली/एकड़ डालें।"
            )
        else:
            return (
                "🌱 **Cotton Growth Advisory**:\n"
                "Maintain line spacing of 90cm. Balance urea with potash to improve boll quality. Pick cotton only after dew dries in the morning to keep cotton clean."
                if not is_hi else
                "🌱 **कपास विकास सलाह**:\n"
                "कतारों के बीच 90 सेमी की दूरी रखें। डोडियों की गुणवत्ता बढ़ाने के लिए यूरिया के साथ पोटाश का भी उपयोग करें। रुई साफ रखने के लिए सुबह ओस सूखने के बाद ही चुगाई करें।"
            )

    elif 'urea' in q or 'fertilizer' in q or 'खाद' in q or 'उर्वरक' in q:
        return (
            "🧪 **Fertilizer Smart Use & Availability**:\n"
            "- **Balanced Dose**: Use DAP at sowing and Urea in splits (top-dressing). Over-use of Urea makes crops weak and damages soil.\n"
            "- **Alternatives**: Use Nano Urea (liquid spray, 1 bottle replaces 1 bag of urea) or vermicompost.\n"
            "- **Stock Check**: Open our 'Fertilizer Stock Finder' to check nearby PACS co-operative society inventories. If dealers demand high prices, report them to the local Agriculture Development Officer (ADO)."
            if not is_hi else
            "🧪 **उर्वरक स्मार्ट उपयोग और उपलब्धता**:\n"
            "- **संतुलित खुराक**: बुवाई के समय डीएपी और बाद में किश्तों में यूरिया डालें। यूरिया के अधिक उपयोग से फसल कमजोर होती है और मिट्टी खराब होती है।\n"
            "- **विकल्प**: नैनो यूरिया (तरल छिड़काव, 1 बोतल 1 बोरी यूरिया के बराबर है) या केंचुआ खाद का प्रयोग करें।\n"
            "- **स्टॉक जांच**: नजदीकी सहकारी समिति (PACS) के पास उपलब्ध स्टॉक की जांच के लिए हमारा 'उर्वरक खोजक' खोलें। कालाबाजारी होने पर कृषि अधिकारी से शिकायत करें।"
        )

    elif 'loan' in q or 'credit' in q or 'bank' in q or 'लोन' in q or 'कर्ज' in q or 'बैंक' in q:
        return (
            "💰 **Formal Bank Loan (Kisan Credit Card - KCC)**:\n"
            "- **Low Interest**: KCC offers loans at 4% annual interest (with timely repayment), while local money lenders charge 24% to 60%.\n"
            "- **Savings Example**: A loan of ₹20,000 from KCC costs just ₹800 interest per year, whereas a private lender will cost ₹6,000+.\n"
            "- **Documents Needed**: Land records (Fard/Khasra), Aadhaar, Bank Passbook, and crop sowing proof. Visit your nearest public bank or Cooperative Bank to apply."
            if not is_hi else
            "💰 **बैंक ऋण और किसान क्रेडिट कार्ड (KCC)**:\n"
            "- **कम ब्याज**: समय पर भुगतान करने पर KCC लोन 4% वार्षिक ब्याज पर मिलता है, जबकि साहूकार 24% से 60% तक वसूलते हैं।\n"
            "- **बचत उदाहरण**: ₹20,000 के ऋण पर KCC में साल भर का ब्याज केवल ₹800 होगा, जबकि साहूकार ₹6,000 से अधिक ले सकता है।\n"
            "- **दस्तावेज**: जमीन के कागजात, आधार कार्ड, बैंक पासबुक और बुवाई प्रमाण पत्र। आवेदन के लिए नजदीकी सहकारी या सरकारी बैंक जाएं।"
        )

    # General fallback
    return (
        "💡 **KisanSaathi Assistant Response**:\n"
        "Thank you for your question! For agricultural advice, you can type about crops (Wheat, Paddy, Cotton), fertilizers, or bank credit (KCC).\n"
        "To get immediate answers: try selecting the exact module buttons on the dashboard such as 'Crop Advisory', 'Market Prices' or 'Disease Checker'!"
        if not is_hi else
        "💡 **किसानसाथी सहायक उत्तर**:\n"
        "आपके प्रश्न के लिए धन्यवाद! खेती की सलाह के लिए आप फसलों (गेहूं, धान, कपास), खाद, या बैंक लोन (KCC) के बारे में पूछ सकते हैं।\n"
        "त्वरित सहायता के लिए: मुख्य स्क्रीन पर मौजूद बटनों (फसल सलाह, मंडी भाव, रोग पहचान) का उपयोग करें!"
    )

# Direct Gemini REST call
def call_gemini_api(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 400
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=8)
        if response.status_code == 200:
            res_json = response.json()
            # Extract text
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            print(f"Gemini API returned status code {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Gemini API exception: {e}")
    return None

# Page Routes
@app.route('/')
def index():
    return render_template('index.html')

# API Routes
@app.route('/api/db', methods=['GET'])
def get_db():
    return jsonify(mock_db)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    query = data.get('query', '').strip()
    lang = data.get('lang', 'en')
    
    if not query:
        return jsonify({"error": "Empty query"}), 400

    # If live Gemini is enabled, construct system context and call it
    if GEMINI_API_KEY:
        system_instructions = (
            "You are KisanSaathi, an agricultural expert AI helper designed for Indian farmers. "
            "Your user has low-literacy. Keep answers extremely simple, short, and highly actionable. "
            "Write in short sentences, bullet points, and use simple icons. "
            "Respond in the language requested (English or Hindi). "
            "Here is the local context of mock prices and recommendations: "
            f"{json.dumps(mock_db.get('crops', {}))} \n"
            f"User query: {query}"
        )
        live_res = call_gemini_api(system_instructions)
        if live_res:
            return jsonify({"response": live_res})
    
    # Fallback to simulated local AI responses
    response_text = get_simulated_ai_response(query, lang)
    return jsonify({"response": response_text})

@app.route('/api/disease-detect', methods=['POST'])
def detect_disease():
    # In a real app we would run image classification, here we mock it based on selection or uploaded name
    crop_selected = request.form.get('crop', 'wheat').lower()
    
    # Check if a file was uploaded
    uploaded_file = request.files.get('file')
    filename = uploaded_file.filename.lower() if uploaded_file else ''
    
    # Match the crop/disease
    disease_info = {}
    
    # If the user uploaded a file, try to match by name, otherwise use the selected crop dropdown
    if 'blast' in filename or 'rice' in filename or crop_selected == 'rice':
        disease_info = next((d for d in mock_db.get('diseases', []) if d['id'] == 'blast'), {})
    elif 'rust' in filename or 'wheat' in filename or crop_selected == 'wheat':
        disease_info = next((d for d in mock_db.get('diseases', []) if d['id'] == 'yellow_rust'), {})
    elif 'bollworm' in filename or 'cotton' in filename or crop_selected == 'cotton':
        disease_info = next((d for d in mock_db.get('diseases', []) if d['id'] == 'pink_bollworm'), {})
    else:
        # Default fallback
        disease_info = mock_db.get('diseases', [])[0]
        
    return jsonify(disease_info)

if __name__ == '__main__':
    # Run on port 5000, accessible locally
    app.run(host='127.0.0.1', port=5000, debug=True)
