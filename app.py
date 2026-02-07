from flask import Flask, render_template, request, jsonify
from zxcvbn import zxcvbn

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_password():
    try:
        data=request.json
        password=data.get('password','')

        if not password:
            return jsonify({'score':0,'feedback':'','suggestion':[],'crack_time':'0s'})
        
        print(f"DEBUG: analysing password:{password}")

        results=zxcvbn(password)

        print(f"DEBUG: score={results['score']}")

        return jsonify({'score':results['score'],
                    'feedback':results['feedback']['warning'],
                    'suggestions': results['feedback']['suggestions'],
                    'crack_time':results['crack_times_display']['offline_slow_hashing_1e4_per_second']
                    })
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({'error': str(e)}),500

if __name__=='__main__':
    app.run(debug=True)