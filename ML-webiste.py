from flask import Flask, request, render_template_string
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer

app = Flask(__name__)

# Load the trained pipeline and feature list
model = joblib.load("model.pkl")
pipeline = joblib.load("pipeline.pkl")

# HTML Template (ultra premium design + animations)
html_page = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Stroke Prediction App</title>
  <style>
    /* ========== GLOBAL STYLES ========== */
    body { 
      font-family: 'Poppins', sans-serif; 
      background: linear-gradient(135deg, #1e90ff, #7f37ff, #ff0080);
      background-size: 400% 400%;
      animation: gradientBG 15s ease infinite;
      margin:0; padding:0; 
      display:flex; justify-content:center; align-items:center;
      min-height:100vh; overflow-x:hidden;
    }

    @keyframes gradientBG {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    /* Floating Particles */
    .particles {
      position: absolute;
      width: 100%;
      height: 100%;
      overflow: hidden;
      z-index:0;
    }
    .particles span {
      position: absolute;
      display: block;
      width: 20px; height: 20px;
      background: rgba(255,255,255,0.15);
      animation: floatUp 25s linear infinite;
      border-radius:50%;
    }
    @keyframes floatUp {
      from { transform: translateY(100vh) scale(0); opacity:0; }
      to { transform: translateY(-10vh) scale(1); opacity:1; }
    }
    .particles span:nth-child(odd) { background: rgba(255,255,255,0.08); }

    /* ========== CONTAINER ========== */
    .container {
      background: rgba(255,255,255,0.08); 
      backdrop-filter: blur(20px);
      border-radius: 25px; 
      padding: 40px 61px; 
      max-width:600px; 
      width:100%;
      box-shadow: 0 10px 40px rgba(0,0,0,0.3); 
      z-index:1;
      animation: dropIn 1.5s cubic-bezier(.19,1,.22,1);
    }

    @keyframes dropIn {
      from { opacity:0; transform: translateY(-80px) scale(0.95); }
      to { opacity:1; transform: translateY(0) scale(1); }
    }

    /* Title */
    h1 { 
      text-align:center; 
      font-size:2.5rem;
      margin-bottom:20px;
      background: linear-gradient(to right, #00ffe7, #ff0080, #ffe600);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-shadow: 0 0 20px rgba(255,255,255,0.3);
      animation: glowPulse 2s infinite alternate;
    }

    @keyframes glowPulse {
      from { text-shadow: 0 0 5px #fff, 0 0 15px #ff0080; }
      to { text-shadow: 0 0 20px #00ffe7, 0 0 35px #ffe600; }
    }

    /* Inputs */
    input[type=text] { 
      width:100%; 
      padding:14px; 
      margin-top:14px; 
      border:none; 
      border-radius:12px; 
      outline:none;
      background: rgba(255,255,255,0.85);
      transition: all 0.35s ease;
      font-size:1rem;
    }
    input[type=text]:focus {
      background: #fff;
      transform: scale(1.05);
      box-shadow: 0 0 12px rgba(30,144,255,0.8);
    }

    /* Button */
    button { 
      background: linear-gradient(135deg, #ff0080, #1e90ff, #7f37ff);
      color:white; 
      padding:16px; 
      border:none; 
      width:100%; 
      margin-top:22px; 
      border-radius:15px; 
      cursor:pointer; 
      font-size:1.2rem;
      font-weight:600;
      letter-spacing:1px;
      transition: all 0.4s ease;
      position: relative;
      overflow:hidden;
    }
    button::before {
      content:"";
      position:absolute;
      top:0; left:-100%;
      width:100%; height:100%;
      background: rgba(255,255,255,0.3);
      transform:skewX(-25deg);
      transition: all 0.7s ease;
    }
    button:hover::before { left:100%; }
    button:hover { transform: translateY(-3px) scale(1.05); box-shadow:0 8px 20px rgba(0,0,0,0.4); }

    /* Result Box */
    .result { 
      margin-top:28px; 
      padding:18px; 
      border-radius:15px;
      font-size:1.3rem;
      font-weight:bold;
      text-align:center;
      animation: fadePop 0.8s ease-out;
    }
    .healthy { 
      background: rgba(0,255,150,0.2); 
      border:2px solid #00e676; 
      color:#00e676; 
      text-shadow:0 0 8px #00e676; 
    }
    .danger { 
      background: rgba(255,0,80,0.2); 
      border:2px solid #ff1744; 
      color:#ff1744; 
      text-shadow:0 0 8px #ff1744;
    }

    @keyframes fadePop {
      from { opacity:0; transform:scale(0.8); }
      to { opacity:1; transform:scale(1); }
    }
  </style>
</head>
<body>
  <!-- floating background particles -->
  <div class="particles">
    <span style="left:10%; animation-duration:22s;"></span>
    <span style="left:30%; animation-duration:28s;"></span>
    <span style="left:50%; animation-duration:25s;"></span>
    <span style="left:70%; animation-duration:30s;"></span>
    <span style="left:90%; animation-duration:26s;"></span>
  </div>

  <div class="container">
    <h1> Dr Strokey</h1>

    <form method="POST" enctype="multipart/form-data">
      <input type="text" placeholder="Longitude" name="a"><br>
      <input type="text" placeholder="Latitude" name="b"><br>
      <input type="text" placeholder="Housing Median Age" name="c"><br>
      <input type="text" placeholder="Total Rooms" name="d"><br>
      <input type="text" placeholder="Total Bedrooms" name="e"><br>
      <input type="text" placeholder="Population" name="f"><br>
      <input type="text" placeholder="Households" name="g"><br>
      <input type="text" placeholder="Median Income" name="h"><br>
      <input type="text" placeholder="Ocean Proximity" name="i"><br>
      <button type="submit">(<>_<>) Predict Now</button>
    </form>

    {% if result %}
       <div class="result {% if 'not' in result %}healthy{% else %}danger{% endif %}">{{ result }}</div>
    {% endif %}
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        # If one-by-one values are given
        request.form.get("a")
        a = float(request.form["a"])
        b = float(request.form["b"])
        c = float(request.form["c"])
        d = float(request.form["d"])
        e = float(request.form["e"])
        f = float(request.form["f"])
        g = float(request.form["g"])
        h = float(request.form["h"])
        i = float(request.form['i'])
        
        
        input_feature = [[a,b,c,d,e,f,g,h,i]]
        dataFrame_feature = pd.DataFrame(input_feature,columns=['longitude','latitude','housing_median_age','total_rooms','total_bedrooms','population','households','median_income','ocean_proximity'])
        final_feature_upgrade = pipeline.transform(dataFrame_feature)
        prediction = model.predict(final_feature_upgrade)

        print(f'The House Price is :{prediction[0]}')
    
    return render_template_string(html_page, result=result)


if __name__ == "__main__":
    app.run(debug=True)
